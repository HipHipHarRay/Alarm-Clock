import datetime
import winsound
import time
import threading
from time import strftime
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.clock import Clock
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty


class HomePage(Screen):
    box = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_interval(self.update_time, 0.3) #Schedule a callback 'update_time' function to be called every 0.3 seconds(so it would change faster than the alarm).

        self.clock = Label(
            text=datetime.datetime.now().strftime("%H:%M"),
            size_hint=(0.7, 0.5),
            font_size=200,
            font_name="Calibrib.ttf",
            pos_hint={"center_x": 0.5, "center_y": 0.70}
        )

        self.alarm_button = Button(
            text="Alarm",
            size_hint=(.5, .13),
            font_size=40,
            font_name="Calibrib.ttf",
            pos_hint={"center_x": 0.5, "center_y": 0.42},
        )

        self.alarm_button.bind(on_press=self.alarm_screen) #Triggers the calling of 'alarm_screen' function when the alarm button is pressed.

        self.timer_button = Button(
            text="Timer",
            size_hint=(0.5, 0.13),
            font_size=40,
            font_name="Calibrib.ttf",
            pos_hint={"center_x": 0.5, "center_y": 0.28}
        )

        self.stopwatch_button = Button(
            text="Stopwatch",
            size_hint=(0.5, 0.13),
            font_size=40,
            font_name="Calibrib.ttf",
            pos_hint={"center_x": 0.5, "center_y": 0.14}
        )

        self.add_widget(self.clock)
        self.add_widget(self.alarm_button)
        self.add_widget(self.timer_button)
        self.add_widget(self.stopwatch_button)
        self.bind(size=self._update_box, pos=self._update_box) #Makes sure the '_update_box' function is called when the size of the box/window is changed.

        self.alarm_popup = AlarmPopup()

    def alarm_screen(self, *args):
        self.alarm_popup.open()

    def _update_box(self, instance, value): #Makes sure the box/window is positioned and sized correctly if function is called.
        if self.box is None:
            return
        self.box.pos = instance.pos
        self.box.size = instance.size

    def update_time(self, dt):
        self.clock.text = datetime.datetime.now().strftime("%H:%M")


class AlarmPopup(Popup):
    def __init__(self, **kwargs):
        super(AlarmPopup, self).__init__(**kwargs)
        self.title = "Set Alarm"

        layout = BoxLayout(orientation='vertical')

        self.alarm_input = TextInput(
            hint_text="HH:MM",
            multiline=False,
            size_hint=(1, 0.5),
            pos_hint={'center_x': 0.5, 'center_y': 0.35})
        layout.add_widget(self.alarm_input)

        self.set_alarm_button = Button(
            text="Set Alarm",
            size_hint=(1, 0.5),
            pos_hint={'center_x': 0.5, 'center_y': 0.65},
            on_press=self.set_alarm)
        layout.add_widget(self.set_alarm_button)

        self.add_widget(layout)
        self.size_hint = (0.2, 0.2)

    def set_alarm(self, instance):
        alarm_time = self.alarm_input.text
        alarm_hour, alarm_minute = map(int, alarm_time.split(":"))
        alarm_thread = threading.Thread(
            target=self.alarm, args=(alarm_hour, alarm_minute))
        alarm_thread.start()
        self.dismiss()

    def alarm(self, alarm_hour, alarm_minute):
        while True:
            current_time = time.strftime("%H:%M")
            if current_time == f"{alarm_hour:02}:{alarm_minute:02}":
                winsound.Beep(500, 5000)
                break


class Alarm(App):
    def build(self):
        self.sm = ScreenManager()
        self.sm.add_widget(AlarmPopup(name='Alarm'))
        return self.sm


class ClockApp(App):
    def build(self):
        self.sm = ScreenManager()
        self.sm.add_widget(HomePage(name='home'))
        return self.sm


if __name__ == "__main__":
    ClockApp().run()
