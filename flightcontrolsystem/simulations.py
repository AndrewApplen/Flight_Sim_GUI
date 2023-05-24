import random
from flightsimexception import FlightSimException
""" Simulators for each sensor """


#each instance of the simulation needs to be global to be
#accessed by program.  If the classes were instantiated elsewhere
#this would not be needed.  This simulation emulates hardware
#so this becomes an association/aggrigation
global tach1_
global tach2_
global compass_
global engTemp1_
global engTemp2_
global fuelL_
global fuelC_
global fuelR_
global airspeed_

global UPDATE_PERIOD
UPDATE_PERIOD = 200


class Simulator:
    """Base Class for all simulators"""

    def __init__(self,devID:str,initVal:float) -> None:
        """ all simulations will require a devID, the GUI ID of the 
        input 'device' as a string;
        and an initial value as a default output"""
        self.devID = devID
        self.value = initVal # default value

    def get_data(self,values:dict) -> float:
        """values is the dictionary of values of which the devID is the key
        Base Class Simulation just returns initVal from constructor
        Need to override to get simulated data"""
        return self.value

    
class Compass(Simulator):
    """Creates a random walk with bias for heading,
    Outputs a value between 0 and 359 degrees as an integer
    in the float output (for display purposes)"""

    # _value = 0

    def __init__(self, devID: str, initVal: float) -> None:
        super().__init__(devID, initVal)
        self.initVal = initVal

    def get_data(self, values:dict=None) -> float:
        """Creates the radom walk output with drift"""
        delta = random.random() - 0.5 + 0.1 #0.005 this is how fast compass drifts
        self.initVal = (self.initVal + delta + 360) %360
        return int(self.initVal)
    
    @classmethod
    def setCompass(cls, direction:int) -> None:
        cls.self.initVal = direction % 360


class DelaySim(Simulator):
    """Create a delay filter to cause a lag in the outputs"""
    def __init__(self, devID:str, initVal:float, outLow:float ,outHigh:float ,delay:int) -> None:
        super().__init__(devID, initVal)
        """devID is the device used for input with a range of 0 - 100
        initVal is the inital value of the output
        outLow and outHigh define the range of the output device
        delay is the delay in miliseconds"""
        self._delay = delay
        numback = self._delay//UPDATE_PERIOD # number of backvalues
        self.backvalues = [initVal] * numback
        self.slope = (outHigh - outLow) / 100.0
        self.offset = outLow / self.slope

    def get_data(self, values: dict) -> float:
        """uses the value found in the dictionary as the input"""
        val = ((values[self.devID]) - self.offset) * self.slope
        self.backvalues.pop(0)
        self.backvalues.append(val)
        self.value = (sum(self.backvalues)/len(self.backvalues))
        return self.value
    
    @property
    def delay(self):
        """gets current delay"""
        return self._delay
    
    @delay.setter
    def delay(self, new_delay:int):
        """sets new delay"""
        self._delay = new_delay
        numback = self._delay // UPDATE_PERIOD
        self.backvalues = [self.value] * numback


class Fuel(Simulator):
    """This is where the hardware would out put data
    in this case we fabricate the data that is output"""
    BURN_RATE = 0.002 #pounds per second takes into consideration the scale factors used

    def __init__(self, devID:str, initVal:float,devID2:str) -> None:
        super().__init__(devID,initVal)
        self.devID2 = devID2
        self.__total = initVal / 100

    def get_data(self, values:dict) -> float:
        self.__total = self.__total - (Fuel.BURN_RATE * ((values[self.devID] + values[self.devID2]) / 2))
        if self.devID2 is not None:
            self.__total = self.__total - (Fuel.BURN_RATE * values[self.devID2])
        self.__total = self.__total if self.__total > 0 else 0
        return self.__total
    
    @classmethod #changes burn rate
    def burnRate(cls, newRate:float):
        cls.BURN_RATE = newRate
    
    @property
    def total(self) -> float: # returns total amount of fuel in pounds
        return self.__total * 100
    
    @total.setter
    def total(self,total:int): #the new total amount of fuel(not just what was added)
        if total > 10000:
            self.__total = 10000/100
            raise FlightSimException("Fuel Overflow")
        else:
            self.__total = total/100 # apply scaling

    def __str__(self) -> str:
        return (f'FUEl LBS: {self.__total*100:.2f} | BURN RT: {self.BURN_RATE}')


class AirSpeed(DelaySim):
    """This is where the hardware would out put data
    in this case we fabricate the data that is output  refure to 
    DelaySim super class for full description"""
    def __init__(self, devID: str, initVal: float, outLow: float, outHigh: float, delay: int, devID2:str) -> None:
        super().__init__(devID, initVal, outLow, outHigh, delay)
        self.devID2 = devID2

    def get_data(self, values: dict) -> float:
        val = (((values[self.devID] + values[self.devID2]) / 2) - self.offset) * self.slope
        self.backvalues.pop(0)
        self.backvalues.append(val)
        self.value = (sum(self.backvalues)/len(self.backvalues))
        return self.value
    
    @property
    def delay(self):
        """gets current delay"""
        return self._delay
    
    @delay.setter
    def delay(self, new_delay:int):
        """sets new delay"""
        self._delay = new_delay
        numback = self._delay // UPDATE_PERIOD
        self.backvalues = [self.value] * numback
    

# create tach simulators
TACH_DELAY = 1500 #ms     
TACH_INITIAL = 600 #RPM 
TACH_LOW_RANGE = 0 
TACH_HIGH_RANGE = 3850.0 #RPM Max output 

tach1_ = DelaySim('-THR1-', TACH_INITIAL, TACH_LOW_RANGE, TACH_HIGH_RANGE, TACH_DELAY)
tach2_ = DelaySim('-THR2-', TACH_INITIAL, TACH_LOW_RANGE, TACH_HIGH_RANGE, TACH_DELAY)

#create temp simulators
TEMPR_DELAY = 10000 #ms 
TEMPR_INITIAL = 0.15 #volts 
TEMPR_LOW_RANGE = 0.0 #volts = - 30 degrees F 
TEMPR_HIGH_RANGE = 1.3 #volts = 250 degrees F 

engTemp1_ = DelaySim('-THR1-', TEMPR_INITIAL, TEMPR_LOW_RANGE, TEMPR_HIGH_RANGE, TEMPR_DELAY)
engTemp2_ = DelaySim('-THR2-', TEMPR_INITIAL, TEMPR_LOW_RANGE, TEMPR_HIGH_RANGE, TEMPR_DELAY)

#create fuel burn
INIT_CENTER = 9000
INIT_WING = 8000

fuelL_ = Fuel('-THR1-',INIT_WING ,'-THR2-')
fuelC_ = Fuel('-THR1-', INIT_CENTER, '-THR2-')
fuelR_ = Fuel('-THR1-', INIT_WING,'-THR2-')


#creates compass simulations
INIT_DIRECTION = 22
compass_ = Compass('-COMPASS-', INIT_DIRECTION)

#creates airspeed simulations
DELAY_SPD = 20000 #MS
INITIAL_SPD = 0 # NOT MOVING
LOW_RANGE_SPD = 0.31 #VOLTS OFFSET SO THROTTLE OF 10 HAS 0 MPH
HIGH_RANGE_SPD = 3.1 #VOLTS

airspeed_ = AirSpeed('-THR1-', INITIAL_SPD, LOW_RANGE_SPD, HIGH_RANGE_SPD, DELAY_SPD, '-THR2-')