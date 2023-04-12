import numpy as np
import random
import copy
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
        learning - the learning type, either 'ql' or 'sarsa'
        init_state - The initial state of the world, a StateSpace object
        alpha - The learning rate
        gamma - The discounting factor for future Q values

        API:
        choose_action - agent takes current RW state, chooses an action and returns it
        update - agent updates RL state given new RW state and reward for last action
        set_policy - agent changes policy to passed policy
        set_learning - agent changes learning method
        """
        self.agent = agent
        self.actions = ACTIONS
        self.rlstate = rlstate
        self.policy = policy
        self.seed = self.policy.seed
        self.learning = 'ql'
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

    def set_learning(self, learning):
        """
        Change the agent's learning method to a new method
        """
        self.learning = learning

    def _update_table(self):
        """
        Given the current state space, use appropriate learning method to update the Q-table
        """
        if self.learning == 'sarsa' and len(self.history) > 2:
            self._update_table_sarsa()
        elif self.learning == 'ql':
            self._update_table_ql()
    
    def _update_table_ql(self):
        """
        Updates Q-tablet using Q-learning
        """
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

    def _update_table_sarsa(self):
        """
        Updates Q-table using SARSA
        """
        prev_step = self.history[-3]
        prev_state = prev_step[0]
        action = prev_step[1]
        reward = prev_step[2]
        curr_step = self.history[-2]
        new_state = curr_step[0]
        next_action_taken = curr_step[1]
        old_q = self.table[action][prev_state]
        next_q = self.table[next_action_taken][new_state]
        self.table[action][prev_state] = (1-self.alpha)*old_q + self.alpha*(reward + self.gamma*next_q)

    def _prune_history(self):
        """
        Reduce the size of the history that the agents keep, to avoid memory leaks
        """
        self.history = self.history[-2:]

    def extract_table(self, state):
        """
        Extract the Q-table state at the present for the agent, in the form suitable for history.
        The format uses a (3,3,3) matrix encoding the direction and strength of the action with strongest Q value of the agent at that space,
        for the current RL state space information regarding the location of the other agent, block carrying status, and state of the rest of the world
        """
        strength = [0] * 27
        moves = ['' for i in range(27)]
        for i in range(3):
            for j in range(3):
                for k in range(3):
                    state.update_agent_loc(self.agent, (i,j,k))
                    actions = copy.deepcopy(self.actions)
                    random.shuffle(actions)
                    cur_rlstate = self.rlstate.map_state(state, self.agent)
                    max_q = 0
                    max_act = ''
                    for a in actions:
                        temp = self.table[a][cur_rlstate]
                        if temp > max_q:
                            max_q = temp
                            max_act = a
                    strength[i*9 + j*3 + k] = max_q
                    moves[i*9 + j*3 + k] = max_act
        return (strength, moves)
