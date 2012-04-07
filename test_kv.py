# -*- coding:utf-8 -*-

import kivy
#kivy.require("1.2.0")

from kivy.uix.floatlayout import FloatLayout
from kivy.uix.stacklayout import StackLayout
from kivy.uix.popup import Popup
from kivy.app import App

class Panier(StackLayout):
    pass

class Details(Popup):
    uv = ""

    def __init__(self, uv, **kwargs):
        super(Details, self).__init__(**kwargs)
        self.uv = uv
	self.tree.bind(minimum_height=self.tree.setter("height"))

    def commander_pressed(self):
        self.dismiss()

class Root(FloatLayout):
    def title_touched(self):
        print "Here we are !"
        Details("MT23").open()

class TestApp(App):
    def build(self):
        return Root()

if __name__ == "__main__":
    TestApp().run()
