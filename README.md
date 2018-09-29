# The Entity Project
Attempting to create a realtime learning and reacting agent by structurally simulating the brain (including the neocortex and basal ganglia pathways).Now using Nupic from Numenta.org as the base.

Read this:
https://discourse.numenta.org/t/proposing-a-model-for-the-basal-ganglia-and-reinforcement-learning-in-htm/2603

My original idea is to simulate the brain structure without fully urderstanding it. I just code to a extent that enough resources are given to my agent to complete tasks.

Most people view HTM layers provided by numenta are for memory,but I just view them as cortexes, although they are not very same as the biological ones.

The link given above present a theory to explain how basal gaglia pathways work. My coding is partly influnced by it. The writer called for people to test his ideas.So this repo is it.

# Now my agent has:
Striatum D1 neurons

Struatum D2 neurons

Cortex Layer 4

Cortex Layer 5

Hacky GPi and GPe

Motor output now is done by spatial pooling the whole L5. This is to be modified.
Maybe other cortex layers will be added soon.


#This Branch
is for A LOT changes
First trials of the master branch showed very negative results.I guess that something is missing for a HTM system to gain creativity.
So learning to complete the task given by my agent alone is not possible.It can neither figure out patterns nor filter out the answer from random.
But I still believe that my agent's structure is right.After thinking for a while,my hypothesis is now:

My agent should have three phases of interaction with the environment,mimicking,learning and reacting.

When in mimicking, the agent is provided with observation and the best action to tackle the past observation in time order.In this phase, the agent learn by memorizing.
It will soon be able to predict what the environment will be(awareness) and what action it will take(self-awareness) next timestep according to HTM Layers' properties.

When in learning, the agent's taken action(i.e.,the one the agent 'wants' to take)will be evaluated(by comparing it with the answer).If right, D1's synapse threshold
will be lowered(D2's will be strenghtened).Then both layers will be fed with the L5's columns' state.So gradually D1 will mostly predict right actions.
If the taken action is wrong,things will go negatively and D2 will mostly predict wrong actions.
L4's state will be combined with D1 and D2's states by those hacky GPi and GPe,then fed into L5 for action geneneration.

Reacting is a very normal phase where the agent is 'learned' and shows its ability of finishing the task.

Now I'm cleaning my code in an object-oriented way,clearifying properties and defining funcs.An UX/UI designer Kunologist is invited to code a research environment where
data can be collected in an organized way.The cleaning is for docking with the environment.
