"""
A partir de l'exercice 2 :
- A partir des informations retournes par l'environnement a chaque step, essayez d'implémenter votre propre IA
(via des systèmes de règles "expertes") pour faire tenir l'agent en équilibre le plus longtemps possible
    - Les actions possibles sont 0 et 1 (force appliqué sur le plateau vers la gauche ou la droite)
    - Les observations fournies par l'environnement sont :
    [position of cart, velocity of cart, angle of pole, rotation rate of pole]
"""

import gym

env = gym.make('CartPole-v0')
env.reset()

env._max_episode_steps = 1000000000
action = 1
done = False
run = 10
step_count = 0
avg = 0

for i_episode in range(run):
    observation = env.reset()
    for step in range(1000000000):
        observation, reward, done, _ = env.step(action)
        pos, velocity, angle, rotation = observation
        # print(observation)

        # if angle < 0:
        #     action = 0
        # elif angle > 0:
        #     action = 1

        # if rotation > .05:
        #     action = 1
        # elif rotation < -.05:
        #     action = 0

        if angle > 0.1:
            action = 1
        elif angle < -0.1:
            action = 0
        elif rotation > 0.18:
            action = 1
        elif rotation < -0.18:
            action = 0
        elif velocity > 0.025:
            action = 1
        elif velocity < -0.025:
            action = 0
        elif pos < -0.4:
            action = 0
        elif pos > 0.4:
            action = 1
        else:
            action = (action + 1) % 2

        # env.render()

        if done:
            break
    env.close()
    print("Vous avez tenu ", step, "steps")
    step_count = step_count + step

avg = step_count / run
print("Moyenne: ", avg, " en ", run)
