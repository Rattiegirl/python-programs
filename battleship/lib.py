
import random
import json
import os
import re
import time
from battleship.config import *

def render_sea(sea):

    for row in sea:
        for col in row:
            print(col, end = " ")
        print()

def create_sea(rows, cols):
    sea = []

    for r in range(rows):
        row = []

        for c in range(cols):
            row.append(".")

        sea.append(row)

    return sea

def in_sea(sea, r_id, c_id):

    if (r_id > len(sea) - 1) or (r_id < 0):

        return False
    
    if (c_id > len(sea[r_id]) - 1) or (c_id < 0):

        return False
    
    return True

def spot_is_available(sea, r_id, c_id):

    if not in_sea(sea, r_id, c_id):

        return False
    
    return sea[r_id][c_id] == "."


def place_in_sea(sea, r_id, c_id, sign = "-"):

    if in_sea(sea, r_id, c_id):

        sea[r_id][c_id] = sign


def place_ship(sea, row, col, length = 1, direction = True):

    row_index = row - 1
    col_index = col - 1

    if direction:

        for x in range(length):

            if spot_is_available(sea, row_index, col_index + x) == False:

                return False

        for x in range(length):

            sea[row_index][col_index + x] = "#"

            place_in_sea(sea, row_index, col_index + x + 1)
            place_in_sea(sea, row_index, col_index - 1)
           

            for x in range(length + 2):

                place_in_sea(sea, row_index - 1, col_index - 1 + x)
                place_in_sea(sea, row_index + 1, col_index - 1 + x)
               

    else:

        for x in range(length):

            if spot_is_available(sea, row_index + x, col_index) == False:

                return False
            
    
        for x in range(length):

            sea[row_index + x][col_index] = "#"

            place_in_sea(sea, row_index + x + 1, col_index)
            place_in_sea(sea, row_index - 1, col_index)
        

            for x in range(length + 2):

                place_in_sea(sea, row_index - 1 + x, col_index - 1)
                place_in_sea(sea, row_index - 1 + x, col_index + 1)


    return True

def place_random_ships(sea, ships): 

       

    for ship in ships:

        while True:

            row_index = random.randint(0, len(sea) - 1)
            col_index = random.randint(0, len(sea[row_index]) - 1)
            direction = random.choice([True, False])

            if place_ship(sea, row_index, col_index, ship, direction):

                break

for ship in SHIPS:
    total_ship_decks += ship

# print("Hello! Let's play some Battleship!")
# row = input("What row would you like to place your ship in?")
# col = input("What column would you like to place your ship in?")
# length = input("How long will the ship be?")
# direction = input("Will your ship stretch right [True] or up [False]?")
# print("Placing the ship...")
# place_ship(sea, row, col, length, direction)
# render_sea

# if input("Add more ships? Yes or No") == "Yes":

def menu():
    
    print("Hello! Let's play some Battleship!")

    sea = create_sea(ROWS, COLS)

    for ship in SHIPS:

        while True:

            print(f"Place a ship that is {ship} deck(s) long \n")
            row = int(input("What row would you like to place your ship in?\n"))
            col = int(input("What column would you like to place your ship in?\n"))
            direction = input("Will your ship stretch [r]ight or down (press enter)?\n") == "r"

            if place_ship(sea, row, col, ship, direction):

                print("Here is your sea layout as of now:")
                render_sea(sea)
                print()

                break

            else:
                
                print("Doesn't seem like a ship can be placed there, try again")
                      

# menu()

# sea = create_sea(ROWS, COLS)

# render_sea(sea)
# place_ship(sea, 3, 5, 1, True)
# place_ship(sea, 1, 1, 4, False)
# place_ship(sea, 3, 5, 4, False)
# place_ship(sea, 6, 4, 3, True)
# place_ship(sea, 11, 4, 3, True)
# place_ship(sea, 7, 4, 9, True)

# place_random_ships(sea, SHIPS)
# render_sea(sea)


def render_seas(user_sea, comp_sea_visible, comp_sea, user_sea_visible):
    render_sea(user_sea)
    print("\n")
    render_sea(comp_sea_visible)
    print("\n")
    render_sea(comp_sea)
    print("\n")
    render_sea(user_sea_visible)
    print("\n")

def no_ships(sea, total_ship_decks):
    hit_decks = 0
    for row in range(ROWS):
        for col in range(COLS):
            if (sea[row][col] == "X"):
                hit_decks += 1
    return hit_decks == total_ship_decks

def hit(sea, row, col):
    if (sea[row][col] == "#"):
        return True
    return False

def sunk_check_old(sea, row, col):

    if (sea[row + 1][col] == "#"):
        return False
    elif (sea[row - 1][col] == "#"):
        return False
    elif (sea[row][col + 1] == "#"):
        return False
    elif (sea[row][col - 1] == "#"):
        return False
    
    return True

