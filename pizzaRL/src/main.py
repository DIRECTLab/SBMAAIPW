from pizzaenv import MultiAgentPizzaEnv
from stable_baselines3 import PPO

env = MultiAgentPizzaEnv()  # Flag to pull real data
model = PPO("MlpPolicy", env, verbose=1)

model.learn(total_timesteps=50000)  # Train directly on cluster

