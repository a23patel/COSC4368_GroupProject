import unittest
from agent import VSQRandomAgent
from cell import StateSpace

class TestAgent(unittest.TestCase):
    def test_initialize(self):
        """
        Tests that the agent initializes without error
        """
        state = StateSpace()
        agent1 = VSQRandomAgent('M', state, seed=420)
    
if __name__=='__main__':
    unittest.main()