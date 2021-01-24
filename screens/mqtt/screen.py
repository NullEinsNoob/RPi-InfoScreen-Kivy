from kivy.app import App

from datetime import datetime
import time

from kivy.properties import DictProperty
from kivy.clock import Clock

from kivy.properties import StringProperty
import paho.mqtt.client as mqtt

from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen


class Drawer(Screen):

    tempIn = StringProperty("")
    tempOut = StringProperty("")

    timedata = DictProperty({})
    
    def __init__(self, **kwargs):
        self.get_time()
        #super(Drawer, self).__init__(**kwargs)
        super(Drawer, self).__init__()
        self.name="mqtt"	

        self.timer = None
        self.on_start()
        
    def get_time(self):
        """Sets self.timedata to current time."""
        n = datetime.now()
        self.timedata["h"] = n.hour
        self.timedata["m"] = n.minute
        self.timedata["s"] = n.second
        
    def update(self, dt):
        self.get_time()

    def on_enter(self):
        # We only need to update the clock every second.
        self.timer = Clock.schedule_interval(self.update, 1)

    def on_pre_enter(self):
        self.get_time()

    def on_pre_leave(self):
        # Save resource by unscheduling the updates.
        Clock.unschedule(self.timer)


    def floodOn(self):
        mqttc.publish("rf/light", "1069077")

    def floodOff(self):
        mqttc.publish("rf/light", "1069076")

    def lamp2On(self):
	#print "Lampe 2 Ein"
        mqttc.publish("sonoff-winter/cmnd/power", "ON")

    def lamp2Off(self):
	#print "Lampe 2 Aus"
        mqttc.publish("sonoff-winter/cmnd/power", "OFF")

    def lamp3On(self):
        print("Lampe 3 Ein")

    def lamp3Off(self):
        print("Lampe 3 Aus")

    def on_start(self):
        print("On Start")
        MQTT_SERVER = "localhost"
        MQTT_PATH = "/esp/bme280/"
        INNER = "Inner/get/"
        OUTER = "Outer/get/"
        TEMP = "temperature"
        HUM = "humidity"
        PRESS = "pressure"

        #topic = "rf/light"
	#cmnd = "/cmnd/power"

        ON = "1069077"
        OFF = "1069076"

        def onConnect(client, userdata, flags, rc):
            #print("Connected with result code "+str(rc))
            if rc == 0:
                client.connected_flag=True #set flag
                mqttc.subscribe(MQTT_PATH + INNER + TEMP, 0)
                mqttc.subscribe(MQTT_PATH + OUTER + TEMP, 0)
	        
        def onMessage(client, userdata, msg):
            msg.payload = msg.payload.decode("utf-8")
            print ("[INFO   ] [MQTT        ] topic: " + msg.topic +" msg: "+ msg.payload)
            
            if msg.topic == (MQTT_PATH + INNER + TEMP):
                userdata['self'].tempIn = msg.payload
		
            if msg.topic == (MQTT_PATH + OUTER + TEMP):
                userdata['self'].tempOut = msg.payload

        mqtt.Client.connected_flag=False#create flag in class
        parameters = {'self': self}
        global mqttc
        mqttc = mqtt.Client(client_id="kivy-client", clean_session=True, userdata = parameters)
        mqttc.on_connect      = onConnect
        mqttc.on_message      = onMessage
        
        mqttc.loop_start() # start loop to process callbacks! (new thread!)
        try:
            mqttc.connect(MQTT_SERVER, 1883, keepalive=60, bind_address="")
        except:
            mqttc.connected_flag=False

        while not mqttc.connected_flag: #wait in loop
            #print("In wait loop")
            time.sleep(1)
        #print("in Main Loop")
        
