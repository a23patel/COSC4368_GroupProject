import numpy as np

class Agent:
    def __init__(self, actions, policy):
        """
        Constructor for SARSA/Q-Learning agent.

        Arguments:
        actions - a list of possible actions which the agent can perform
        policy - a Policy object, which provides a function that, given a state, returns an action
        """
        self.actions = actions
        self.policy = policy
        # TODO initialize Q-table as 0s for interactive learning
        self.table = None
        self.last_action = None
        

    def choose_action(self, state):
        """
        Given the current state space, use policy to determine next action, and return that action
        """
        action_taken = self.policy.execute(state, self.table)
        self.last_action = action_taken
        return action_taken

    def update_table(self, state):
        """
        Given the current state space, use appropriate learning method to update the Q-table
        """
        # TODO implement: use self.last_action to use temporal update to Q-table
        return

class Policy:
    def __init__(self, states, actions, seed=None):
        """
        Constructor for SARSA/Q-Learning policy.
        This is a base class which will be specialized for the different epsilon-greedy policies utilized in this experiment
        """
        self.states = states
        self.actions = actions
        # placeholder
        self.pi = None
        self.rng = np.random.default_rng(seed=seed)

    def execute(self, state, table):
        """
        Execute the policy for one step, given current state and the Q table
        """
        return self.pi(state, table)
    
    def is_applicable(self, state, action):
        """
        Returns True if the given action is applicable
        """
        # TODO implement
        return True


    def get_applicable_actions(self, state):
        """
        Returns an list of actions applicable in the given state
        """
        return list(filter(lambda action: self.is_applicable(state, action), self.actions))

    
class PRandom(Policy):
    def __init__(self, *args):
        super().__init__(*args)
        self.pi = lambda s, _: self.random(s)

    def random(self, state):
        if state == 'pickup':
            return 'pickup'
        elif state == 'dropoff':
            return 'dropoff'
        else:
            valid_actions = self.get_applicable_actions(state)
            action_taken = self.rng.choice(valid_actions)
            return action_taken
        
class PGreedy(Policy):
    def __init__(self, *args):
        super().__init__(*args)
        self.pi = lambda s, qs: self.greedy(s, qs)

    def greedy(self, state, table):
        # TODO flesh out this sketch
        if state == 'pickup':
            return 'pickup'
        elif state == 'dropoff':
            return 'dropoff'
        else:
            valid_actions = self.get_applicable_actions(state)
            # TODO implement choose greedy option
            return None

class PExploit(PRandom, PGreedy):
    def __init__(self, *args):
        super(PRandom, self).__init__(*args)
        self.pi = lambda s, qs: self.exploit(s, qs)

    def exploit(self, state, table):
        """
        PEXPLOIT is just PGREEDY 80% of the time, and PRANDOM 20% of the time
        """
        if state == 'pickup':
            return 'pickup'
        elif state == 'dropoff':
            return 'dropoff'
        else:
            use_random = self.rng.random() > 0.8
            if use_random:
                return self.random(state)
            else:
                return self.greedy(state, table)