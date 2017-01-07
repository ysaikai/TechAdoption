import numpy as np
import datetime
# from mesa.batchrunner import BatchRunner
from mybatchrunner import MyBatchRunner
import pandas as pd
import matplotlib.pyplot as plt
from model import *

mode = [0,1] # 0: random, 1: targeted
mode_name = {0: 'Random', 1: 'Targeted'}
parameters = {'width': 30, 'height': 30, 'mode': mode}
batch_run = MyBatchRunner(
  TechAdopt,
  parameters,
  iterations=5,
  max_steps=10,
  model_reporters={
    "Rate": lambda m: sum(a.adoption for a in m.schedule.agents) / m.N,
    "ATT": compute_ATT,
    "seed": lambda m: m.seed} )
batch_run.run_all()

'''Resutls'''
df = batch_run.get_model_vars_dataframe()
df = df.set_index('Run')
df.sort_index(inplace=True)
df.to_csv('../output/' + '{:%Y%m%d%H%M%S.csv}'.format(datetime.datetime.now()))

'''Plot'''
for i in mode:
  plt.figure(mode_name[i])
  plt.hist(df['Rate'][df['mode']==i])
plt.show()
