import platform
from os import system
import numpy as np
import time

class Interface():
    def __init__(self, env):
        self.symbols = ["O", "X"]
        self.str_line = '---------------'
        self.env = env
        self.moves_dict = {
            1: [0, 0], 2: [0, 1], 3: [0, 2],
            4: [1, 0], 5: [1, 1], 6: [1, 2],
            7: [2, 0], 8: [2, 1], 9: [2, 2],
        }

    def ask_params(self):
        self.h_choice = ''  # X or O
        # Human chooses X or O to play
        while not self.h_choice in self.symbols:
            try:
                print('')
                self.h_choice = input('Choose X or O\nChosen: ').upper()
            except (KeyError, ValueError):
                print('Incorrect input')

        # Setting computer's choice
        i = 0
        self.c_choice = self.symbols[i]
        while self.c_choice == self.h_choice:
            i += 1
            self.c_choice = self.symbols[i]
        self.chars = {-1: self.h_choice, 1: self.c_choice, 0: ' '}
        self.env.set_choices(self.h_choice, self.c_choice)


    def render(self):
        print('\n' + self.str_line)
        for row in self.env.state:
            for cell in row:
                symbol = self.chars[cell]
                print(f'| {symbol} |', end='')
            print('\n' + self.str_line)

    def clean(self):
        os_name = platform.system().lower()
        if 'windows' in os_name:
            system('cls')
        else:
            system('clear')

    def human_turn(self):
        if self.env.is_game_finished():
            return
        self.clean()
        print(f'Human turn [{self.h_choice}]')
        self.render()
        move = 0
        while move < 1 or move > 9:
            try:
                move = int(input('Use numpad (1..9): '))
                coord = self.moves_dict[move]
                can_move = self.env.set_human_move(coord[0], coord[1])
                if not can_move:
                    print('Not valid move')
                    move = -1
            except (KeyError, ValueError):
                print('Incorrect input')

    def ai_turn(self, x, y):
        if self.env.is_game_finished():
            print("game finished")
            return

        self.clean()
        print(f'Computer turn [{self.c_choice}]')
        self.render()

        self.env.set_ai_move(x, y)
        time.sleep(1)