import numpy as np

class Morpion():

    def __init__(self):
        self.human = -1
        self.ai = +1
        self.state = np.zeros((3, 3))

    def set_choices(self, h_choice, c_choice):
        self.h_choice = h_choice
        self.c_choice = c_choice

    def empty_cells(self):
        return np.transpose(np.where(self.state == 0))

    def get_depth(self):
        return self.empty_cells().shape[0]

    def is_game_finished(self):
        return self.get_depth() == 0 or self.game_over()

    def is_winning(self, player):
        score = player * 3
        if (self.state.sum(axis=1) ==score).any() or (self.state.sum(axis=0)==score).any():
            # check if any line or column as 3 time the symbol
            return True
        if (self.state.trace() == score) or (self.state[::-1].trace()==score):
            # check diagonal
            return True
        return False

    def is_valid(self, x, y):
        return self.state[x,y] == 0

    def set_move(self, x, y, player):
        if self.is_valid(x, y):
            self.state[x][y] = player
            return True
        return False

    def unset_move(self,x,y):
        self.state[x][y] = 0

    def set_human_move(self, x, y):
        return self.set_move(x,y, self.human)

    def set_ai_move(self, x, y):
        return self.set_move(x, y, self.ai)

    def game_over(self):
        return self.is_winning(self.human) or self.is_winning(self.ai)

    def human_wins(self):
        return self.is_winning(self.human)

    def ai_wins(self):
        return self.is_winning(self.ai)

    def __copy__(self):
        new = Morpion()
        new.state = self.state.copy()
        new.set_choices(self.h_choice, self.c_choice)
        return new