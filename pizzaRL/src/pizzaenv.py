import gymnasium as gym
from gymnasium.spaces import Box
import numpy as np
from util import get_gpu_power, set_gpu_power, get_pizza_temp

class MultiAgentPizzaEnv(gym.Env):
    def __init__(self, max_steps=1000) -> None:
        super().__init__()
        # Observation space has the shape
        # gpu1 power, gpu2 power, pizza temp
        self.observation_space = Box(low=np.array([0, 0, 0]),
                                          high=np.array([350, 350, 200]),
                                          dtype=np.float32)


        # Action space: adjust the power draw of the gpu
        # -1 is -50W, 1 is +50W 
        self.action_space = Box(low=-1, high=1, shape=(2,), dtype=np.float32)

        
        self.gpu1_power = 0
        self.gpu2_power = 0

        self.target_temp = 80 # fahrenheight
        self.current_step = 0
        self.max_steps_per_ep = max_steps

        self.reset()

    def step(self, action):
        
        gpu1_power, gpu2_power = get_gpu_power()
        pizza_temp = get_pizza_temp()
        
        # take action [-1,1] and scale it by 50 to add or subtract 50W of power draw
        power_change_gpu1, power_change_gpu2 = action[0] * 50, action[1] * 50


        self.gpu1_power, self.gpu2_power = set_gpu_power(power_change_gpu1, power_change_gpu2)
        
        reward = -abs(self.pizza_temp - self.target_temp)

        
        self.current_step += 1

        done = self.current_step >= self.max_steps_per_ep


        return np.array([gpu1_power, gpu2_power, pizza_temp], dtype=np.float32), reward, done, done, {}

    def reset(self, seed=42, options={}):

        if np.random.rand() < 0.5:
            self.pizza_temp = 65
            self.gpu1_power = 0
            self.gpu2_power = 0
        else:
            self.pizza_temp = get_pizza_temp()
            self.gpu1_power, self.gpu2_power = get_gpu_power()

        return np.array([self.gpu1_power, self.gpu2_power, self.pizza_temp], dtype=np.float32), {}

    def render(self):
        print(f"step: {self.current_step} - Pizza temp: {self.pizza_temp}F, gpu1 power: {self.gpu1_power}W, gpu2 power: {self.gpu2_power}W")

