#!python3
# """ OOP demo/exercise project for 1D731Z class """
import PySimpleGUI as sg
import simulations
from simulations import *
from sensors import *
from displays import *
from flightsimexception import FlightSimException

class FlightSim():
    """This class encapsulates the GUI for the application"""
   
    #The landing gear display is not a standard element within PySimpleGUI
    #So this is a placeholder until a class is created for this Element
    #These variables are needed in the initializer and run() method  
    lg_disp = None
    lg_nose = None
    lg_left = None
    lg_right = None

    def __init__(self) -> None:
        
        #GUI Definition and Layout
        sg.theme('DarkAmber')

        # our instance variables
        self.window = None
        self.dash = []        

        airspeed_frame = sg.Frame('Air Speed',
                [[sg.Push(),sg.Text('0', size = (3,2),font='Calibri 36 bold',justification='right',
                key='-AIRSPEED-'),sg.Push()]],size=(100,150))

        engine_temp_frame = sg.Frame('Engine Temp',
                [[sg.Push(), sg.ProgressBar(100,'v',(11,10), key='-ET1-'),
                sg.ProgressBar(100,'v',(11,10), key='-ET2-'), sg.Push()]],size=(90,150))

        compass_frame = sg.Frame('Compass',
                [[sg.Push(),sg.Text('359', size = (3,1),font='Calibri 36 bold',
                    justification='center', key='-COMPASS-'),sg.Push()],
                [sg.Push(),sg.Text('N', size = (3,1),font='Calibri 24 bold',
                    justification='center', key='-DIR-'),sg.Push()]],
                size=(100,150))

        tachometer_frame = sg.Frame('Tachometer',
                [[sg.Push(), sg.ProgressBar(100,'v',(11,10), key='-TACH1-'),
                sg.ProgressBar(100,'v',(11,10), key='-TACH2-'), sg.Push()]],size=(90,150))

        throttle_frame = sg.Frame('Throttle',
                [[sg.Slider(range=(0,100),default_value=10,orientation='v',size=(7,12),key='-THR1-'),
                sg.Slider(range=(0,100),default_value=10,orientation='v',size=(7,12), key='-THR2-'), sg.Push()]])

        landing_gear_frame = sg.Frame('Landing Gear',
                [[sg.Push(),sg.Button('UP',key='-UP-'),sg.Push()],
                [sg.Graph(canvas_size=(80,50), graph_bottom_left=(0,0),graph_top_right=(80,50),
                    background_color='gray', key='-LG_DISP-')],
                [sg.Push(),sg.Button('DN',key='-DN-'),sg.Push()]])

        fuel_guage_frame = sg.Frame('Fuel',
                [[sg.Push(),sg.Text('Left'),sg.ProgressBar(100,'h',(10,5),key=('-FUELLEFT-'))],
                [sg.Push(),sg.Text('Center'),sg.ProgressBar(100,'h',(10,5),key=('-FUELCENTER-'))],
                [sg.Push(),sg.Text('Right'),sg.ProgressBar(100,'h',(10,5),key=('-FUELRIGHT-'))]],size=(200,110))

        flight_computer_frame = sg.Frame('Flight Computer',
                [[sg.Multiline('Status: Power up normal\n',size=(25,20),key='-COMPUTER-')]],size=(200,200))

        layout = [[sg.Text('Air Force POOP Drone Flight Simulator')],
                [sg.HorizontalSeparator()],
                [sg.Push(),airspeed_frame,engine_temp_frame,tachometer_frame,fuel_guage_frame,compass_frame,sg.Push()],
                [sg.HorizontalSeparator()],
                [sg.Push(),throttle_frame,flight_computer_frame,landing_gear_frame,sg.Push()],
                [sg.Exit(),sg.Button('Refuel',key='-REFUEL-'),sg.Button('Set North',key='-NORTH-')]]

        #create the main window
        self.window = sg.Window('AF POOP Drone Simulator', layout, size=(650,450),finalize=True)
        #get the canvas and give it an identifier which can be used by graphing tools
        #to create a custom landing gear display
        FlightSim.lg_disp = self.window['-LG_DISP-']
        FlightSim.lg_left = FlightSim.lg_disp.DrawCircle((18,25),8, fill_color='green',line_color='green')
        FlightSim.lg_nose = FlightSim.lg_disp.DrawCircle((40,25),8, fill_color='green',line_color='green')
        FlightSim.lg_right = FlightSim.lg_disp.DrawCircle((62,25),8, fill_color='green',line_color='green')

        '''attach either hardware or a simulator to the sensor
        and configure the display for the sensor
        note, this requires the simulators to be defined as global
        V     V     V     V     V     V     V     V     V     V     V'''

        tach1_sens = Tach_sensor(simulations.tach1_)
        tach1_disp = TachBar(self.window['-TACH1-'].update,875,850,990)
        tach2_sens = Tach_sensor(simulations.tach2_)
        tach2_disp = TachBar(self.window['-TACH2-'].update,875,850,990)

        comp_sens = Compass_sensor(simulations.compass_)
        comp_disp = CompassDisp(self.window['-COMPASS-'].update, self.window['-DIR-'].update)

        engTemp1_sens = Tempr_sensor(simulations.engTemp1_)
        engTemp1_disp = Bar(self.window['-ET1-'].update,875,850,990)
        engTemp2_sens = Tempr_sensor(simulations.engTemp2_)
        engTemp2_disp = Bar(self.window['-ET2-'].update,875,850,990)

        fuelL_sens = Fuel_sensor(simulations.fuelL_)
        fuelL_disp = Fuel_Level(self.window['-FUELLEFT-'].update)
        fuelC_sens = Fuel_sensor(simulations.fuelC_)
        fuelC_disp = Fuel_Level(self.window['-FUELCENTER-'].update)
        fuelR_sens = Fuel_sensor(simulations.fuelR_)
        fuelR_disp = Fuel_Level(self.window['-FUELRIGHT-'].update)

        airspeed_sens = Airspeed_sensor(simulations.airspeed_)
        airspeed_disp = AirspeedDisp(self.window['-AIRSPEED-'].update,875,850,990)

        #appends values to dash list to be displayed
        self.dash.append((tach1_sens,tach1_disp))
        self.dash.append((tach2_sens,tach2_disp))

        self.dash.append((engTemp1_sens,engTemp1_disp))
        self.dash.append((engTemp2_sens,engTemp2_disp))

        self.dash.append((fuelL_sens,fuelL_disp))
        self.dash.append((fuelC_sens,fuelC_disp))
        self.dash.append((fuelR_sens,fuelR_disp))

        self.dash.append((comp_sens,comp_disp))

        self.dash.append((airspeed_sens,airspeed_disp))

        # the entire dashboard pairs the sensor to the display and stores
        # the respective methods as a list of tuples


    def run(self):

        #Event loop to run the program
        while True:
            try:
                # the event loop frequency is set in the simulation
                event, values = self.window.read(timeout=simulations.UPDATE_PERIOD)
                #print(event,'====', values)
                if event == sg.WIN_CLOSED or event == 'Exit':
                    break
                if event == '-REFUEL-':
                    simulations.fuelC_.total += 750
                if event == '-NORTH-':
                    simulations.compass_.initVal = 0 #sets compass to North
                    raise FlightSimException('North is set')
                if event == '-UP-':
                    Fuel.burnRate(0.001) #changes Fuel BURN_RATE when UP is pressed
                    raise FlightSimException('Landing Gear Up')
                if event == '-DN-':
                    Fuel.burnRate(0.002) #changes Fuel BURN_RATE when DN is pressed
                    raise FlightSimException('Landing Gear Down')
                #read the sensors and update the displays
                for sen,disp in self.dash:
                    disp.update(sen.read_sensor(values))
            except FlightSimException as e:
                self.window['-COMPUTER-'].print(e)
            print(simulations.fuelC_)#prints fuel level
        self.window.close()

if __name__ == "__main__":
    """Creates the primary GUI display and runs the event loop"""
    fs = FlightSim()
    fs.run()
