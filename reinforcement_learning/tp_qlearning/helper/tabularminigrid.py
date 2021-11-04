# Bravo pour avoir ouvert ce fichier ! C’est super d’être curieux
# et de vouloir comprendre comment le code donné fonctionne

from enum import IntEnum

import gym
import gym_minigrid
import numpy as np
from gym import spaces, Wrapper
from gym_minigrid.minigrid import MiniGridEnv

class TabularMiniGrid(Wrapper):

    class Actions(IntEnum):
        right = 0
        down = 1
        left = 2
        up = 3

    def __init__(self, env, fix_seed=True):
        """Remplace les comportements par défaut de minigrid avec un champ de vision centré sur l’agent
        pour des données tabulaires (position de l’agent)"""
        super().__init__(env)
        self.env = env
        self.actions = self.Actions
        self.action_space = spaces.Discrete(len(self.actions))  # Action qui ne sont plus alocentrique mais absolu
        self.env.max_steps = np.infty  # Pas de baisse de la récompense au fur à chaque pas de temps
        self.env.agent_view_size = 3  # j’ai pas trouvé comment faire sauter le champs de vision (uniquement visuel)
        self.observation_space = spaces.Box(np.array((0, 0)), np.array((self.width, self.height)), dtype=int)
        self.fix_seed = fix_seed

    def reset(self):
        if self.fix_seed:
            self.env.seed(0)
        _ = self.env.reset()
        return np.array(self.agent_pos)

    def step(self, action):
        """Par défaut, minigrid est allocentrique (l’agent ne fait pas "haut", "bas" "gauche", "droite" mais
        "avancer tout droit", "tourner sur la gauche", "tourner sur la droite". Cette fonction rend les déplacement
        absolu et non plus allocentrique

        Par ailleurs, elle change les observation pour la position (x, y) de l’agent plutôt 
        """
        self.env.agent_dir = action
        _, reward, done, info = super().step(MiniGridEnv.Actions.forward)
        obs = np.array(self.agent_pos)
        return obs, reward, done, info



class WrongActionWrapper(Wrapper):
    def __init__(self, env, p=0.1):
        super().__init__(env)
        self.p = p

    def step(self, action):
        if np.random.random() < self.p:
            action = np.random.choice(self.env.actions)
        return self.env.step(action)
