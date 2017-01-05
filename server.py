from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid, ChartModule
from agents import *
from model import TechAdopt

def portrayal(agent):
  assert agent is not None

  portrayal = {
    "Shape": "rect",
    "w": 1,
    "h": 1,
    "Filled": True,
    "Layer": 0,
  }
  if agent.type == 0:
    if agent.adoption == False:
      portrayal['Color'] = 'white'
    else:
      portrayal['Color'] = 'orange'
  if agent.type == 1:
    if agent.adoption == False:
      portrayal['Color'] = '#e6ffe6'
    else:
      portrayal['Color'] = 'green'
  if agent.type == -1:
    if agent.adoption == False:
      portrayal['Color'] = '#ffe6e6'
    else:
      portrayal['Color'] = 'red'

  return portrayal

def launch(w, h, scale, num_steps):
  title = 'Modest Technology Adoption'
  grid = CanvasGrid(portrayal, w, h, w*scale, h*scale)
  chart = ChartModule([
    {'Label': 'AvgRate', 'Color': 'blue'}
  ], 300, 780)

  server = ModularServer(TechAdopt, [grid, chart], title, w, h)
  server.max_steps = num_steps
  server.port = 8889
  server.launch()
