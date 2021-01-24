from datetime import datetime

from kivy.clock import Clock
from kivy.properties import StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen

class birthdayScreen(Screen):

    first_line = StringProperty("")
    second_line = StringProperty("")
    third_line = StringProperty("")

    def __init__(self, **kwargs):
        #super(birthdayScreen, self).__init__(**kwargs)
        super(birthdayScreen, self).__init__()
        self.name="birthday"
        self.birthdates = kwargs["params"]

        self.bname, month, day, self.byear = self.getBirthday(self.birthdates)
	
        self.birthday = self.getDay(month, day)
        self.first_line = "Es sind noch ..."
        self.second_line = "[Berechne Zeit...]"
        self.third_line = "bis zu Deinem Geburtstag!"
        self.timer = None
    
    def getBirthday(self, birthdates):
        month = 12
        day = 31
        year = 1900
        name = "Silvester"
        nw = datetime.now()

        for person, date in birthdates.items():

            if nw.month > date[1]:
                continue
            if nw.month == date[1] and nw.day > date[0]:
                continue
	    
            if month >= date[1]:
                if month == date[1]:
                    if day > date[0]:
                        month = date[1]
                        day = date[0]
                        year = date[2]
                        name = person
                else:
                    month = date[1]
                    day = date[0]
                    year = date[2]
                    name = person
        return name, month, day, year

    def getDay(self, month, day):
        nw = datetime.now()
        if nw.month == month and nw.day > day:
            yr = nw.year + 1
        else:
            yr = nw.year

        return datetime(yr, month, day, 0, 0)

    def on_enter(self):
        self.timer = Clock.schedule_interval(self.update, 1)

    def on_leave(self):
        Clock.unschedule(self.timer)

    def update(self, *args):
        nw = datetime.now()
	
        if self.birthday.month >= nw.month and self.birthday.day < nw.day:
            self.bname, month, day, self.byear = self.getBirthday(self.birthdates)
            self.birthday = self.getDay(month, day)
        
        delta = self.birthday - nw
        y = nw.year - self.byear

        if delta.total_seconds() < 0:
            # It's Bday

            self.first_line = "[size=30]Alles Gute[/size]"
            self.second_line = "[size=80]zum {year}. Geburtstag,[/size]".format(year=y)
            self.third_line = "[size=30]{name}![/size]".format(name=self.bname)

        else:

            d = delta.days
            h, rem = divmod(delta.seconds, 3600)
            m, _ = divmod(rem, 60)
	    
            self.first_line = "[size=30]Es sind noch ...[/size]"
            self.second_line = ("[size=30][size=70]{d}[/size] Tage, "
                                "[size=60]{h}[/size] Stunden und "
                                "[size=60]{m}[/size] "
                                "Minuten[/size]").format(d=d, h=h, m=m)
            self.third_line = "[size=30]... bis zu Deinem [size=60]{year}.[/size][size=30] Geburtstag, [size=60]{name}.[/size]".format(name=self.bname, year=y)
