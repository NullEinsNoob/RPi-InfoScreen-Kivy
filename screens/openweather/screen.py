import requests
from datetime import datetime
import time

from kivy.uix.screenmanager import Screen

from kivy.uix.label import Label
from kivy.uix.image import AsyncImage
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.clock import Clock
from kivy.properties import StringProperty


def wind_deg2txt(deg):
    #                 0   1    2   3    4   5    6   7    8
    wind_dir_name = ['N', 'NO', 'O', 'SO', 'S', 'SW', 'W', 'NW', 'N']
    if deg:
        wind_sections = 360 / 8
        offset = wind_sections / 2
        y = int((deg + offset) / wind_sections)
        wind_dir_txt = wind_dir_name[y]
    else:
        wind_dir_txt = "XX"
    return (wind_dir_txt)


def get_weather(url):
    try:
        #print("url: ", url)
        r = requests.get(url)
    except Exception as e:
        print("Fehler bei Anfrage: ", e)
    return r.json()


def time_converter(time):
    converted_time = datetime.datetime.fromtimestamp(
        int(time)
    ).strftime('%I:%M %p')
    return converted_time


class WeatherForecastHourly(BoxLayout):
    """Custom widget to show hourly forecast summary."""
    weather = StringProperty("")

    def __init__(self, **kwargs):
        #super(WeatherForecastHourly, self).__init__(**kwargs)
        super(WeatherForecastHourly, self).__init__()
        self.name="openweather"
        self.buildText(kwargs["summary"])

    def buildText(self, summary):
        wochen = {
            "Monday": "Mo",
            "Tuesday": "Di",
            "Wednesday": "Mi",
            "Thursday": "Do",
            "Friday": "Fr",
            "Saturday": "Sa",
            "Sunday": "So"
        }
        fc = {}

        date = summary["dt_txt"]
        day = wochen.get(datetime.fromtimestamp(summary['dt']).strftime('%A'))
        hour = datetime.fromtimestamp(summary['dt']).strftime('%H')

        fc["dy"] = "{} {}".format(day, hour)
        fc["su"] = summary["weather"][0]["description"]
        fc["hg"] = summary['main']['temp_max']
        fc["po"] = summary["clouds"]["all"]
        self.weather = ("{dy}\n{su}\nmax: "
                        "{hg}{dg}\nRegen: {po}%").format(dg="C", **fc)


class WeatherForecastDay(BoxLayout):
    """Custom widget to show daily forecast summary."""

    weather = StringProperty("")
    icon_url = StringProperty("")
    day = StringProperty("")

    def __init__(self, **kwargs):
        #super(WeatherForecastDay, self).__init__(**kwargs)
        super(WeatherForecastDay, self).__init__()
        self.buildText(kwargs["summary"])

    def buildText(self, day):
        print("forecast day")
        wochen = {
            "Monday": "Mo",
            "Tuesday": "Di",
            "Wednesday": "Mi",
            "Thursday": "Do",
            "Friday": "Fr",
            "Saturday": "Sa",
            "Sunday": "So"
        }
        dt = day['dt_txt']
        main = day['main']
        print("main: ", main)
        temp = str(main['temp_max'])
        weather = day['weather']
        
        for item in weather:
            print("Item: ", item)
            desc = item['description']
            print("description day: ", desc)
            print(type(desc))
            #newStringThing = desc.decode(encoding='UTF-8')
            #descN = str(desc, encoding='UTF-8')
            #descN = desc.decode()
            icon = item['icon']

        wind = day['wind']
        print("wind: ", wind)
        dir = wind_deg2txt(wind['deg'])
        print("directioin: ", dir)
        # rain = day['rain']

        img = "http://openweathermap.org/img/w/" + str(icon) + ".png"

        print("text")
        text = "[size=25]T: {0} C\n[/size]" \
               "[size=20]{1}\n[/size]" \
               "{2}".format(temp, desc, dir)
               #"{2}".format(temp, desc.encode('utf-8'), dir)
        print("Tag")
        self.day = ""
        txt = wochen.get(datetime.fromtimestamp(day.get('dt')).strftime('%A'))
        self.day = "[size=35]{}[/size]".format(txt)
        print("weather")
        self.weather = text
        print("icon")
        self.icon_url = img


