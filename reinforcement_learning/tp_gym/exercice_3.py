"""
Exercice 3: Implémenter et visualiser des agents aléatoires sur les différents environnements disponibles
de gym
Bonus : les tester tous à la suite automatiquement !
"""
import time
import gym
env_list = gym.envs.registry.all()

print("Tous les environnements disponibles :", env_list)
print("Attention : tous ne sont pas disponibles par defaut dans gym !")


for env_id in env_list:
    time.sleep(5)
    env = gym.make(env_id.id)
    print("L'environnement ", env_id.id, " est en cours d'exécution...")
    env.reset()
    for step in range(2000):
        env.render()
        observation, reward, done, _ = env.step(env.action_space.sample())
        env.render()
        if done:
            break
    time.sleep(5)
    env.close()
