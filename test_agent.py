import unittest
from agent import VSQRandomAgent, VSQGreedyAgent
from stateSpace import StateSpace

class TestAgent(unittest.TestCase):
    def test_initialize(self):
        """
        Tests that the agent initializes without error
        """
        state = StateSpace('original')
        agent1 = VSQRandomAgent('M', state, seed=420)

    def test_random(self):
        """
        Testing the behavior of a random agent: it should choose uniformly from available actions.
        """
        state = StateSpace('original')
        agent1 = VSQRandomAgent('F', state, seed=167)
        valid_actions = agent1.policy.get_applicable_actions(state)
        hist = {}
        for action in valid_actions:
            hist[action] = 0
        # We let the agent choose actions randomly
        for t in range(1000):
            hist[agent1.choose_action(state)] += 1

        for action in valid_actions:
            self.assertGreater(hist[action], 0)
        
        print(hist)

    # def test_greedy(self):
    #     state = StateSpace('original')
    #     agent1 = VSQGreedyAgent('F', state, seed=167)
        
    
if __name__=='__main__':
    unittest.main()