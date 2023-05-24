""" Displays for the Cockpit Simulation System """
from typing import Callable     #used for a parameter
from flightsimexception import FlightSimException
from sensors import *


class Display:
    """This is the base class from which all of our displays will be derived."""

    def __init__(self, guiUpdate:Callable) -> None:
        self.gui = guiUpdate

    def update(self,value:float):
        self.gui(value)

    @staticmethod
    def validate_range(value:int) -> bool:
        return 1 <= value <= 100


class Bar(Display):
    """yeah, this does the things where data is displayed on the progress bar 
    of the GUI GUI"""
    def __init__(self, guiUpdate:Callable, caution:int, warn:int, limit_switch:int) -> None:
        super().__init__(guiUpdate)
        self.caution = caution
        self.warn = warn
        self.limit_switch = limit_switch
        self.state = 'safe'

    def update(self, value:int):
        self.gui(value)


class TachBar(Bar):
    """yeah, this does the things where data is displayed on the progress bar 
    of the GUI GUI"""
    def update(self, value:int):
        self.gui(value)
        match self.state:
            case 'safe':
                if value >= 80:
                    self.state = 'yellow'
                    raise FlightSimException('Engine RPM is YELLOW')
            case 'yellow':
                if value > 90:
                    self.state = 'redline'
                    raise FlightSimException('Engine RPM is REDLINE')
            case 'redline':
                if value < 80:
                    self.state = 'safe'
                    raise FlightSimException('Engine RPM good chief!')
            case _:
                raise FlightSimException('Flight computer error 828abc')


class Fuel_Level(Display):
    """This is nice, again there will not be a need to make any changes to the code,
      but do create the Fuel_Level class, as it will be expanded in the future. """
    def __init__(self, guiUpdate:Callable) -> None:
        super().__init__(guiUpdate)
        self.state = 'safe'

    def update(self,value:float):
        self.gui(value)
        match self.state:
            case 'safe':
                if not Display.validate_range(value):
                    self.state = 'caution'
                    raise FlightSimException('It aint got no gas')
            case 'caution':
                if Display.validate_range(value):
                    self.state = 'safe'
                    raise FlightSimException('Fuel Tank Low')
            case _:
                raise FlightSimException('Flight computer error 223')
                

class CompassDisp(Display):
    """This is where the the display gets updated to the gui"""

    def __init__(self, guiUpdate:Callable, guiUpdate2:Callable) -> None:
        """constructor for compass disp"""
        self.guiUpdate = guiUpdate
        self.guiUpdate2 = guiUpdate2

    def update(self, value:float):
        """checks compass values to update compass
        direction and comapass cardinal"""
        self.guiUpdate(value)
        comp_points = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']
        if value >= 337.5 or value < 22.5:
            self.guiUpdate2(comp_points[0])
        elif value < 67.5:
            self.guiUpdate2(comp_points[1])
        elif value < 112.5:
            self.guiUpdate2(comp_points[2])
        elif value < 157.5:
            self.guiUpdate2(comp_points[3])
        elif value < 202.5:
            self.guiUpdate2(comp_points[4])
        elif value < 247.5:
            self.guiUpdate2(comp_points[5])
        elif value < 292.5:
            self.guiUpdate2(comp_points[6])
        else:
            self.guiUpdate2(comp_points[7])


class AirspeedDisp(Display):
    """Updates the airspeed GUI and sends errors to the 
    flight computer.  Depending on the speed errors are displayed
    to reflect."""
    def __init__(self, guiUpdate:Callable, caution:int, warn:int, limit_switch:int) -> None:
        super().__init__(guiUpdate)
        self.caution = caution
        self.warn = warn
        self.limit_switch = limit_switch
        self.state = 'safe'

    def update(self, value:int):
        self.gui(value)
        match self.state:
            case 'safe':
                if value > 310:
                    self.state = 'caution'
                    raise FlightSimException('Caution: Airspeed too high')
            case 'caution':
                if value < 310:
                    self.state = 'safe'
                    raise FlightSimException('Airspeed is normal')
                elif value > 375:
                    self.state = 'warning'
                    raise FlightSimException('Warning: Airspeed WAY too high')
            case 'warning':
                if value < 375:
                    self.state = 'caution'
                    raise FlightSimException('Caution: Airspeed too high')
                elif value > 450:
                    self.state = 'redline'
                    raise FlightSimException('AIRSPEED IS BEYOND REDLINE')
            case 'redline':
                if value < 450:
                    self.state = 'warning'
                    raise FlightSimException('Warning: Airspeed way too high')
            case _:
                raise FlightSimException('Flight computer error 550')