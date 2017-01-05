import numpy as np
from mesa.time import BaseScheduler

class RandomSingleActivation(BaseScheduler):
  proportion = 0.2 # A portion of the agents move each period

  def step(self):
    num = int( self.proportion*len(self.agents) )
    np.random.shuffle(self.agents)
    for i in range(num):
      self.agents[i].step()

    self.steps += 1
    self.time += 1
