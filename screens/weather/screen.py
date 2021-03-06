import os
import sys
import requests
import time
from datetime import date
from datetime import datetime
os.environ['KIVY_GL_BACKEND'] = 'gl'

from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty
from kivy.clock import Clock
from kivy.uix.scrollview import ScrollView

sys.path.append(os.path.dirname(os.path.abspath(__file__)))


class WeatherForecastHourly(BoxLayout):
    """Custom widget to show hourly forecast summary."""
    weather = StringProperty("")

    def __init__(self, **kwargs):
        super(WeatherForecastHourly, self).__init__(**kwargs)
        self.buildText(kwargs["summary"])

    def buildText(self, summary):
        wochen = {
            "Monday": "Montag",
            "Tuesday": "Dienstag",
            "Wednesday": "Mittwoch",
            "Thursday": "Donnerstag",
            "Friday": "Freitag",
            "Saturday": "Samstag",
            "Sunday": "Sonntag"
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
        super(WeatherForecastDay, self).__init__(**kwargs)
        self.buildText(kwargs["summary"])

    def buildText(self, summary):
        wochen = {
            "Monday": "Montag",
            "Tuesday": "Dienstag",
            "Wednesday": "Mittwoch",
            "Thursday": "Donnerstag",
            "Friday": "Freitag",
            "Saturday": "Samstag",
            "Sunday": "Sonntag"
        }
        fc = {}
        cond = ''
        icnurl = ''
        self.day = wochen.get(datetime.fromtimestamp(summary.get('dt')).strftime('%A'))
        weather = summary['weather']
        for item in weather:
            cond = str(item['main'])
            icon = item['icon']
            icnurl = "http://openweathermap.org/img/w/" + str(icon)

        fc["su"] = cond
        main = summary['main']
        temp_min = str(main['temp_min'])
        temp_max = str(main['temp_max'])
        fc["hg"] = temp_max
        fc["lw"] = temp_min
        self.icon_url = icnurl
        self.weather = ("{su}\nTmax: {hg}{dg}\n"
                        "Tmin: {lw}%").format(dg="C", **fc)

        """self.weather = ("{su}\nTmax: {hg}{dg}\n"
                        "Tmin: {lw}\nRegen: {po}%").format(dg="C", **fc)"""


class WeatherSummary(Screen):
    """Screen to show weather summary for a selected location."""
    location = StringProperty("")

    def __init__(self, **kwargs):
        super(WeatherSummary, self).__init__(**kwargs)
        self.location = kwargs["location"]
        self.url_forecast = kwargs["forecast"]
        self.url_hourly = kwargs["hourly"]
        self.bx_forecast = self.ids.bx_forecast
        self.bx_hourly = self.ids.bx_hourly
        self.nextupdate = 0
        self.timer = None

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
        # Try to get the daily data but handle any failure to do so.
        try:
            self.forecast = requests.get(self.url_forecast).json()
            days = self.forecast["forecast"]["simpleforecast"]["forecastday"]
        except:
            days = None

        # Try to get the hourly data but handle any failure to do so.
        try:
            self.hourly = requests.get(self.url_hourly).json()
            hours = self.hourly["hourly_forecast"]
        except:
            hours = None

        # Clear the screen of existing widgets
        self.bx_forecast.clear_widgets()
        self.bx_hourly.clear_widgets()

        # If we've got daily info then we can display it.
        if days:
            for day in days:
                frc = WeatherForecastDay(summary=day)
                self.bx_forecast.add_widget(frc)

        # If not, let the user know.
        else:
            lb_error = Label(text="Error getting weather data.")
            self.bx_forecast.add_widget(lb_error)

        # If we've got hourly weather data then show it
        if hours:

            # We need a scroll view as there's a lot of data...
            w = len(hours) * 45
            bx = BoxLayout(orientation="horizontal", size=(w, 180),
                           size_hint=(None, None), spacing=5)
            sv = ScrollView(size_hint=(1, 1))
            sv.add_widget(bx)

            for hour in hours:
                frc = WeatherForecastHourly(summary=hour)
                bx.add_widget(frc)
            self.bx_hourly.add_widget(sv)

        # If there's no data, let the user know
        else:
            lb_error = Label(text="Error getting weather data.")
            self.bx_forecast.add_widget(lb_error)

        # We're done, so schedule the next update
        if hours and days:
            dt = 60 * 60
        else:
            dt = 5 * 60

        self.nextupdate = time.time() + dt
        self.timer = Clock.schedule_once(self.getData, dt)


class WeatherScreen(Screen):
    # forecast = "https://api.openweathermap.org/data/2.5/forecast?id=2927916&mode=json&units=metric&APPID={key}"
    forecast = "https://api.openweathermap.org/data/2.5/forecast?id={location}&mode=json&units=metric&APPID={key}"
    # hourly = "https://api.openweathermap.org/data/2.5/weather?id=2927916&mode=json&units=metric&APPID={key}"
    hourly = "https://api.openweathermap.org/data/2.5/weather?id={location}&mode=json&units=metric&APPID={key}"

    def __init__(self, **kwargs):
        super(WeatherScreen, self).__init__(**kwargs)
        self.key = kwargs["params"]["key"]
        self.location = kwargs["params"]["location"]
        self.flt = self.ids.weather_float
        self.flt.remove_widget(self.ids.weather_base_box)
        self.scrmgr = self.ids.weather_scrmgr
        self.running = False
        self.scrid = 0
        self.myscreens = [x["address"] for x in self.locations]

    def on_enter(self):
        # If the screen hasn't been displayed before then let's load up
        # the locations
        if not self.running:
            for location in self.location:

                # Create the necessary URLs for the data
                forecast, hourly = self.buildURLs(location["address"])

                # Create a weather summary screen
                ws = WeatherSummary(forecast=forecast,
                                    hourly=hourly,
                                    name=location["address"],
				    location=location["name"])

                # and add to our screen manager.
                self.scrmgr.add_widget(ws)

            # set the flag so we don't do this again.
            self.running = True

        else:
            # Fixes bug where nested screens don't have "on_enter" or
            # "on_leave" methods called.
            for c in self.scrmgr.children:
                if c.name == self.scrmgr.current:
                    c.on_enter()

    def on_leave(self):
        # Fixes bug where nested screens don't have "on_enter" or
        # "on_leave" methods called.
        for c in self.scrmgr.children:
            if c.name == self.scrmgr.current:
                c.on_leave()

    def buildURLs(self, location):
        return (self.forecast.format(key=self.key, location=self.location),
                self.hourly.format(key=self.key, location=self.location))

    def next_screen(self, rev=True):
        a = self.myscreens
        n = -1 if rev else 1
        self.scrid = (self.scrid + n) % len(a)
        self.scrmgr.transition.direction = "up" if rev else "down"
        self.scrmgr.current = a[self.scrid]
