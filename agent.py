import numpy as np
from action import Action
from policy import PGreedy, PExploit, PRandom

# Constant determining how often to prune the history the agents keep track of
MAX_HISTORY = 10
# Total possible actions available
ACTIONS = ['Pickup', 'Dropoff', 'N', 'S', 'E', 'W', 'U', 'D']

class Agent:
    def __init__(self, agent, rlstate, policy, init_state, alpha=0.5, gamma=0.5):
        """
        Constructor for generic agent.

        Arguments:
        agent - 'M' for male agent, 'F' for female agent
        rlstate - A RLState object which provides a mapping from the real-world state space to RL states
        policy - a Policy object, which provides a function that, given an RL state, returns an action
        init_state - The initial state of the world

        API:
        choose_action - agent takes current RW state, chooses an action and returns it
        update - agent updates RL state given new RW state and reward for last action
        set_policy - agent changes policy to passed policy
        """
        self.agent = agent
        self.actions = ACTIONS
        self.rlstate = rlstate
        self.policy = policy
        self.table = self._initialize_table()
        self.history = [[self.rlstate.map_state(init_state, self.agent), None, 0]]
        self.alpha = alpha
        self.gamma = gamma
        
    def _initialize_table(self):
        """
        Initialize the Q-table with 0s

        The Q-table currently is implemented as a dictionary indexed by action into ndarrays of the state space
        """
        shape = self.rlstate.shape()
        table = {}
        for a in self.actions:
            table[a] = np.zeros(shape)
        return table

    def choose_action(self, state):
        """
        Given the current state of the world, use policy to determine next action, and return that action
        """
        # TODO for now, this is requiring both Real-World and RL states, because Policy module needs to
        # determine whether an action is applicable even if that is impossible to know with just the RL state
        action_taken = self.policy.execute(state, self.rlstate.map_state(state, self.agent), self.table) # added self.agent arg to map_state call
        self.history[-1][1] = action_taken
        return action_taken

    def update(self, new_state, reward):
        """
        Updates the agent as needed, after an action is taken and reward is obtained
        Then run a Q-table update
        """
        self.history.append([self.rlstate.map_state(new_state, self.agent), None, 0])
        self.history[-2][2] = reward
        self._update_table()
        # TODO modify this for performance later?
        if len(self.history) > MAX_HISTORY:
            self._prune_history()

    def set_policy(self, policy):
        """
        Changes the agent's policy to a new policy
        """
        self.policy = policy

    def _update_table(self):
        """
        Given the current state space, use appropriate learning method to update the Q-table

        This method is intended to be overridden by subclasses that implement Q-learning or SARSA
        """
        return
    
    def _prune_history(self):
        """
        Reduce the size of the history that the agents keep, to avoid memory leaks
        """
        self.history = self.history[-2:]

class QLAgent(Agent):
    """
    A generic agent that uses Q-Learning to update its table
    """
    def _update_table(self):
        prev_step = self.history[-2]
        prev_state = prev_step[0]
        action = prev_step[1]
        reward = prev_step[2]
        new_state = self.history[-1][0]
        old_q = self.table[action][prev_state]
        best_next_action = None
        best_next_action_q = -2**32
        for ap in self.actions:
            if self.table[ap][new_state] > best_next_action_q:
                best_next_action = ap
                best_next_action_q = self.table[ap][new_state]
        self.table[action][prev_state] = (1-self.alpha)*old_q + self.alpha*(reward + self.gamma*best_next_action_q)

class SARSAAgent(Agent):
    """
    A generic agent that uses SARSA to update its table
    """
    def _update_table(self):
        prev_step = self.history[-2]
        prev_state = prev_step[0]
        action = prev_step[1]
        reward = prev_step[2]
        curr_step = self.history[-1]
        new_state = curr_step[0]
        next_action_taken = curr_step[1]
        old_q = self.table[action][prev_state]
        next_q = self.table[next_action_taken][new_state]
        self.table[action][prev_state] = (1-self.alpha)*old_q + self.alpha(reward + self.gamma*next_q)

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

class VSAgent(Agent):
    """
    Generic agent using Very Simple RL
    """
    def __init__(self, agent, policy, init_state, alpha=0.5, gamma=0.5):
        super().__init__(agent, VSSpace(), policy, init_state)

# Here are defined the basic agents used for testing:
# TODO implement more later

class VSQRandomAgent(VSAgent, QLAgent):
    """
    Agent using QL updates, Very Simple RL state space, and PRANDOM policy
    """
    def __init__(self, agent, init_state, alpha=0.5, gamma=0.5, seed=None):
        super(VSAgent, self).__init__(agent, None, init_state, alpha, gamma)
        self.set_policy(PRandom(agent, self.rlstate, self.actions, seed=seed))
