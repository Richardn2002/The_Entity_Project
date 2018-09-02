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
