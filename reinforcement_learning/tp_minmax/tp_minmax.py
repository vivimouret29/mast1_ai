from interface import Interface
from morpion import Morpion
import numpy as np

def get_ai_move(env):
    state = env.state
    print("Current state")
    print(state)
    empty_cases = env.empty_cells()
    nb_empty = len(empty_cases)
    choice = empty_cases[np.random.choice(nb_empty)]
    print("Ai choice ", choice)
    return choice

def heuristique(env):
    if env.ai_wins():
        return 1
    if env.human_wins():
        return -1
    return 0

def minmax(env, player, depth):
    if depth == 0 or env.is_game_finished():
        score = heuristique(env)
        return (-1, -1), score
    best_move = (-1, -1)
    if player == env.ai:
        best_score = -2
    else:
        best_score = 2
    for cell in list(env.empty_cells()):
        x,y = cell
        env.set_move(x,y,player)
        _, score = minmax(env,  -player, depth - 1)
        if player == env.ai and score > best_score:
            best_score = score
            best_move = (x, y)
        elif player == env.human and score < best_score:
            best_score = score
            best_move = (x, y)
        env.unset_move(x, y)

    return best_move, best_score

def get_ai_move(env):
    best_move, score = minmax(env, env.ai, depth=4)
    return best_move


def main():
    """
    Main function that calls all functions
    """
    env = Morpion()
    interface = Interface(env)
    interface.clean()

    interface.ask_params()
    interface.clean()

    # Main loop of this game
    while not env.is_game_finished():
        interface.human_turn()
        if env.is_game_finished():
            break
        x, y = get_ai_move(env)
        print(x, y)
        interface.ai_turn(x, y)

    # Game over message
    if env.human_wins():
        interface.clean()
        interface.render()
        print('YOU WIN!')
    elif env.ai_wins():
        interface.clean()
        interface.render()
        print('YOU LOSE!')
    else:
        interface.clean()
        interface.render()
        print('DRAW!')


if __name__ == "__main__":
    main()