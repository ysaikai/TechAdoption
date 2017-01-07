import datetime
import sys
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

try:
  mode = int(sys.argv[1]) # mode: 1. Visualization, 2. Console for details
  if not(mode == 1 or mode == 2):
    print("Give me 1 or 2.")
    quit()
except IndexError:
  mode = 2
  print("A wrong argument! Processing as if '{}' were given...".format(mode))

if mode == 1:
  num_steps = 99
  w = 30
  h = 30
  scale = 400 // max(w, h)

  import server
  server.launch(w, h, scale, num_steps)

elif mode == 2:
  num_steps = 99
  w = 30
  h = 30

  import numpy as np
  import matplotlib.pyplot as plt
  # %matplotlib inline
  import pandas as pd
  pd.set_option('display.max_rows', None)
  from model import *

  m = TechAdopt(w, h)
  print('{:>4} {:5} {:6}'.format('ID','Adopt','Radius'))
  for i in range(num_steps):
    m.step()
    print("{:3d}. {:5.2f} {:6.2f}".format(
      m.schedule.steps,
      sum(a.adoption for a in m.schedule.agents) / m.N,
      np.mean([a.radius for a in m.type0]), ) )

  '''Model data'''
  print( 'ATT =', round(compute_ATT(m), 2) )
  print( 'seed =', m.seed)
  # df_m.to_csv('../output/' + '{:%Y%m%d%H%M%S.csv}'.format(datetime.datetime.now()))

  '''Agent data'''
  # df_a = m.datacollector.get_agent_vars_dataframe()
  # df = df_a.mean(level="AgentID")
  # print(df.join( df_a.std(level="AgentID" ), lsuffix='_m', rsuffix='_s' ))
