from stable_baselines3 import PPO
from environment import AsteroidDodgeEnv

# Create the environment
env = AsteroidDodgeEnv()

# Load the trained model
model = PPO.load("ppo_asteroid_dodge", env=env)

# Evaluate the agent
obs = env.reset()
for i in range(1000):
    action, _states = model.predict(obs, deterministic=True)
    obs, reward, done, info = env.step(action)
    env.render()
    if done:
        obs = env.reset()

env.close()