class openweather(Screen):
    def __init__(self, **kwargs):
        #super(openweather, self).__init__(**kwargs)
        super(openweather, self).__init__()
        self.name="openweather"
        self.key = kwargs["params"]["key"]
        self.localID = kwargs["params"]["localID"]
        self.bx_forecast = self.ids.bx_forecast
        self.bx_hourly = self.ids.bx_hourly
        self.nextupdate = 0
        self.timer = None
        self.json_out_cur = ""
        self.getData()

    def on_enter(self):
        # Check if the next update is due
        if (time.time() > self.nextupdate):
            dt = 0.5
        else:
            dt = self.nextupdate - time.time()

        self.timer = Clock.schedule_once(self.getData, dt)

    def on_leave(self):
        Clock.unschedule(self.timer)

    def getData(self, *args):
        #print("getData")
        # Try to get the daily data but handle any failure to do so.
        try:
            #print("try days")
            self.forecast = get_weather(
                # "https://api.openweathermap.org/data/2.5/weather?q={self.localID}&mode=json&units=metric&APPID={self.key}")
                "https://api.openweathermap.org/data/2.5/forecast?q=Falkenstein/Vogtland&lang=de&mode=json&units=metric&APPID=2aabe577ee483dbc0f67e1e434c8e5b1")

            days = self.forecast['list']
            #print("forecast: ", self.forecast)
            #print("days: ", days)
        except Exception as e:
            print("Fehler bei Anfrage forecast", e)
            days = None

        # Try to get the hourly data but handle any failure to do so.
        try:
            #print("try hourly")
            self.hourly = get_weather(
                # "https://api.openweathermap.org/data/2.5/weather?q={self.localID}&mode=json&units=metric&APPID={self.key}")
                "https://api.openweathermap.org/data/2.5/weather?q=Falkenstein/Vogtland&lang=de&mode=json&units=metric&APPID=2aabe577ee483dbc0f67e1e434c8e5b1")
            #print("response")
            #print(self.hourly)
            hours = self.hourly

        except Exception as e:
            print("Fehler bei Anfrage hourly", e)
            hours = None
        print("vor Clear screen")
        # Clear the screen of existing widgets
        self.bx_forecast.clear_widgets()
        # self.bx_hourly.clear_widgets()

        # If we've got daily info then we can display it.
        daycount = 0
        if days:
            # print days
            for day in days:
                if day['dt_txt'].endswith('12:00:00'):
                    frc = WeatherForecastDay(summary=day)
                    self.bx_forecast.add_widget(frc)
                    daycount += 1
                if daycount > 5:
                    break

        # If not, let the user know.
        else:
            lb_error = Label(text="Error getting weather data.")
            self.bx_forecast.add_widget(lb_error)

        # If we've got hourly weather data then show it
        if hours:
            print("stunden")
            self.get_hourly(hours)

        # If there's no data, let the user know
        else:
            lb_error = Label(text="Error getting weather data.")
            self.bx_forecast.add_widget(lb_error)

        # We're done, so schedule the next update
        if hours and days:
            dt = 60 * 60
        else:
            dt = 5 * 60
        print("update")
        self.nextupdate = time.time() + dt
        self.timer = Clock.schedule_once(self.getData, dt)
        # print "ende"

    def get_hourly(self, hours):
        print("get_hourly")
        name = str(hours.get('name'))
        weather = hours['weather']
        print("items in weather")
        for item in weather:
            print("Item: ", item)
            mainitem = item['main']
            desc = item['description']
            icon = item['icon']
            icnurl = "http://openweathermap.org/img/w/" + str(icon) + ".png"

        main = hours['main']
        temp = str(main.get('temp'))
        tmp_min = str(main.get('temp_min'))
        temp_max = str(main.get('temp_max'))
        hum = str(main.get('humidity'))
        press = str(main.get('pressure'))

        wind = hours['wind']
        #print("Wind")
        #print wind.get('deg')
        dir = wind_deg2txt(wind.get('deg'))
        speed = str(wind.get('speed'))

        # '[size=24]Temp.: {3} C[/size]\n' \

        sys = hours['sys']
        sunrise = datetime.fromtimestamp(sys.get('sunrise')).strftime('%H:%M')
        sunset = datetime.fromtimestamp(sys.get('sunset')).strftime('%H:%M')
        # self.ids.hourly.text
       
        text = '[size=35]{0}\n[/size]' \
            '[size=35]{2}[/size]\n' \
            'Temp.: [size=35]{3} C\n[/size]' \
            "Temp. min: [size=35]{4} C[/size], max: [size=35]{5} C[/size]\n" \
            "\n" \
            "Luftfeuchte: {6} %, Druck: {7} hPa\n" \
            "Wind aus {8}, {9} m/s\n" \
            "Sonne von {10} bis {11}".format(name, mainitem, desc, temp, tmp_min, temp_max, hum, press, dir, speed, sunrise, sunset)
    
        self.ids.hourly.text = text
      
        self.ids.iconhourly.source = icnurl
       
        # self.bx_hourly.add_widget(AsyncImage(source=icnurl))
        # self.bx_hourly.add_widget(Label(text=lb))

    def get_day(self, day):
        print("def get_day")
        dt = day['dt_txt']
        main = day['main']
        temp = main['temp_max']
        weather = day['weather']

        for item in weather:
            desc = item['description']
            icon = item['icon']

        wind = day['wind']
        # dir = wind['deg']
        dir = wind_deg2txt(wind['deg'])
        # rain = day['rain']

        img = "http://openweathermap.org/img/w/" + str(icon) + ".png"

        text = "{0}\n" \
                  "T: {1} C\n" \
                  "{2}\n" \
                  "{3}".format(dt, temp, desc, dir)
        return text.encode('utf-8'), img
