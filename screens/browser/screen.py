from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen

import webview

class BrowserApp(App):
    def build(self):
        return webview.create_window('Full-screen window',
					'http://localhost:1880/ui/',
					fullscreen=True)

class browserScreen(Screen):
    def __init__(self, **kwargs):
        super(browserScreen, self).__init__(**kwargs)

    webview.create_window('Full-screen window',
	  	       	'http://localhost:1880/ui/',
			fullscreen=True)
    webview.start()

