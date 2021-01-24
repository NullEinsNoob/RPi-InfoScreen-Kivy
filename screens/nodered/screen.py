from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen

# from kivy.garden.cefpython import CefBrowser, cefpython
from kivy.app import App

import webview
  

class LoginScreen(BoxLayout):    
    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        self.on_web()    
    
    def on_web(self):
        # url='http://www.google.com'
	url='http://localhost:1880/ui/'
        print("Im open windows")
        webview.create_window('My Web App', url=url)

class BrowserApp(App):    
    def build(self):
        return LoginScreen()


class NodeRedScreen(Screen):
    def __init__(self, **kwargs):
        super(NodeRedScreen, self).__init__(**kwargs)

	BrowserApp().run()
   
