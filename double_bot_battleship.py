import random
from battleship.lib import *

def start():

    comp_1_sea = create_sea(ROWS, COLS)
    comp_2_sea = create_sea(ROWS, COLS)
    comp_1_sea_visible = create_sea(ROWS, COLS)
    comp_2_sea_visible = create_sea(ROWS, COLS)
    place_random_ships(comp_1_sea, SHIPS)
    place_random_ships(comp_2_sea, SHIPS)

    is_it_bot_1s_turn = random.choice([True, False])

    while True:
        if is_it_bot_1s_turn:
            print("Bot 1 is thinking...")
            # time.sleep(1)
            if comp_turn(comp_2_sea_visible, comp_2_sea): # 4
                if no_ships(comp_2_sea, total_ship_decks):
                    print("BOT 2 LOST HAHA")
                    break
            else: 
                is_it_bot_1s_turn = False

        else:
            print("Bot 2 is thinking...")
            # time.sleep(2)
            if comp_turn(comp_1_sea_visible, comp_1_sea): # 4
                if no_ships(comp_1_sea, total_ship_decks):
                    print("BOT 1 LOST HAHA")
                    break
            else: 
                is_it_bot_1s_turn = True

        render_seas(comp_1_sea, comp_1_sea_visible, comp_2_sea, comp_2_sea_visible)

start()