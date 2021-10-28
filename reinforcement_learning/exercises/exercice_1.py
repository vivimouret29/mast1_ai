import time
import gym

# Step 1 : créer l'environnement "Cartpole-v0" dans gym et le stocker dans la variable env
env = gym.make('CartPole-v0')

# Step 2: initialisez l'environnement au moyen de sa méthode reset()
env.reset()

# Step 3: visualisez votre environnement. Pensez à utiliser time.sleep(...) pour éviter
# l'affichage ne disparaisse immédiatement !
for _ in range(1000):
    env.render()

env.close()

