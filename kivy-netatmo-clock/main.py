from kivy.app import App
from kivy.clock import Clock
from kivy.core.text import LabelBase
from kivy.core.window import Window
from kivy.utils import get_color_from_hex
import lnetatmo


from time import strftime


class ClockApp(App):
    sw_started = False
    sw_seconds = 0

    def on_start(self):
        Clock.schedule_interval(self.update, 5)

    def update(self, nap):
        if self.sw_started:
            self.sw_seconds += nap

        self.root.ids.time.text = strftime('[b]%H:%M[/b]:%S')
        print("Calling Netatmo at "+strftime('%H:%M:%S'))
        # Device-Liste von Netatmo abholen
        try:
            authorization = lnetatmo.ClientAuth()
            devList = lnetatmo.DeviceList(authorization)
 
 
 
            ## Ermittlung der aktuellen Wetterdaten ---------------------------------------------
 
            # Aktuelle Aussentemperatur ausgeben
            gardentemp=devList.lastData()['GardenTemp']['Temperature']
            print (gardentemp)
            self.root.ids.outsidetemp.text = "Aussen {:.2f}°C".format(gardentemp)+ " - Min {:.2f}".format(devList.lastData()['GardenTemp']['min_temp']) +" Max {:.2f}".format(devList.lastData()['GardenTemp']['max_temp']) 
            self.root.ids.humidity.text=" Humidity {:.2f}".format(devList.lastData()['GardenTemp']['Humidity'])
        
            m, s = divmod(self.sw_seconds, 60)
            #        self.root.ids.stopwatch.text = ('%02d:%02d.[size=40]%02d[/size]' %
            #                                        (int(m), int(s), int(s * 100 % 100)))
        except:
            print("Error occured")

    def start_stop(self):
        self.root.ids.start_stop.text = 'Start' if self.sw_started else 'Stop'
        self.sw_started = not self.sw_started

    def reset(self):
        if self.sw_started:
            self.root.ids.start_stop.text = 'Start'
            self.sw_started = False

        self.sw_seconds = 0

if __name__ == '__main__':
    Window.clearcolor = get_color_from_hex('#101216')
    LabelBase.register(name='Roboto',
                       fn_regular='Roboto-Thin.ttf',
                       fn_bold='Roboto-Medium.ttf')
    ClockApp().run()
