from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen
import random


class SophieCalc(Screen):
    quest = []
    fehlt = 0
    avis = 0
    bvis = 0
    count = 0
    io = 0

    def __init__(self, **kwargs):
        super(SophieCalc, self).__init__(**kwargs)
        self.newQuest()

    def build(self):
        self.newQuest()

    def newQuest(self):
        o = random.randint(0, 1)
        a = random.randint(0, 10)
        b = random.randint(0, 10)
        self.avis = random.randint(0, 1)
        self.bvis = random.randint(0, 1)

        self.ids.Zahl1.text = str(a)
        self.ids.Zahl2.text = str(b)

        if o == 0:
            self.ids.LabelOperand.text = "+"
            c = a + b
            self.quest = [a, "+", b, "=", c]
        else:
            self.ids.LabelOperand.text = "-"
            c = a - b
            self.quest = [a, "-", b, "=", c]
            if a < b:
                self.ids.Zahl1.text = str(b)
                self.ids.Zahl2.text = str(a)
                c = b - a
                self.quest = [b, "-", a, "=", c]

        self.ids.Ergebnis.text = str(c)

        # sichtbarkeit zuordnen
        if self.avis == 0:
            self.ids.Zahl1.text = ""
            self.fehlt = 1
        else:
            if self.bvis == 0:
                self.ids.Zahl2.text = ""
                self.fehlt = 2
            else:
                self.ids.Ergebnis.text = ""
                self.fehlt = 3

    def check(self):
        # print(self.root.ids.count.text)
        # print self.ids
        q = self.quest
        try:
            a = int(self.ids.Zahl1.text)
        except:
            a = 0
        try:
            b = int(self.ids.Zahl2.text)
        except:
            b = 0
        try:
            res = int(self.ids.Ergebnis.text)
        except:
            res = 0
        o = self.ids.LabelOperand.text
        # print(str(a), str(o), str(b), "=", str(res))

        if o == "+":
            # print("plus")
            c = a + b
            op = "+"
        else:
            # print("minus")
            c = a - b
            op = "-"

        p = CustomPopUp()
        p.ids.Labelcond.text = "Falsch!"
        p.ids.Labelcond.color = 1, 0, 0, 1
        p.ids.outputAnswer.color = 1, 0, 0, 1
        p.ids.imgAnswer.source = "falsch.png"
        if res == c:
            self.io += 1
            p.ids.Labelcond.text = "Richtig!"
            p.ids.Labelcond.color = 0, 1, 0, 1
            p.ids.outputAnswer.color = 0, 1, 0, 1
            p.ids.imgAnswer.source = "richtig.png"

        p.ids.outputAnswer.text = "{0} {1} {2} = {3}".format(str(a), op, str(b), str(c))
        self.count += 1
        self.ids.count.text = "Du hast {0} von {1} richtig.".format(str(self.io), str(self.count))

        p.open()
        self.newQuest()

    def calc(self):
        self.ids.outputLabel.text = str(eval(self.root.ids.outputLabel.text))

    def button_pressed(self, button):
        print "es wurde eine Zahl gedrueckt"
        print button.text
        print self.fehlt
        # Zahl 1 fehlt
        if self.fehlt == 1:
            if self.ids.Zahl1.text == '':
                self.ids.Zahl1.text = button.text
            else:
                if button.text == "ENTF":
                    self.ids.Zahl1.text = ""
                else:
                    self.ids.Zahl1.text += button.text
        # Zahl 2 fehlt
        elif self.fehlt == 2:
            if self.ids.Zahl2.text == '':
                self.ids.Zahl2.text = button.text
            else:
                if button.text == "ENTF":
                    self.ids.Zahl2.text = ""
                else:
                    self.ids.Zahl2.text += button.text
        # Ergebnis fehlt
        elif self.fehlt == 3:
            if self.ids.Ergebnis.text == '':
                self.ids.Ergebnis.text = button.text
            else:
                if button.text == "ENTF":
                    self.ids.Ergebnis.text = ""
                else:
                    self.ids.Ergebnis.text += button.text


class CalcAnswer(Screen):
    def __init__(self, **kwargs):
        super(CalcAnswer, self).__init__(**kwargs)


class CustomPopUp(Popup):
    def __init__(self, **kwargs):
        super(CustomPopUp, self).__init__(**kwargs)