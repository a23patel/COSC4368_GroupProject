import numpy as np

class RLSpace:
    """
    An abstract class representing the Reinforcement Learning (RL) state space
    It provides mappings from the real-world state space, and information about the shape of the space.
    """
    def map_state(self, state, agent):
        """
        Given a real-world state, provide a state in the RL state space of the given agent
        """
        pass

    def shape(self):
        """
        Returns shape of RL space, used to generate Q table
        """
        pass

    def isDropoff(self, rlstate):
        pass

    def isPickup(self, rlstate):
        pass

    def isCarrying(self, rlstate):
        pass

class VSSpace(RLSpace):
    """
    "Very Simple" RL space: each agent's RL space contains only their coordinates, and whether they hold a block.
    """
    def map_state(self, state, agent):
        loc = state.get_location(agent)
        is_carrying = state.is_agent_carrying(agent)
        return (loc[0], loc[1], loc[2], 1 if is_carrying else 0)
    
    def shape(self):
        return (3, 3, 3, 2)
    
    def isDropoff(self, rlstate):
        return rlstate[3]
    
class SSSpace(RLSpace):
    """
    "Somewhat Simple" RL space: each agent's RL space contains only their coordinates, whether they hold a block,
    and the L1 distance to the other agent
    """
    def map_state(self, state, agent):
        loc = state.get_location(agent)
        other_loc = state.get_location('F' if agent == 'M' else 'M')
        is_carrying = state.is_agent_carrying(agent)
        return (loc[0], loc[1], loc[2], 1 if is_carrying else 0,
                # + 2?  shift range to start at 0 for use as index in qtable
                (loc[0] - other_loc[0]) + 2, 
                (loc[1] - other_loc[1]) + 2,
                (loc[2] - other_loc[2]) + 2)
    
    def shape(self):
        return (3, 3, 3, 2, 5, 5, 5)
    
    def isDropoff(self, rlstate):
        return rlstate[3] 
