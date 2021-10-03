from simulator.simulator import Simulator
from unittest.mock import patch, call, mock_open
import unittest
import numpy as np

class simulator(unittest.TestCase):

    @patch('simulator.simulator.Environment')
    @patch('simulator.simulator.Simulator.observe')
    def test_init_with_list_state(self, obs, env):
        sim = Simulator(env, np.array([]))
        obs.assert_called()
        self.assertFalse(sim._current_state is sim._initial_state)

    @patch('simulator.simulator.Environment')
    def test_render(self, env):
        sim = Simulator(env, np.array([]))
        sim.render()
        env.draw.assert_called()

    @patch('simulator.simulator.Environment')
    def test_reset(self, env):
        sim = Simulator(env, np.array([1]))
        sim.reset()
        self.assertEqual(sim._current_state, sim._initial_state)

    @patch('simulator.simulator.Environment')
    def test_step(self, env):
        env.get_next_state.return_value = np.array([2])
        sim = Simulator(env, np.array([1]))
        action = np.array([2])
        next_state = sim.step(action)
        # env.get_next_state.assert_called_with([(np.array([1]),
        #  action)])
        env.get_next_state.assert_called_with(np.array([1]), action)
        self.assertEqual(next_state, action)

    @patch('simulator.simulator.Environment')
    def test_observer(self, env):
        env.get_observation.return_value = np.array([2])
        sim = Simulator(env, np.array([1]))
        obs = np.array([2])
        ret_obs = sim.observe()
        env.get_observation.assert_called_with([np.array([1])])
        self.assertEqual(ret_obs, obs)

    @patch('simulator.simulator.Environment')
    @patch('simulator.simulator.Simulator.step')
    @patch('simulator.simulator.Simulator.observe')
    @patch('simulator.simulator.Simulator.render')
    def test_run(self, rdr, obs, stp, env):
        init_state = np.array([0])
        action = np.array([1])
        env.get_best_action.return_value = action
        obs.return_value = np.ones((1,4))
        stp.return_value = np.array([2])
        sim = Simulator(env, init_state)
        sim.run(steps=5, render=True)
        self.assertEqual(rdr.call_count, 6)
        self.assertEqual(env.get_best_action.call_count, 5)
        self.assertEqual(obs.call_count, 6)
        self.assertEqual(stp.call_count, 5)