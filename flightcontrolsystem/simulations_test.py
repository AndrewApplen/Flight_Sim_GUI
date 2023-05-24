import unittest
from flightcontrolsystem import simulations as sim

devID_t = "-TEST-"
initVal_t = 60
values_t = {devID_t : initVal_t}

result_t = 60

class TestSim_BaseClass(unittest.TestCase):
    ''' Tests the non-functional base class'''

    def test_init(self):
        test1 = sim.Simulator(devID_t,initVal_t)
        self.assertEqual(test1.devID, devID_t)

    def test_value(self):
        test2 = sim.Simulator(devID_t,initVal_t)
        self.assertEqual(test2.value, result_t)

    def test_update(self):
        test3 = sim.Simulator(devID_t,initVal_t)
        self.assertEqual(test3.get_data(values_t),result_t)

