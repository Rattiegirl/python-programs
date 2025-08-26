from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from battleship.lib import *
import os
import random
import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))
app = FastAPI()
app.mount("/pictures", StaticFiles(directory="pictures"), name="pictures")

class MoveRequest(BaseModel):
    coordinate: str

# Глобальное состояние игры
game = {
    "user_sea": create_sea(ROWS, COLS),
    "bot_sea": create_sea(ROWS, COLS),
    "user_visible": create_sea(ROWS, COLS),
    "bot_visible": create_sea(ROWS, COLS),
    "is_user_turn": True,
    "finished": False,
    "winner": None,
    "move_log": [],  # Лог ходов
}

# Расставим корабли при старте сервера
place_random_ships(game["user_sea"], SHIPS)
place_random_ships(game["bot_sea"], SHIPS)

def add_move_log(player, coordinate, result, sunk=False):
    """Добавляет запись в лог ходов"""
    timestamp = datetime.datetime.now().strftime("%H:%M:%S")
    game["move_log"].append({
        "timestamp": timestamp,
        "player": player,
        "coordinate": coordinate,
        "result": result,
        "sunk": sunk
    })

@app.get("/state")
def get_state():
    return {
        "user_sea": game["user_sea"],
        "user_visible": game["user_visible"],
        "bot_sea": game["bot_sea"],
        "bot_visible": game["bot_visible"],
        "is_user_turn": game["is_user_turn"],
        "game_over": game["finished"],
        "winner": game["winner"],
        "move_log": game["move_log"],
    }

@app.post("/move")
def make_move(move: MoveRequest):
    if game["finished"]:
        return {"message": "Game is already finished", **get_state()}

    if not game["is_user_turn"]:
        return {"message": "It's not your turn", **get_state()}

    coord = move.coordinate.lower()
    if not valid_coords(coord):
        raise HTTPException(status_code=400, detail="Invalid coordinate format (use a1–j10)")

    alphabet = "abcdefghij"
    row = int(coord[1:]) - 1
    col = alphabet.index(coord[0])

    cell = game["bot_sea"][row][col]
    if cell in ("X", "~"):
        return {"message": "Already targeted", **get_state()}

    if hit(game["bot_sea"], row, col):
        game["bot_visible"][row][col] = "#"
        game["bot_sea"][row][col] = "X"
        sunk, s_row, s_col, s_length, s_direction = sunk_check(game["bot_sea"], row, col)
        if sunk:
            surround_ship(game["bot_visible"], s_row, s_col, s_direction, s_length)
        add_move_log("user", coord, "hit", sunk)
        if no_ships(game["bot_sea"], total_ship_decks):
            game["finished"] = True
            game["winner"] = "user"
            return {"result": "hit", "sunk": sunk, "message": "You win!", **get_state()}
        # Пользователь попал - ход остается за ним
        return {"result": "hit", "sunk": sunk, **get_state()}

    # промах — бот ходит
    game["bot_visible"][row][col] = "~"
    game["is_user_turn"] = False
    add_move_log("user", coord, "miss")

    # Бот делает ходы до промаха
    bot_moves = []
    while not game["is_user_turn"] and not game["finished"]:
        bot_result = bot_move()
        bot_moves.append(bot_result)
        if bot_result.get("continue"):
            # Бот попал и продолжает ходить
            continue
        else:
            # Бот промахнулся или игра закончилась
            break
    
    return {"result": "miss", "bot_moves": bot_moves, **get_state()}

def bot_move():
    if game["finished"]:
        return {"message": "Game already over"}

    # row, col = get_random_free_point(game["user_visible"])
    row, col = get_recursive_random_point(game["user_visible"])
    # Конвертируем координаты в формат a1-j10
    alphabet = "abcdefghij"
    coord = f"{alphabet[col]}{row + 1}"
    
    if hit(game["user_sea"], row, col):
        game["user_visible"][row][col] = "#"
        game["user_sea"][row][col] = "X"
        sunk, s_row, s_col, s_length, s_direction = sunk_check(game["user_sea"], row, col)
        if sunk:
            surround_ship(game["user_visible"], s_row, s_col, s_direction, s_length)
        add_move_log("bot", coord, "hit", sunk)
        if no_ships(game["user_sea"], total_ship_decks):
            game["finished"] = True
            game["winner"] = "bot"
            return {"result": "hit", "sunk": sunk, "message": "Bot wins!"}
        # Бот попал - продолжает ходить
        return {"result": "hit", "sunk": sunk, "continue": True}

    # промах — передаём ход обратно пользователю
    game["user_visible"][row][col] = "~"
    game["is_user_turn"] = True
    add_move_log("bot", coord, "miss")
    return {"result": "miss"}

@app.post("/reset")
def reset_game():
    """Сбрасывает игру к начальному состоянию"""
    global game
    
    # Создаем новые поля
    game["user_sea"] = create_sea(ROWS, COLS)
    game["bot_sea"] = create_sea(ROWS, COLS)
    game["user_visible"] = create_sea(ROWS, COLS)
    game["bot_visible"] = create_sea(ROWS, COLS)
    
    # Расставляем корабли заново
    place_random_ships(game["user_sea"], SHIPS)
    place_random_ships(game["bot_sea"], SHIPS)
    
    # Сбрасываем состояние игры
    game["is_user_turn"] = True
    game["finished"] = False
    game["winner"] = None
    game["move_log"] = []
    
    return {"message": "Game reset successfully", **get_state()}

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
