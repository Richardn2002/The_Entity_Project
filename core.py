class Entity():
    def __init__(self,columnCount,InputEncoderParams,toL4ConnectorParamsI,toL4ConnectorParamsII,toL5ConnectorParams,toD1ConnectorParams,toD2ConnectorParams,L4Params,L5Params,k,D1Params,D2Params):
        self.columnCount = columnCount
        self.toL4ConnectorParamsI = toL4ConnectorParamsI
        self.toL4ConnectorParamsII = toL4ConnectorParamsII
        self.toL5ConnectorParams = toL5ConnectorParams
        self.toD1ConnectorParams = toD1ConnectorParams
        self.toD2ConnectorParams = toD2ConnectorParams
        self.L4Params = L4Params
        self.L5Params = L5Params
        self.k = k
        self.D1Params = D1Params
        self.D2Params = D2Params
        self.learning = False

        #encoder
        from nupic.encoders import MultiEncoder
        self.InputEncoder = MultiEncoder()
        self.InputEncoder.addMultipleEncoders(InputEncoderParams)
        print "Encoder Online"

        #spatialPoolers
        from nupic.algorithms.spatial_pooler import SpatialPooler
        self.toL4ConnectorI = SpatialPooler(
            inputDimensions=(toL4ConnectorParamsI["inputDimensions"],),
            columnDimensions=(columnCount,),
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
        self.toL4ConnectorII = SpatialPooler(
            inputDimensions=(columnCount*3,),
            columnDimensions=(columnCount,),
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
        self.toL5Connector = SpatialPooler(
            inputDimensions=(columnCount,),
            columnDimensions=(columnCount,),
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
        self.toD1Connector = SpatialPooler(
            inputDimensions=(columnCount,),
            columnDimensions=(columnCount,),
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
        self.toD2Connector = SpatialPooler(
            inputDimensions=(columnCount,),
            columnDimensions=(columnCount,),
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

        #HTM Layers
        from nupic.algorithms.temporal_memory import TemporalMemory
        self.L4ActiveColumns = numpy.zeros(self.columnCount,dtype = int)
        self.L4 = TemporalMemory(
            columnDimensions = (columnCount,),
            seed = 42,
        )
        print "L4 Online"
        self.L5ActiveColumns = numpy.zeros(self.columnCount,dtype = int)
        self.L5 = TemporalMemory(
            columnDimensions = (columnCount,),
            seed = 42,
        )
        print "L5 Online"
        self.D1ActiveColumns = numpy.zeros(self.columnCount,dtype = int)
        self.D1 = TemporalMemory(
            columnDimensions = (columnCount,),
            seed = 42,
            initialPermanence=0.21,
            connectedPermanence=0.5,
        )
        print "D1 Online"
        self.D2ActiveColumns = numpy.zeros(self.columnCount,dtype = int)
        self.D2 = TemporalMemory(
            columnDimensions = (columnCount,),
            seed = 42,
            initialPermanence=0.21,
            connectedPermanence=0.5,
        )
        print "D2 Online"

    def encode_input (sine1,sine2,angularSpeed1,angularSpeed2,efferenceCopy):
        return self.InputEncoder.encode({"sine1":sine1,"sine2":sine2,"angularSpeed1":angularSpeed1,"angularSpeed2":angularSpeed2,"efferenceCopy":efferenceCopy})

    def reset (self):
        self.action = 0
        self.L4.reset()
        self.L5.reset()
        self.D1.reset()
        self.D2.reset()

    def mimic(self,observation,action):
        #mimicking only requires remembering the given obs-act pattern,thus the striatum is neglected in this func
        self.learning = True
        self.action = action
        encodedInput = self.encode_input(observation[0],observation[2],observation[4],observation[5],str(action))

        self.toL4ConnectorI.compute(encodedInput , self.learning , self.L4ActiveColumns)
        self.L4.compute(self.L4ActiveColumns , learn = self.learning)
        L4activeColumnIndices = numpy.nonzero(self.L4ActiveColumns)[0]

        L5Temp = numpy.zeros(self.columnCount,dtype = int)
        for column in L4activeColumnIndices:
            L5Temp[column] = 1
        self.toL5Connector.compute(L5Temp , self.learning , self.L5ActiveColumns)
        self.L5.compute(self.L5ActiveColumns , learn = self.learning)
        L5activeColumnIndices = numpy.nonzero(self.L5ActiveColumns)[0]

        #no action generation is needed in this func

    def learn(self,env,observation,expectedReaction):
        #We humans learn by trial and error,so does an AI agent.For neural networks,they have BP,but HTM does not
        #have a clear way to reinforcement learn(Where to feed in rewards?).Here I try to do something new.
        self.learning = False #...trial
        encodedInput = self.encode_input(observation[0],observation[2],observation[4],observation[5],str(self.action))

        self.toL4ConnectorI.compute(encodedInput , self.learning , self.L4ActiveColumns)
        L4Temp = numpy.zeros(self.columnCount *3 , dtype = int)#ready to receive D1's disinhibition and D2's inhibition
        L4activeColumnIndices = numpy.nonzero(self.L4ActiveColumns)[0]
        for column in L4activeColumnIndices:
            L4Temp[int(column)*3] = 1
        D1ActiveColumnsIndices = numpy.nonzero(self.D1ActiveColumns)[0]
        for column in D1ActiveColumnsIndices:
            L4Temp[int(column)*3+1] = 1
        D2ActiveColumnsIndices = numpy.nonzero(self.D2ActiveColumns)[0]
        for i in range(self.columnCount-1):
            L4Temp[i*3+2] = 1
        for column in D2ActiveColumnsIndices:  #achieve inhibition in this way
            L4Temp[i*3+2] = 0
        self.toL4ConnectorII.compute(L4Temp , self.learning , self.L4ActiveColumns)
        self.L4.compute(self.L4ActiveColumns , learn = self.learning)
        L4activeColumnIndices = numpy.nonzero(self.L4ActiveColumns)[0]

        L5Temp = numpy.zeros(self.columnCount , dtype = int)
        for column in L4activeColumnIndices:
            L5Temp[column] = 1
        self.toL5Connector.compute(L5Temp , self.learning , self.L5ActiveColumns)
        self.L5.compute(self.L5ActiveColumns,learn = self.learning)
        L5activeColumnIndices = numpy.nonzero(self.L5ActiveColumns)[0]

        #Action Generation
        p = 84 #there are 84 bits in the SDR representing the action fed in the agent,this is the "Efference Copy"
        count0 = 0
        count1 = 0
        count2 = 0
        for activeIndice in L5activeColumnIndices:
            convertedIndice = (activeIndice +1) * 1126 / columnCount
            if convertedIndice <= 1126 - p/4 and convertedIndice > 1126 - p /2 :
                count2 = count2 +1
            if convertedIndice <= 1126 - p/2 and convertedIndice > 1126 - 3* p /4 :
                count1 = count1 +1
            if convertedIndice <= 1126 - 3* p /4 and convertedIndice > 1126 - p :
                count0 = count0 +1

        if count2 == max(count0 , count1 , count2):
            self.action = 2
        if count1 == max(count0 , count1 , count2):
            self.action = 1
        if count0 == max(count0 , count1 , count2):
            self.action = 0

        #...and error
        if self.action == expectedReaction :
            reward = 0.1
        else :
            reward = -0.1

        self.D1.setConnectedPermanence(self.D1.getConnectedPermanence() * (self.k**(-reward)))#reward
        self.D2.setConnectedPermanence(self.D2.getConnectedPermanence() * (self.k**reward))#punishment

        #Learn to correct mistakes(remember what's right and whats' wrong)
        self.learning = True
        DTemp = numpy.zeros(self.columnCount,dtype = int)
        for column in L5activeColumnIndices:
            DTemp[column] = 1
        self.toD1Connector.compute(DTemp , self.learning , self.D1ActiveColumns)
        self.toD2Connector.compute(DTemp , self.learning , self.D2ActiveColumns)
        self.D1.compute(self.D1ActiveColumns , learn = self.learning)
        self.D2.compute(self.D2ActiveColumns , learn = self.learning)

        return reward

    def react(self,observation):
        self.learning = False
        encodedInput = self.encode_input(observation[0],observation[2],observation[4],observation[5],str(self.action))

        self.toL4ConnectorI.compute(encodedInput , self.learning , self.L4ActiveColumns)
        L4Temp = numpy.zeros(self.columnCount *3 , dtype = int)
        L4activeColumnIndices = numpy.nonzero(self.L4ActiveColumns)[0]
        for column in L4activeColumnIndices:
            L4Temp[int(column)*3] = 1
        D1ActiveColumnsIndices = numpy.nonzero(self.D1ActiveColumns)[0]
        for column in D1ActiveColumnsIndices:
            L4Temp[int(column)*3+1] = 1
        D2ActiveColumnsIndices = numpy.nonzero(self.D2ActiveColumns)[0]
        for i in range(self.columnCount-1):
            L4Temp[i*3+2] = 1
        for column in D2ActiveColumnsIndices:
            L4Temp[i*3+2] = 0
        self.toL4ConnectorII.compute(L4Temp , self.learning , self.L4ActiveColumns)
        self.L4.compute(self.L4ActiveColumns , learn = self.learning)
        L4activeColumnIndices = numpy.nonzero(self.L4ActiveColumns)[0]

        L5Temp = numpy.zeros(self.columnCount , dtype = int)
        for column in L4activeColumnIndices:
            L5Temp[column] = 1
        self.toL5Connector.compute(L5Temp , self.learning , self.L5ActiveColumns)
        self.L5.compute(self.L5ActiveColumns,learn = self.learning)
        L5activeColumnIndices = numpy.nonzero(self.L5ActiveColumns)[0]

        p = 84
        count0 = 0
        count1 = 0
        count2 = 0
        for activeIndice in L5activeColumnIndices:
            convertedIndice = (activeIndice +1) * 1126 / columnCount
            if convertedIndice <= 1126 - p/4 and convertedIndice > 1126 - p /2 :
                count2 = count2 +1
            if convertedIndice <= 1126 - p/2 and convertedIndice > 1126 - 3* p /4 :
                count1 = count1 +1
            if convertedIndice <= 1126 - 3* p /4 and convertedIndice > 1126 - p :
                count0 = count0 +1

        if count2 == max(count0 , count1 , count2):
            self.action = 2
        if count1 == max(count0 , count1 , count2):
            self.action = 1
        if count0 == max(count0 , count1 , count2):
            self.action = 0

        return self.action
