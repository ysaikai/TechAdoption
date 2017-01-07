from mesa.batchrunner import BatchRunner
from itertools import product
from collections import defaultdict
import pandas as pd

class MyBatchRunner(BatchRunner):

  def run_all(self):
    """ Run the model at all parameter combinations and store results. """
    params = self.parameter_values.keys()
    param_ranges = self.parameter_values.values()
    run_count = 0
    seed = defaultdict(dict)
    for param_values in list(product(*param_ranges)):
      kwargs = dict(zip(params, param_values))
      iter_count = 0
      for _ in range(self.iterations):
        run_count += 1
        iter_count += 1
        '''Use the stored seeds'''
        if seed.get(iter_count) is not None:
          kwargs['seed'] = seed[iter_count]
        model = self.model_cls(**kwargs)
        self.run_model(model)
        '''Collect and store results:'''
        if self.model_reporters:
          key = tuple(list(param_values) + [run_count])
          self.model_vars[key] = self.collect_model_vars(model)
        if self.agent_reporters:
          agent_vars = self.collect_agent_vars(model)
          for agent_id, reports in agent_vars.items():
            key = tuple(list(param_values) + [run_count, agent_id])
            self.agent_vars[key] = reports
        '''If not yet, store the seed'''
        if seed.get(iter_count) is None:
          seed[iter_count] = self.model_vars[key]['seed']
        '''Print progress'''
        print('Run =', run_count, '; Iter =', iter_count, '; mode =', kwargs['mode'])
