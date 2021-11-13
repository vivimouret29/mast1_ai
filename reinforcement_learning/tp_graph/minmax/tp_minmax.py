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
    # TODO : implémentez votre heuristique en cas d'arret
    # Si le jeu est terminé, vous pouvez utiliser les méthodes ci-dessous pour trouver qui a gagné
    #env.ai_wins()
    #env.human_wins()
    return 0

def minmax(env, player, depth):
    """
    Methode minmax recursive
    :param env: l'environnement, ici le plateau du morpion
    :param player: le jouer actuel : ai = 1, human = -1. astuce : -1 * player nous permet d'avoir le joueur suivant
    :param depth: la profondeur actuelle, 0=arret de la recursion
    :return: (x,y), score
    x, y sont les coordonnées du meilleur coup trouvé
    score est le score associé à ce coup
    """
    # je vous aide : la condition d'arret est deja faite
    if depth == 0 or env.is_game_finished():
        score = heuristique(env)
        return (-1, -1), score

    for cell in list(env.empty_cells()): # parcours tout les coups possibles dans la situation actuelle
        x,y = cell
        ### Todo : completer la methode minmax
        ### Methodes utiles:
        ### env.copy() permet de copier un env. Attention à la taille mémoire, on fait beaucoup de recursion !
        ### env.set_move(x, y, player) permet de changer l'etat du board
        ### env.unset_move(x,y) permet d'enlever le mouvement joué
        ### player == env.ai permet de tester si le joueur actuel est ai
        ### player == env.human permet de tester si le joueur actuel est humain






    return best_move, best_score

"""
# Todo : de-commenter cette fonction pour tester votre fonction minmax
def get_ai_move(env):
    best_move, score = minmax(env, env.ai, depth=9)
    return best_move
"""

def main():
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