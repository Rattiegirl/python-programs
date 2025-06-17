
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

def sunk_check(sea, row, col):
    pass

def surround_ship(sea, row, col):
    pass

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
    pass

def comp_turn(user_sea_visible, user_sea):
    row, col = get_recursive_random_point(user_sea_visible)
    # print(f"the {row} is the attempted row")

    # row, col = get_coord_dot(user_sea_visible)
    if hit(user_sea, row, col):
        user_sea_visible[row][col] = "#"
        user_sea[row][col] = "X"
        if sunk_check(user_sea, row, col):
            surround_ship(user_sea_visible, row, col)
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