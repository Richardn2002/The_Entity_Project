#...
import numpy
numpy.set_printoptions(threshold="nan")
import os
_DIR = os.path.dirname(os.path.abspath(__file__))
_PARAMS_PATH = os.path.join(_DIR, "params", "model.yaml")

#loading data
import yaml
with open(_PARAMS_PATH, "r") as f:
  modelParams = yaml.safe_load(f)["model"]

columnCount = modelParams["columnCount"]
#encoder
InputEncoderParams = modelParams["sensor"]["encoders"]
#spatialPoolers
toL4ConnectorParamsI = modelParams["connectors"]["toL4I"]
toL4ConnectorParamsII = modelParams["connectors"]["toL4II"]
toL5ConnectorParams = modelParams["connectors"]["toL5"]
toD1ConnectorParams = modelParams["connectors"]["toD1"]
toD2ConnectorParams = modelParams["connectors"]["toD2"]
#HTM Layers
L4Params = modelParams["processors"]["cortex"]["L4"]
L5Params = modelParams["processors"]["cortex"]["L5"]
k = modelParams["processors"]["striatum"]["k"]
D1Params = modelParams["processors"]["striatum"]["D1"]
D2Params = modelParams["processors"]["striatum"]["D2"]

#the Entity
from core import Entity
agent = Entity(columnCount,InputEncoderParams,toL4ConnectorParamsI,toL4ConnectorParamsII,toL5ConnectorParams,toD1ConnectorParams,toD2ConnectorParams,L4Params,L5Params,k,D1Params,D2Params)
agent.reset()

#environment
import gym
env = gym.make("Acrobot-v1")
env.reset()
env.render()
print "Environment Online"

