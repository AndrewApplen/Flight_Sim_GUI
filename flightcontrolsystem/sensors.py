""" The Sensors class is often called a wrapper which
provides a common software intface to different types
of hardware sensors.  Each type of device will currently
connect to a simulator, but in the near future they will
individually connect to hardware
 """

from simulations import Simulator

class Sensors:
    """This is the base class from which all of our sensors will be derived,
    so it has little functionality other than being a common definition 
    for the interface """
    
    def __init__(self, sim:Simulator) -> None:
        """This parameter is the instance
          of the simulator class that 
          provides the data. """
        self.sim = sim

    def read_sensor(self, values:dict) -> float:
        """takes in parameter as dict of values from event loop and 
        returns a value obtained """
        return self.sim.get_data(values)


class Tach_sensor(Sensors):
    """calculates tach values to be displayed"""
    def read_sensor(self, values:dict) -> float:
        TACH_SCALE_FACTOR = 0.025
        return self.sim.get_data(values) * TACH_SCALE_FACTOR
    

class Tempr_sensor(Sensors):
    """calculates tempr values to be displayed"""
    def read_sensor(self, values: dict) -> float:
        TEMPR_SCALE_FACTOR = 75.0/1.3
        OFFSET = -20.0
        return (self.sim.get_data(values) * TEMPR_SCALE_FACTOR) - OFFSET
    

class Fuel_sensor(Sensors):
    """The fuel sensor will use hardware in the future, so a class needs to 
    be constructed as a placeholder now.  This is about as simple as can be,
      there are presently no changes to the constructor or read_sensor(). """

    def read_sensor(self, values: dict) -> float:
        return super().read_sensor(values)
    
    @staticmethod
    def pounds_to_gallons(pounds:float):
        gallons = pounds / 6.5
        return gallons
        
    
class Compass_sensor(Sensors):
    """ The compass sensor will use hardware in the future, but for now it is
    just a place holder"""
    
    def read_sensor(self, values: dict) -> float:
        return super().read_sensor(values)
    

class Airspeed_sensor(Sensors):
    """Does simple conversion for what the scale factor is to calculate
    aispeed from 0 to 550mph aprox."""
    def read_sensor(self, values: dict) -> float:
        NO_SPEED = 0
        AIRSPEED_SCALE_FACTOR = 550.0/2.79
        speed = int(self.sim.get_data(values) * AIRSPEED_SCALE_FACTOR)
        if speed < NO_SPEED:
            return NO_SPEED
        else:
            return speed


if __name__=='__main__':
    gallons = Fuel_sensor.pounds_to_gallons(7500.00)
    print(gallons)

