import kivy
from kivy.app import App
from kivy.properties import StringProperty, ObjectProperty
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen
from kivy.uix.widget import Widget
import os
import sqlite3
import speech_recognition as sr

kivy.require('1.10.1')


class MainMenu(Screen):
    name = StringProperty('main_menu')


class OtherMenu(Screen):
    name = StringProperty('other_menu')


class Voice(Screen):
    name = StringProperty('voice')

    def open_terminal(self):
        os.system("gnome-terminal")

    def open_office(self):
        os.system("libreoffice")

    def open_powerPoint(self):
        os.system("loimpress")

    def open_Execel(self):
        os.system("localc")

    def command(self):

        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("Speak:")
            audio = r.listen(source)

        try:
            voice = r.recognize_google(audio)
            print("You said " + r.recognize_google(audio))

        except sr.UnknownValueError:
            print("Could not understand audio")
        except sr.RequestError as e:
            print("Could not request results; {0}".format(e))
        if voice == "office":
            self.open_office()
        else:
            if voice == "PowerPoint":
                self.open_powerPoint()
            if voice == "Excel":
                self.open_Execel()
            if voice == "terminal":
                self.open_terminal()


class RootWidget(Widget):
    state = StringProperty('set_main_menu_state')
    screen_manager = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(RootWidget, self).__init__(**kwargs)

    def on_state(self, instance, value, ):
        if value == 'main_menu':
            self.screen_manager.current = 'main_menu'

    def set_state(self, state, u, p):

        if state == 'main_menu':
            self.screen_manager.current = 'other_menu'
        if state == 'other_menu':
            self.screen_manager.current = 'main_menu'

    def callback(self, u, p):

        connection = sqlite3.connect('voice.db')
        cursor = connection.execute("select * from person where username=:usr and password=:pas",
                                    {"usr": u, "pas": p})
        row = cursor.fetchone()

        if row is None:
            popup = Popup(title='Error Sign in', content=Label(text='No Such User'), auto_dismiss=True)
            popup.open()

        else:
            self.screen_manager.current = 'voice'

    def register(self, u, p, f):
        connection = sqlite3.connect("voice.db")
        curssor= connection.cursor()
        curssor.execute("insert into person(username,password,function)values(?,?,?)",
                           (u, p, f))
        connection.commit()


class TestApp(App):

    def build(self):
        pass


if __name__ == '__main__':
    TestApp().run()