def sunk_check(sea, row, col):
    # проверка на однопалубный корабль
    if (
        (row == 0 or sea[row-1][col] == "-") 
        and (col == 0 or sea[row][col-1] == "-") 
        and (row == ROWS-1 or sea[row+1][col] == "-") 
        and (col == COLS-1 or sea[row][col+1] == "-")
    ):
        return True, row, col, 1, True
    
    direction = False

    if (
        (col != 0 and sea[row][col-1] in ("#", "X")) 
        or (col != COLS-1 and sea[row][col+1] in ("#", "X")) 
    ):
        direction = True
    
    if direction:
        start_col = col
        while start_col > 0:
            if sea[row][start_col-1] == "#":
                return False, None, None, None, None
            if sea[row][start_col-1] == "X":
                start_col -= 1
            else: 
                break
            
        end_col = col
        while end_col < COLS-1:
            if sea[row][end_col+1] == "#":
                return False, None, None, None, None
            if sea[row][end_col+1] == "X":
                end_col += 1
            else: 
                break
        return True, row, start_col, end_col - start_col + 1, True
    
    else:
        start_row = row
        while start_row > 0:
            if sea[start_row-1][col] == "#":
                return False, None, None, None, None
            if sea[start_row-1][col] == "X":
                start_row -= 1
            else:
                break
        
        end_row = row
        while end_row < ROWS-1:
            if sea[end_row+1][col] == "#":
                return False, None, None, None, None
            if sea[end_row+1][col] == "X":
                end_row += 1
            else:
                break
        return True, start_row, col, end_row - start_row + 1, False

        
         
    
def surround_ship(sea, start_row, start_col, direction, length):
    if direction:
        min_col = 0
        max_col = COLS - 1
        # если слева нет стены
        if start_col > 0:
            sea[start_row][start_col-1] = "-"
            min_col = start_col - 1
         # если справо нет стены
        if start_col + length < COLS:
            sea[start_row][start_col + length] = "-"
            max_col = start_col + length
         # если сверху нет стены
        if start_row > 0:

            for i in range (min_col, max_col + 1):
                sea[start_row - 1][i] = "-"
        
         # если снизу нет стены
        if start_row < ROWS - 1:

            for i in range (min_col, max_col + 1):
                sea[start_row + 1][i] = "-"
   
    else:
        min_row = 0
        max_row = ROWS - 1
        if start_row > 0:
            sea[start_row - 1][start_col] = "-"
            min_row = start_row - 1
        if start_row + length < ROWS:
            sea[start_row + length][start_col] = "-"
            max_row = start_row + length
        if start_col > 0:
            for i in range(min_row, max_row + 1):
                sea[i][start_col - 1] = "-"
        if start_col < COLS - 1:
            for i in range(min_row, max_row + 1):
                sea[i][start_col + 1] = "-"






def user_turn(coordinate, comp_sea_visible, comp_sea):
    alphabet = "abcdefghij"
    # coordinate = input()
    row = int(coordinate[1:]) - 1
    col = alphabet.index(coordinate[0])
    if comp_sea[row][col] == None:
        print("Invalid command. Try ")
    if hit(comp_sea, row, col):
        comp_sea_visible[row][col] = "#"
        comp_sea[row][col] = "X"
        if sunk_check(comp_sea, row, col):
            surround_ship(comp_sea_visible, row, col)
            print("You sunk the ship! Aim for another one.")
        else: 
            print("You hit a ship! Your turn again.")
        
        return True
    else:
        print("Aww, you missed. Bot's turn!")
        comp_sea_visible[row][col] = "~"
        return False

def valid_coords(coordinate):
    return bool(re.fullmatch(r'^[a-j](?:10|[1-9])$', coordinate))

def get_coord_dot(sea):
    for row in range(ROWS):
        for col in range(COLS):
            if (sea[row][col] == "X"):
                if (sea[row+1][col] == "."):
                    dot_row = row + 1
                    dot_col = col
                elif (sea[row][col+1] == "."):
                    dot_row = row
                    dot_col = col + 1
                elif (sea[row-1][col] == "."):
                    dot_row = row - 1
                    dot_col = col
                elif (sea[row][col-1] == "."):
                    dot_row = row
                    dot_col = col - 1
    return dot_row, dot_col


def comp_turn(user_sea_visible, user_sea):
    row, col = get_recursive_random_point(user_sea_visible)
    # print(f"the {row} is the attempted row")

    # row, col = get_coord_dot(user_sea_visible)
    if hit(user_sea, row, col):
        user_sea_visible[row][col] = "#"
        user_sea[row][col] = "X"
        sunk, s_row, s_col, s_length, s_direction = sunk_check(user_sea, row, col)
        if sunk:
            surround_ship(user_sea_visible, s_row, s_col, s_direction, s_length)
            print("Bot sunk a ship! Thinking again...")
        else:
            print("Bot hit a ship! Bot's turn again...")
        return True
    else:
        print("Bot missed. Your turn!")
        user_sea_visible[row][col] = "~"
        return False

def get_recursive_random_point(sea_visible):

    row = random.randint(0, ROWS-1)
    col = random.randint(0, COLS-1)
    if sea_visible[row][col] == ".":
        return row, col
    else:
        return get_recursive_random_point(sea_visible)

def get_seas():

    file_path = "seas.json"
    try:
        with open(file_path, 'r') as file:
            seas = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        seas = []
    return seas

def save_seas(user_sea, comp_sea, user_sea_visible, comp_sea_visible):

    with open("seas.json", "w") as f:
        json.dump([user_sea, comp_sea, user_sea_visible, comp_sea_visible], f)

def clear_seas():

    os.remove("seas.json")