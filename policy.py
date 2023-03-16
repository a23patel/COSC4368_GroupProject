from action import Action
import numpy as np

class Policy:
    def __init__(self, agent, states, actions, seed=None):
        """
        Constructor for SARSA/Q-Learning policy.
        This is a base class which will be specialized for the different epsilon-greedy policies

        Arguments:
        agent - 'M' for the male agent, 'F' for the female agent
        states - The RL state space being used
        actions - A list of actions that are available

        Properties:
        pi - The function executed to choose an action, given the current state and a Q table, intended to be overridden
        rng - A random number generator used for stochastic policies, which can be initialized with a prescribed seed
        """
        self.agent = agent
        self.states = states
        self.actions = actions
        # placeholder
        self.pi = None
        self.rng = np.random.default_rng(seed=seed)

    def execute(self, state, rlstate, table):
        """
        Execute the policy for one step, given current real world and RL states, and the Q table
        """
        return self.pi(state, rlstate, table)
    
    def is_applicable(self, state, action):
        """
        Returns True if the given action is applicable given the current state
        """
        # TODO this is going to get replaced with something in the Action module?
        a = Action()
        # Location of this agent
        loc = state.getLocation(self.agent)
        # Location of other agent
        oloc = state.getLocation('F' if self.agent == 'M' else 'M')
        # Status of agent TODO this does not match API
        is_carrying = state.isAgentCarrying(self.agent)
        is_in_pickup = state.isPickup(loc)
        is_in_dropoff = state.isDropoff(loc)
        # TODO purge this old code
        # other_agent_north = (loc[0] == oloc[0]) and (loc[1] == oloc[1] - 1) and (loc[2] == oloc[2])
        # other_agent_south = (loc[0] == oloc[0]) and (loc[1] == oloc[1] + 1) and (loc[2] == oloc[2])
        # other_agent_east = (loc[0] == oloc[0] - 1) and (loc[1] == oloc[1]) and (loc[2] == oloc[2])
        # other_agent_west = (loc[0] == oloc[0] + 1) and (loc[1] == oloc[1]) and (loc[2] == oloc[2])
        # other_agent_up = (loc[0] == oloc[0]) and (loc[1] == oloc[1]) and (loc[2] == oloc[2] - 1)
        # other_agent_down = (loc[0] == oloc[0]) and (loc[1] == oloc[1]) and (loc[2] == oloc[2] + 1)
        # can_north = loc[1] != 2
        # can_south = loc[1] != 0
        # can_west = loc[0] != 0
        # can_east = loc[0] != 2
        # can_up = loc[2] != 2
        # can_down = loc[2] != 0
        if action == 'Pickup':
            return not is_carrying and is_in_pickup
        elif action == 'Dropoff':
            return is_carrying and is_in_dropoff
        # TODO purge this old code
        # elif action == 'North':
        #     return can_north and not other_agent_north
        # elif action == 'S':
        #     return can_south and not other_agent_south
        # elif action == 'W':
        #     return can_west and not other_agent_west
        # elif action == 'E':
        #     return can_east and not other_agent_east
        # elif action == 'U':
        #     return can_up and not other_agent_up
        # elif action == 'D':
        #     return can_down and not other_agent_down
        elif action == 'N':
            return a.isNorthApplicable(loc, state)
        elif action == 'S':
            return a.isSouthApplicable(loc, state)
        elif action == 'W':
            return a.isWestApplicable(loc, state)
        elif action == 'E':
            return a.isEastApplicable(loc, state)
        elif action == 'U':
            return a.isUpApplicable(loc, state)
        elif action == 'D':
            return a.isDownApplicable(loc, state)

    def get_applicable_actions(self, state):
        """
        Returns an list of actions applicable in the given state
        """
        return list(filter(lambda action: self.is_applicable(state, action), self.actions))

class PRandom(Policy):
    """
    The PRANDOM policy: at any point, choose uniform random action from available actions
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pi = lambda s, _: self.random(s)

    def random(self, state):
        valid_actions = self.get_applicable_actions(state)
        if 'Pickup' in valid_actions:
            return 'Pickup'
        elif 'Dropoff' in valid_actions:
            return 'Dropoff'
        else:
            return self.rng.choice(valid_actions)
        
class PGreedy(Policy):
    """
    The PGREEDY policy: always choose the available action leading to the highest possible Q value from the given state
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pi = lambda s, rs, qs: self.greedy(s, rs, qs)

    def greedy(self, state, rlstate, table):
        valid_actions = self.get_applicable_actions(state)
        if 'Pickup' in valid_actions:
            return 'Pickup'
        elif 'Dropoff' in valid_actions:
            return 'Dropoff'
        else:
            best_q = -2**32
            best_a = None
            for action in valid_actions:
                this_q = table[action][rlstate]
                if this_q > best_q:
                    best_q = this_q
                    best_a = action
            return best_a

class PExploit(PRandom, PGreedy):
    """
    The PEXPLOIT policy: randomly perform PGREEDY 80% of the time, and PRANDOM 20% of the time.
    """
    def __init__(self, *args, **kwargs):
        super(PRandom, self).__init__(*args, **kwargs)
        self.pi = lambda s, rs, qs: self.exploit(s, rs, qs)

    def exploit(self, state, rlstate, table):
        if self.rng.random() >= 0.8:
            return self.random(state)
        else:
            return self.greedy(state, rlstate, table)