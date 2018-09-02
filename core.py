
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
D1Params = modelParams["processors"]["striatum"]["D1"]
D2Params = modelParams["processors"]["striatum"]["D2"]
print "Params Loaded"

#building
#environment
import gym
env = gym.make("Acrobot-v1")
env.reset()
env.render()
print "Environment Online"
action = 0
observation,reward,done,info = env.step(action)
reward = 0.0 #the original reward signal has to be twisted
import math
def calcReward (obs):#return the height of the end of the pendulum in -1~1,simple trig!
    return -obs[0]-math.cos(math.acos(obs[0])+math.acos(obs[2]))

#encoder
from nupic.encoders import MultiEncoder
InputEncoder = MultiEncoder()
InputEncoder.addMultipleEncoders(InputEncoderParams)
def encode_input (sine1,sine2,angularSpeed1,angularSpeed2,efferenceCopy):
    return InputEncoder.encode({"sine1":sine1,"sine2":sine2,"angularSpeed1":angularSpeed1,"angularSpeed2":angularSpeed2,"efferenceCopy":efferenceCopy})
print "Encoder Online"

#spatialPoolers
from nupic.algorithms.spatial_pooler import SpatialPooler
toL4ConnectorI = SpatialPooler(
  inputDimensions=(toL4ConnectorParamsI["inputDimensions"],),
  columnDimensions=(toL4ConnectorParamsI["columnCount"],),
  potentialPct=toL4ConnectorParamsI["potentialPct"],
  globalInhibition=toL4ConnectorParamsI["globalInhibition"],
  localAreaDensity=toL4ConnectorParamsI["localAreaDensity"],
  numActiveColumnsPerInhArea=toL4ConnectorParamsI["numActiveColumnsPerInhArea"],
  synPermInactiveDec=toL4ConnectorParamsI["synPermInactiveDec"],
  synPermActiveInc=toL4ConnectorParamsI["synPermActiveInc"],
  synPermConnected=toL4ConnectorParamsI["synPermConnected"],
  boostStrength=toL4ConnectorParamsI["boostStrength"],
  seed=toL4ConnectorParamsI["seed"],
  wrapAround=toL4ConnectorParamsI["wrapAround"]
)#this part sucks
toL4ConnectorII = SpatialPooler(
  inputDimensions=(toL4ConnectorParamsII["inputDimensions"],),
  columnDimensions=(toL4ConnectorParamsII["columnCount"],),
  potentialPct=toL4ConnectorParamsII["potentialPct"],
  globalInhibition=toL4ConnectorParamsII["globalInhibition"],
  localAreaDensity=toL4ConnectorParamsII["localAreaDensity"],
  numActiveColumnsPerInhArea=toL4ConnectorParamsII["numActiveColumnsPerInhArea"],
  synPermInactiveDec=toL4ConnectorParamsII["synPermInactiveDec"],
  synPermActiveInc=toL4ConnectorParamsII["synPermActiveInc"],
  synPermConnected=toL4ConnectorParamsII["synPermConnected"],
  boostStrength=toL4ConnectorParamsII["boostStrength"],
  seed=toL4ConnectorParamsII["seed"],
  wrapAround=toL4ConnectorParamsII["wrapAround"]
)
print "toL4Connector Online"
toL5Connector = SpatialPooler(
  inputDimensions=(toL5ConnectorParams["inputDimensions"],),
  columnDimensions=(toL5ConnectorParams["columnCount"],),
  potentialPct=toL5ConnectorParams["potentialPct"],
  globalInhibition=toL5ConnectorParams["globalInhibition"],
  localAreaDensity=toL5ConnectorParams["localAreaDensity"],
  numActiveColumnsPerInhArea=toL5ConnectorParams["numActiveColumnsPerInhArea"],
  synPermInactiveDec=toL5ConnectorParams["synPermInactiveDec"],
  synPermActiveInc=toL5ConnectorParams["synPermActiveInc"],
  synPermConnected=toL5ConnectorParams["synPermConnected"],
  boostStrength=toL5ConnectorParams["boostStrength"],
  seed=toL5ConnectorParams["seed"],
  wrapAround=toL5ConnectorParams["wrapAround"]
)
print "toL5Connector Online"
toD1Connector = SpatialPooler(
  inputDimensions=(toD1ConnectorParams["inputDimensions"],),
  columnDimensions=(toD1ConnectorParams["columnCount"],),
  potentialPct=toD1ConnectorParams["potentialPct"],
  globalInhibition=toD1ConnectorParams["globalInhibition"],
  localAreaDensity=toD1ConnectorParams["localAreaDensity"],
  numActiveColumnsPerInhArea=toD1ConnectorParams["numActiveColumnsPerInhArea"],
  synPermInactiveDec=toD1ConnectorParams["synPermInactiveDec"],
  synPermActiveInc=toD1ConnectorParams["synPermActiveInc"],
  synPermConnected=toD1ConnectorParams["synPermConnected"],
  boostStrength=toD1ConnectorParams["boostStrength"],
  seed=toD1ConnectorParams["seed"],
  wrapAround=toD1ConnectorParams["wrapAround"]
)
print "toD1Connector Online"
toD2Connector = SpatialPooler(
  inputDimensions=(toD2ConnectorParams["inputDimensions"],),
  columnDimensions=(toD2ConnectorParams["columnCount"],),
  potentialPct=toD2ConnectorParams["potentialPct"],
  globalInhibition=toD2ConnectorParams["globalInhibition"],
  localAreaDensity=toD2ConnectorParams["localAreaDensity"],
  numActiveColumnsPerInhArea=toD2ConnectorParams["numActiveColumnsPerInhArea"],
  synPermInactiveDec=toD2ConnectorParams["synPermInactiveDec"],
  synPermActiveInc=toD2ConnectorParams["synPermActiveInc"],
  synPermConnected=toD2ConnectorParams["synPermConnected"],
  boostStrength=toD2ConnectorParams["boostStrength"],
  seed=toD2ConnectorParams["seed"],
  wrapAround=toD2ConnectorParams["wrapAround"]
)
print "toD2Connector Online"
actionOutput = SpatialPooler(
  inputDimensions=(2048,),
  columnDimensions=(3,),
  potentialPct=1.0,
  globalInhibition=True,
  localAreaDensity=-1.0,
  numActiveColumnsPerInhArea=1,
  synPermInactiveDec=0.05,
  synPermActiveInc=0.1,
  synPermConnected=0.2,
  boostStrength=3.0,
  seed=42,
  wrapAround=True
)
print "actionOutputer Online"
#HTM Layers
from nupic.algorithms.temporal_memory import TemporalMemory
L4ActiveColumns = numpy.zeros(2048,dtype = int)
L4 = TemporalMemory(
  seed=42
)
print "L4 Online"
L5ActiveColumns = numpy.zeros(2048,dtype = int)
L5 = TemporalMemory(
  seed = 42
)
print "L5 Online"
D1ActiveColumns = numpy.zeros(2048,dtype = int)
D1 = TemporalMemory(
  seed = 42,
  initialPermanence=0.21,
  connectedPermanence=0.5,
)
print "D1 Online"
D2ActiveColumns = numpy.zeros(2048,dtype = int)
D2 = TemporalMemory(
  seed = 42,
  initialPermanence=0.21,
  connectedPermanence=0.5,
)
print "D2 Online"

