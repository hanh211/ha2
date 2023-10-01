#!/usr/bin/env python

import kivy
import lovecal

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.properties import StringProperty
from kivy.graphics import Color, Rectangle
from kivy.core.audio import SoundLoader
from kivy.uix.textinput import TextInput
from kivy.core.window import Window
from kivy.uix.bubble import Bubble


class ValidateInput(TextInput):
    #invalid_set = r"/\*:|'.?" + '"<>'

    invalid_set = r"[-.\'@_!#$%^&*()<>?/\|}{~:0123456789 ]"
    count = 0

    def insert_text(self, substring, from_undo=False):
        firstname = [c for c in substring if c not in self.invalid_set]
        s = ''.join(firstname)
        if not self.filled:
            return super().insert_text(s, from_undo=from_undo)


#    def keyboard_on_key_up(self, keycode, text):
#        if self.readonly and text[1] == "backspace":
#            self.readonly = False
#            self.do_backspace()

class Manager(ScreenManager):

    result = StringProperty(None)
    percentage = StringProperty(None)

    def __init__(self, **kwargs):
        super(Manager, self).__init__(**kwargs)

    def playstart(self):
        sound = SoundLoader.load('sound/click.wav')
        sound.play()

    def playreturn(self):
        sound = SoundLoader.load('sound/click.wav')
        sound.play()


    def results(self):
        sound = SoundLoader.load('sound/click.wav')
        print(self.ids.firstname.text)
        print(self.ids.secondname.text)
        first = self.ids.firstname.text
        second = self.ids.secondname.text
        results = lovecal.calculator(first, second)
        #print(results)
        if results == "Failed":
            self.result = "Failed"
            self.percentage = "Failed"
        else:
            self.result = results['result']
            self.percentage = results['percentage']
        #self.result = results[1]
        #self.percentage = results[0]
        print(self.result)
        print(self.percentage)
        #print(str(results['percentage']))
        #print(str(results['result']))
        sound.play()

class ScreenApp(App):
    def build(self):
        self.icon = 'images/appicon.png'
        self.sm = Manager()
        return self.sm

Window.softinput_mode = "below_target"

if __name__ == '__main__':
    ScreenApp().run()
