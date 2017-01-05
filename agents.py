import numpy as np
from mesa import Agent

class Person(Agent):
  threshold = 0.05
  ub_radius = 5
  noise = 0.05

  def __init__(self, aid, pos, model):
    super().__init__(aid, model)
    self.pos = pos
    self.type = 0
    self.radius = np.random.randint(1, self.ub_radius+1)
    self.adoption = False
    self.experience = False


  def step(self):
    if self.experience==False or self.type==0:
      if (np.random.rand() < self.noise):
        self.adoption = not self.adoption
      else:
        self.radius = self.update_radius()
        rate = self.get_adoption_rate(self.radius)
        '''Requiring the strict majority'''
        if rate != 0.5:
          self.adoption = (rate > 0.5)
      if self.adoption:
        self.experience = True
    else:
      if self.type==-1:
        self.adoption = False


  def update_radius(self):
    r = self.radius
    rate = self.get_adoption_rate(r)
    rate_plus = self.get_adoption_rate(r+1)
    '''Requiring being strictly greater than the threshold'''
    if abs(rate_plus - rate) > self.threshold:
      r += 1
    elif r >= 2:
      rate_minus = self.get_adoption_rate(r-1)
      if abs(rate_minus - rate) < self.threshold:
        r -= 1
    return r


  def get_adoption_rate(self, r):
    neighbors = self.model.grid.get_neighbors(self.pos, moore=True, radius=r)
    rate = np.mean([a.adoption for a in neighbors])
    return rate
