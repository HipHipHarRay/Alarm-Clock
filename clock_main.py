from time import strftime
from kivy.app import App
from homescreen import HomePage
from kivy.uix.screenmanager import ScreenManager
from clock_common import AlarmPopup, StopwatchPopup


class ClockApp(App):
    def build(self):
        self.sm = ScreenManager()
        self.sm.add_widget(HomePage(name='home'))
        return self.sm


class Alarm(App):
    def build(self):
        self.sm = ScreenManager()
        self.sm.add_widget(AlarmPopup(name='Alarm'))
        return self.sm


class StopwatchApp(App):
    def build(self):
        self.sm = ScreenManager()
        self.sm.add_widget(StopwatchPopup(name='Stopwatch'))
        return self.sm


if __name__ == "__main__":
    ClockApp().run()

# Could make new page for Homescreen, and import clock_main. Then I can use ClockApp().run() in another program.
# Have a look for unit tests for each method in App.
# How to write unit tests. How to write resuable code.
# Check youtube about interviews.