#computing
while True:
    while not done:

        input = encode_input(observation[0],observation[2],observation[4],observation[5],str(action))
        toL4ConnectorI.compute(input,True,L4ActiveColumns)
        L4Temp = numpy.zeros(6144,dtype = int)#ready to receive D1's disinhibition and D2's inhibition
        L4activeColumnIndices = numpy.nonzero(L4ActiveColumns)[0]
        for column in L4activeColumnIndices:
            L4Temp[int(column)*3] = 1
        D1ActiveColumnsIndices = numpy.nonzero(D1ActiveColumns)[0]
        for column in D1ActiveColumnsIndices:
            L4Temp[int(column)*3+1] = 1
        D2ActiveColumnsIndices = numpy.nonzero(D2ActiveColumns)[0]
        for i in range(2047):
            L4Temp[i*3+2] = 1
        for column in D2ActiveColumnsIndices:  #achieve inhibition in this way
            L4Temp[i*3+2] = 0
        toL4ConnectorII.compute(L4Temp,True,L4ActiveColumns)
        L4.compute(L4ActiveColumns,learn = True)
        L4activeColumnIndices = numpy.nonzero(L4ActiveColumns)[0]

        L5Temp = numpy.zeros(2048,dtype = int)
        for column in L4activeColumnIndices:
            L5Temp[L4activeColumnIndices] = 1
        toL5Connector.compute(L5Temp,True,L5ActiveColumns)
        L5.compute(L5ActiveColumns,learn = True)
        L5activeColumnIndices = numpy.nonzero(L5ActiveColumns)[0]

        DTemp = numpy.zeros(2048,dtype = int)
        for column in L5activeColumnIndices:
            DTemp[L5activeColumnIndices] = 1
        toD1Connector.compute(DTemp,True,D1ActiveColumns)
        toD2Connector.compute(DTemp,True,D2ActiveColumns)

        D1.compute(D1ActiveColumns,learn = True)

        D2.compute(D2ActiveColumns,learn = True)

        #action generation.I strongly doubt that if spatial pooling the L5 for outout is right...but
        actionTemp = numpy.zeros(3,dtype = int)
        actionOutput.compute(DTemp,True,actionTemp)
        action = actionTemp[0]

        #interact with the environment
        observation,reward,done,info = env.step(action)
        env.render()
        reward = calcReward(observation)
        k = 2
        D1.setConnectedPermanence(D1.getConnectedPermanence() * (k**(-reward)))#reward
        D2.setConnectedPermanence(D2.getConnectedPermanence() * (k**reward))#punishment

    observation = env.reset()
    action = 0










