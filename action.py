class Action:
        
        def isEastApplicable( _agentLocation, _stateSpace):
            # bounds check
            if _agentLocation[0] >= 2:
                return False
            # occupied check
            loc = [_agentLocation[0] + 1, _agentLocation[1], _agentLocation[2]]
            if _stateSpace[loc[0],loc[1],loc[2]].isOccupied():
                return False
            
            return True
        
        def isWestApplicable(_agentLocation, _stateSpace):
            # bounds check
            if _agentLocation[0] <= 0:
                return False
            # occupied check
            loc = [_agentLocation[0] - 1, _agentLocation[1], _agentLocation[2]]
            if _stateSpace[loc[0],loc[1],loc[2]].isOccupied():
                return False
            
            return True
        
        def isNorthApplicable(_agentLocation, _stateSpace):
            # bounds check
            if _agentLocation[1] >= 2:
                return False
            # occupied check
            loc = [_agentLocation[0], _agentLocation[1] + 1, _agentLocation[2]]
            if _stateSpace[loc[0],loc[1],loc[2]].isOccupied():
                return False
            
            return True
        
        def isSouthApplicable(_agentLocation, _stateSpace):
            # bounds check
            if _agentLocation[1] <= 0:
                return False
            # occupied check
            loc = [_agentLocation[0], _agentLocation[1] - 1, _agentLocation[2]]
            if _stateSpace[loc[0],loc[1],loc[2]].isOccupied():
                return False
            
            return True
        
        def isUpApplicable(_agentLocation, _stateSpace):
            # bounds check
            if _agentLocation[2] >= 2:
                return False
            # occupied check
            loc = [_agentLocation[0], _agentLocation[1], _agentLocation[2] + 1]
            if _stateSpace[loc[0],loc[1],loc[2]].isOccupied():
                return False
            
            return True
        
        def isDownApplicable(_agentLocation, _stateSpace):
            # bounds check
            if _agentLocation[2] <= 0:
                return False
            # occupied check
            loc = [_agentLocation[0], _agentLocation[1], _agentLocation[2] - 1]
            if _stateSpace[loc[0],loc[1],loc[2]].isOccupied():
                return False
            
            return True

        def moveEast(self, _agentLocation, _stateSpace):
            # perform bounds check
            if self.isEastApplicable(_agentLocation, _stateSpace): # TODO fix undefined error
                _agentLocation = [_agentLocation[0] + 1, _agentLocation[1], _agentLocation[2]]
        
        def moveWest(self, _agentLocation, _stateSpace):
            # perform bounds check
            if self.isWestApplicable(_agentLocation, _stateSpace): # TODO fix undefined error
                _agentLocation = [_agentLocation[0] - 1, _agentLocation[1], _agentLocation[2]]

        def moveNorth(self, _agentLocation, _stateSpace):
            # perform bounds check
            if self.isNorthApplicable(_agentLocation, _stateSpace): # TODO fix undefined error
                _agentLocation = [_agentLocation[0], _agentLocation[1] + 1, _agentLocation[2]]

        def moveSouth(self, _agentLocation, _stateSpace):
            # perform bounds check
            if self.isSouthApplicable(_agentLocation, _stateSpace): # TODO fix undefined error
                _agentLocation = [_agentLocation[0], _agentLocation[1] - 1, _agentLocation[2]]

        def moveUp(self, _agentLocation, _stateSpace):
            # perform bounds check
            if self.isUpApplicable(_agentLocation, _stateSpace): # TODO fix undefined error
                _agentLocation = [_agentLocation[0], _agentLocation[1], _agentLocation[2] + 1]

        def moveDown(self, _agentLocation, _stateSpace):
            # perform bounds check
            if self.isDownApplicable(_agentLocation, _stateSpace): # TODO fix undefined error
                _agentLocation = [_agentLocation[0], _agentLocation[1], _agentLocation[2] - 1]

        # def pickupBlock(Agent, StateSpace):
            # check Cell type == 'Pickup'
            # check numBlocks in Cell > 0
            # check is agent carrying a block == 0

        # def dropoffBlock(Agent, StateSpace):
            # check Cell type == 'Dropoff'
            # check numBlocks < 5
            # check is agent carrying a block == 1