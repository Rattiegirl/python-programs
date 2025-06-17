import random
from battleship.lib import *

def start():
    old_seas = get_seas()
    if (len(old_seas) == 0):

        user_sea = create_sea(ROWS, COLS)
        comp_sea = create_sea(ROWS, COLS)
        user_sea_visible = create_sea(ROWS, COLS)
        comp_sea_visible = create_sea(ROWS, COLS)
        place_random_ships(user_sea, SHIPS)
        place_random_ships(comp_sea, SHIPS)
    else:
        [user_sea, comp_sea, user_sea_visible, comp_sea_visible] = old_seas
    render_seas(user_sea, comp_sea_visible, comp_sea, user_sea_visible) # 1
    is_it_user_turn = random.choice([True, False]) # check
    while True:
        if is_it_user_turn:
            save_seas(user_sea, comp_sea, user_sea_visible, comp_sea_visible)
            print("Your turn! Where would you like to shoot?")
            command = input()
            if (command == "gg"):
                clear_seas() 
                break   
            if (command == "break"):
                break
            if valid_coords(command):
                if user_turn(command, comp_sea_visible, comp_sea): # 2
                    if no_ships(comp_sea, total_ship_decks): # 3
                        print("YOU WIN YAAAY")
                        break
                else:
                    is_it_user_turn = False
            else: 
                print("The command is invalid. Please try something like a4, gg or break")
        else:
            print("The bot is thinking...")
            time.sleep(3)
            if comp_turn(user_sea_visible, user_sea): # 4
                if no_ships(user_sea, total_ship_decks):
                    print("YOU LOSE HAHA")
                    break
            else: 
                is_it_user_turn = True

        render_seas(user_sea, comp_sea_visible, comp_sea, user_sea_visible)


start()                     
                
    