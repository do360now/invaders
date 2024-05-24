import sys
import os


# Add the current directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from environment import AsteroidDodgeEnv

from stable_baselines3 import PPO
from stable_baselines3.common.env_checker import check_env

# Create the environment
env = AsteroidDodgeEnv()
check_env(env)  # Optional: check if the environment follows the Gym API

# Create the PPO model
model = PPO("CnnPolicy", env, verbose=1)

# Train the model
model.learn(total_timesteps=10000)

# Save the model
model.save("ppo_asteroid_dodge")

# To load the model later:
# model = PPO.load("ppo_asteroid_dodge", env=env)
