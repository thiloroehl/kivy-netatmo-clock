from kivy.app import App
from kivy.clock import Clock
from kivy.core.text import LabelBase
from kivy.core.window import Window
from kivy.utils import get_color_from_hex
import time
import lnetatmo
import traceback
import socket
import os
import struct

from time import strftime


class ClockApp(App):
    debug=False
    ip="x.x.x.x"
    sw_started = False
    sw_seconds = 0
    ipfetched=False

    def on_start(self):
        Clock.schedule_interval(self.update, 5)

    def update(self, nap):
        if self.sw_started:
            self.sw_seconds += nap

        
        print("Calling Netatmo at "+strftime('%H:%M:%S'))
        # Device-Liste von Netatmo abholen
        try:
            
            
            authorization = lnetatmo.ClientAuth()
            devList = lnetatmo.DeviceList(authorization)
            print("Connected to Netatmo")
            # Funktionen um die ID von Modulen und Device zu ermitteln
            print("DeviceList ")
            print(devList.modulesNamesList())
            # Niederschlag ist der Modulname meines Regenmessers
            print("GardenTemp ")
            print(devList.moduleByName('GardenTemp'))
            print("--")
            print("GardenRain ")
            print(devList.moduleByName('GardenRain'))

 
 
 
            ## Ermittlung der aktuellen Wetterdaten ---------------------------------------------
 
            # Aktuelle Aussentemperatur ausgeben
            print("GardenTemperature ")
            gardentemp=devList.lastData()['GardenTemp']['Temperature']
            print("GardenTemperature called.")
            print (gardentemp)
        
            # Wetterdaten des Vortages ermitteln: -----------------------------------------------
            now = time.time()               # Von Jetzt
            start = now - 2* 24 * 3600

            #Ermittlung der Temperaturen als Liste
            resp = devList.getMeasure( device_id='70:ee:50:17:4e:dc',      
                           module_id='02:00:00:17:d9:24',    
                           scale="1day",
                           mtype="min_temp,max_temp",
                           date_begin=start,
                           date_end=now)
 
            # Extraieren von Zeit, minTemp und Maxtemp
            result = [(int(k),v[0],v[1]) for k,v in resp['body'].items()]
            # Liste sortieren (nach Zeit, da erstes Element)
            result.sort()
        
            messdatum = time.localtime(result[0][0])
            #Ermittlung des Datums des Vortages der Min/Max Temperaturen vom Vortag
            messdatum = time.localtime(result[0][0])
 
            #Ermittlung der Min- und Max-Temperaturen des Vortages
            last_temp_min = result[0][1]
            last_temp_max = result[0][2]

            
            self.root.ids.time.text = strftime('[b]%H:%M[/b]:%S')+"   {:.2f}°C".format(devList.lastData()['GardenTemp']['Temperature'])    
            self.root.ids.outsidetemp.text = "{:.2f}°C".format(devList.lastData()['GardenTemp']['min_temp']) +" - {:.2f}°C".format(devList.lastData()['GardenTemp']['max_temp'])+"    Vortag: "+" {:.2f}°C".format(last_temp_min) + " - {:.2f}°C".format(last_temp_max)
            
            rain=devList.lastData()['GardenRain']['Rain']
            sumrain24=devList.lastData()['GardenRain']['Rain']
            
            if rain > 0 or sumrain24 > 0 :
                self.root.ids.humidity.text="Feuchtigkeit {:.2f}%".format(devList.lastData()['GardenTemp']['Humidity'])+"Regen {:.2f}".format(devList.lastData()['GardenRain']['Rain'])+"- 24h {:.2f}".format(devList.lastData()['GardenRain']['Rain'])
            else:
                self.root.ids.humidity.text="Feuchtigkeit {:.2f}%".format(devList.lastData()['GardenTemp']['Humidity'])
                
            #m, s = divmod(self.sw_seconds, 60)
            #           self.root.ids.stopwatch.text = ('%02d:%02d.[size=40]%02d[/size]' %
            #                                      (int(m), int(s), int(s * 100 % 100)))
        except IOError as e :
            print ("IO Error ")
        except :
            print("Error occured")
            print (traceback.format_exc())
        
        print("Everything okay")
        if self.debug:
            if self.ipfetched: 
                self.root.ids.status.text="Netatmo called at - "+strftime('%H:%M:%S') + "- IP {0}".format(self.ip)
            else:
                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                s.connect(("8.8.8.8", 80))
                self.ip= s.getsockname()
                self.ipfetched=True
                
    
    def reset(self):
        if self.sw_started:
            self.root.ids.start_stop.text = 'Start'
            self.sw_started = False

        self.sw_seconds = 0
    
    def restart(self):
        print ("Restarting..")
    
    def start_debug(self):
        print ("Enter debug mode")
        self.debug=True
    
    def testme(self):
        print ("Testing")
    
    

if __name__ == '__main__':
    Window.clearcolor = get_color_from_hex('#101216')
    LabelBase.register(name='Roboto',
                       fn_regular='Roboto-Light.ttf',
                       fn_bold='Roboto-Medium.ttf')

            
    ClockApp().run()
