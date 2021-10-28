# Cet exercice consiste, à partir de votre réponse à l'exercice précédent, à simulez un agent aléatoire
# dans Cartpole pendant 200 unités de temps.
# A chaque stepn vous devez :
#      - générez une action aléatoire et la proposer à gym
#      - visualiser l'environnement
import gym
print("TODO : importer gym, créer et initialiser l'environnement")

env = gym.make('CartPole-v0')
env.reset()

print("TODO : à chaque step de notre simulation : effectuer une action aléatoire, et afficher l'environnement")
for step in range(200):
    # env.action_space.sample permet d'obtenir une action aleatoire parmi l'espace d'action possible
    # env.step est la methode principale pour passer au prochain step ET soumettre une action
    env.render()
    done = env.step(env.action_space.sample())
    if done:
        break

print("TODO : pensez à fermer l'envionnement via sa méthode close")
env.close()


# Vous pouvez lancer plusieurs fois ce script, et remarquer que les actions, et donc les simulations, sont bien différentes
# les unes des autres
