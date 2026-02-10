from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from battleship.lib import *
import os
import random 

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))
app = FastAPI()
app.mount("/pictures", StaticFiles(directory="pictures"), name="pictures")
app.mount("/css", StaticFiles(directory="css"), name="css")
app.mount("/js", StaticFiles(directory="js"), name="js")
app.mount("/sounds", StaticFiles(directory="sounds"), name="sounds")

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
}

# Расставим корабли при старте сервера
place_random_ships(game["user_sea"], SHIPS)
place_random_ships(game["bot_sea"], SHIPS)

@app.get("/state")
def get_state():
    global game
    return {
        "user_sea": game["user_sea"],
        "user_visible": game["user_visible"],
        "bot_sea": game["bot_sea"],
        "bot_visible": game["bot_visible"],
        "is_user_turn": game["is_user_turn"],
        "game_over": game["finished"],
        "winner": game["winner"],
    }

@app.post("/reset")
def resetGame():
    global game

    game["user_sea"] = create_sea(ROWS, COLS)
    game["bot_sea"] = create_sea(ROWS, COLS)
    game["user_visible"] = create_sea(ROWS, COLS)
    game["bot_visible"] = create_sea(ROWS, COLS)

    place_random_ships(game["user_sea"], SHIPS)
    place_random_ships(game["bot_sea"], SHIPS)

    save_seas(game["user_sea"], game["bot_sea"], game["user_visible"], game["bot_visible"])

    game["is_user_turn"] = True
    game["finished"] = False
    game["winner"] = None

    return{"message": "You have reset the game", **get_state()}


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
        if no_ships(game["bot_sea"], total_ship_decks):
            game["finished"] = True
            game["winner"] = "user"
            return {"result": "hit", "sunk": sunk, "message": "You win!", **get_state()}
        return {"result": "hit", "sunk": sunk, **get_state()}

    # промах — бот ходит
    game["bot_visible"][row][col] = "~"
    game["is_user_turn"] = False

    bot_result = bot_move()
    return {"result": "miss", "bot_result": bot_result, **get_state()}

def bot_move():
    if game["finished"]:
        return {"message": "Game already over"}

    # row, col = get_random_free_point(game["user_visible"])
    row, col = get_recursive_random_point(game["user_visible"])
    if hit(game["user_sea"], row, col):
        game["user_visible"][row][col] = "#"
        game["user_sea"][row][col] = "X"
        sunk, s_row, s_col, s_length, s_direction = sunk_check(game["user_sea"], row, col)
        game["is_user_turn"] = False
        bot_move()

        if sunk:
            surround_ship(game["user_visible"], s_row, s_col, s_direction, s_length)
            bot_move()

        if no_ships(game["user_sea"], total_ship_decks):
            game["finished"] = True
            game["winner"] = "bot"
            return {"result": "hit", "sunk": sunk, "message": "Bot wins!"}
        return {"result": "hit", "sunk": sunk}

        

    # промах — передаём ход обратно пользователю
    game["user_visible"][row][col] = "~"
    game["is_user_turn"] = True
    return {"result": "miss"}

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/storybook", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("storybook"
    ".html", {"request": request})
