import datetime
import numpy as np
from mesa import Model
from schedule import RandomSingleActivation
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector
from agents import Person

class TechAdopt(Model):
  types = (-1, 0, 1)
  alpha = 0.1
  beta = 0.1
  proportion_type = (beta, 1-alpha-beta, alpha)
  size_intervention = 0.5
  size_target = 1 # Targeted proportion of Goods
  treated = list() # Agents treated
  controlled = list() # Agents controlled

  def __init__(self, width, height, seed=None, mode=0):
    '''Truncate down to 9 digits as a seed must be between 0 and 4294967295'''
    if seed is None:
      seed = '{:%H%M%S%f}'.format(datetime.datetime.now())
      seed = int(seed[:9])
    np.random.seed(seed)
    self.seed = seed

    self.mode = mode # 0: random, 1: targeted
    self.width = width
    self.height = height
    self.N = width*height
    self.schedule = RandomSingleActivation(self)
    self.grid = MultiGrid(width, height, torus=True)

    '''The exact numbers of each agent'''
    self.size = [int(self.N*p) for p in self.proportion_type]
    self.size[1] = self.N - self.size[0] - self.size[2]

    '''Create agents'''
    aid = -1
    self.type0 = list() # Instances of type 0
    tmp = list()
    for i in range(len(self.types)):
      tmp.extend( [self.types[i]]*self.size[i] )
    np.random.shuffle(tmp)
    for contents, x, y in self.grid.coord_iter():
      aid += 1
      person = Person(aid, (x,y), self)
      person.type = tmp.pop()
      self.schedule.add(person)
      self.grid.place_agent(person, (x,y))
      if person.type == 0:
        self.type0.append(person)

    '''DataCollector'''
    self.datacollector = DataCollector(
      model_reporters = {
        "AvgRate": lambda m: sum(a.adoption for a in m.schedule.agents) / m.N},
      agent_reporters = {
        "Radius": lambda a: a.radius} )

    self.running = True


  def step(self):
    self.schedule.step()
    '''Intervention'''
    if self.schedule.steps == 1:
      num = int( self.size_intervention*self.N )
      if self.mode == 0:
        self.treated = self.intervene_random(num)
      elif self.mode == 1:
        self.treated = self.intervene_target(num)
      elif self.mode == 2:
        self.treated = self.intervene_block(num)
      for a in self.treated:
        a.adoption = True
        a.experience = True
      self.controlled = list( set(self.schedule.agents) - set(self.treated) )

    self.datacollector.collect(self)


  def intervene_random(self, num):
    treated = np.random.choice(self.schedule.agents, num, replace=False)
    return treated


  def intervene_target(self, num):
    pool = [a for a in self.schedule.agents if a.type == 1]
    num_Goods = int(self.size[2]*self.size_target)
    treated = list(np.random.choice(pool, num_Goods, replace=False))
    diff = num - len(treated)
    if diff <= 0:
      treated = np.random.choice(treated, num, replace=False)
    else:
      pool = list(set(self.schedule.agents) - set(treated))
      # pool = self.type0
      treated.extend( np.random.choice(pool, diff, replace=False) )
    return treated

  '''Target those in a block at the left-bottom corners'''
  def intervene_block(self, num):
    tmp = int( np.sqrt(num) )
    l = list()
    for x in range(tmp):
      for y in range(tmp):
        l.append((x,y))
    for y in range(tmp):
      if len(l) < num:
        l.append((tmp,y))
      else:
        break
    for x in range(tmp+1):
      if len(l) < num:
        l.append((x,tmp))
      else:
        break
    return self.grid.get_cell_list_contents(l)


def compute_ATT(model):
  treated = model.treated
  controlled = model.controlled
  avg_treat = np.mean([a.adoption for a in treated])
  avg_control = np.mean([a.adoption for a in controlled])
  return avg_treat - avg_control
