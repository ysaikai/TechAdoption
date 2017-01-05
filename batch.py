import datetime
# from mesa.batchrunner import BatchRunner
from mybatchrunner import MyBatchRunner
import pandas as pd
import matplotlib.pyplot as plt
from model import *

parameters = {'width': 20, 'height': 20}
batch_run = MyBatchRunner(
  TechAdopt,
  parameters,
  iterations=10,
  max_steps=50,
  model_reporters={
    "Rate": lambda m: sum(a.adoption for a in m.schedule.agents) / m.N,
    "ATT": compute_ATT} )
batch_run.run_all()

'''Resutls'''
df = batch_run.get_model_vars_dataframe()
df = df.set_index('Run')
df.sort_index(inplace=True)
# print(df)
df.to_csv('../output/' + '{:%Y%m%d%H%M%S.csv}'.format(datetime.datetime.now()))
plt.hist(df['Rate'])
plt.show()
