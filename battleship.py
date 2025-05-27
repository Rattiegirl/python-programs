import random

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


# SHIPS = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1] 
SHIPS = [3] 
total_ship_decks = 0
ROWS = 10
COLS = 10

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

def user_turn(comp_sea_visible, comp_sea):
    print("Your turn! Where would you like to shoot?")
    alphabet = "abcdefghij"
    coordinate = input()
    row = int(coordinate[1:]) - 1
    col = alphabet.index(coordinate[0])
    if hit(comp_sea, row, col):
        print("You hit a ship! Your turn again.")
        comp_sea_visible[row][col] = "#"
        comp_sea[row][col] = "X"
        return True
    else:
        print("Aww, you missed. Bot's turn!")
        return False

def comp_turn(user_sea_visible, user_sea):
    print("The bot is thinking...")

    row = random.randint(0, ROWS)
    col = random.randint(0, COLS)
    if hit(user_sea, row, col):
        print("Bot hit a ship! Bot's turn again...")
        user_sea_visible[row][col] = "#"
        user_sea[row][col] = "X"
        return True
    else:
        print("Bot missed. Your turn!")
        return False



def start():

    user_sea = create_sea(ROWS, COLS)
    comp_sea = create_sea(ROWS, COLS)
    user_sea_visible = create_sea(ROWS, COLS)
    comp_sea_visible = create_sea(ROWS, COLS)
    place_random_ships(user_sea, SHIPS)
    place_random_ships(comp_sea, SHIPS)

    render_seas(user_sea, comp_sea_visible, comp_sea, user_sea_visible) # 1
    is_it_user_turn = random.choice([True, False]) # check
    while True:
        if is_it_user_turn:
            if user_turn(comp_sea_visible, comp_sea): # 2
                if no_ships(comp_sea, total_ship_decks): # 3
                    print("YOU WIN YAAAY")
                    break
            else:
                is_it_user_turn = False
        else:
            if comp_turn(user_sea_visible, user_sea): # 4
                if no_ships(user_sea, total_ship_decks):
                    print("YOU LOSE HAHA")
                    break
            else: 
                is_it_user_turn = True

        render_seas(user_sea, comp_sea_visible, comp_sea, user_sea_visible)


start()                     
                
    