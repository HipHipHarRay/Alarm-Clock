import datetime
from time import strftime
from kivy.clock import Clock
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty
from kivy.uix.button import Button
from kivy.uix.label import Label
from clock_common import AlarmPopup, StopwatchPopup

class HomePage(Screen):
    box = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Schedule a callback 'update_time' function to be called every 0.3 seconds(so it would change faster than the alarm).
        Clock.schedule_interval(self.update_time, 0.3)

        # Widget design for the clock/time display.
        self.clock = Label(
            text=datetime.datetime.now().strftime("%H:%M"),
            size_hint=(0.7, 0.5),
            font_size=200,
            font_name="Calibrib.ttf",
            pos_hint={"center_x": 0.5, "center_y": 0.70}
        )

        # Button widget design for Alarm.
        self.alarm_button = Button(
            text="Alarm",
            size_hint=(.5, .13),
            font_size=40,
            font_name="Calibrib.ttf",
            pos_hint={"center_x": 0.5, "center_y": 0.42},
        )

        # Triggers the calling of 'alarm_screen' function when the alarm button is pressed.
        self.alarm_button.bind(on_press=self.alarm_screen)

        # Button widget design for timer.
        self.timer_button = Button(
            text="Timer",
            size_hint=(0.5, 0.13),
            font_size=40,
            font_name="Calibrib.ttf",
            pos_hint={"center_x": 0.5, "center_y": 0.28}
        )

        # Button widget design for stopwatch.
        self.stopwatch_button = Button(
            text="Stopwatch",
            size_hint=(0.5, 0.13),
            font_size=40,
            font_name="Calibrib.ttf",
            pos_hint={"center_x": 0.5, "center_y": 0.14}
        )

        # Triggers the calling of 'stopwatch_screen' function when the stopwatch_button is pressed.
        self.stopwatch_button.bind(on_press=self.stopwatch_screen)

        # Widgets above added to layout.
        self.add_widget(self.clock)
        self.add_widget(self.alarm_button)
        self.add_widget(self.timer_button)
        self.add_widget(self.stopwatch_button)
        # Makes sure the '_update_box' function is called when the size of the box/window is changed.
        self.bind(size=self._update_box, pos=self._update_box)

        # Create a variable for the popup classes.
        self.alarm_popup = AlarmPopup()
        self.stopwatch_popup = StopwatchPopup()

    # alarm_screen fucntion to be called when stopwatch_button is pressed.
    def alarm_screen(self, *args):
        self.alarm_popup.open()

    # stopwatch_screen fucntion to be called when stopwatch_button is pressed.
    def stopwatch_screen(self, *args):
        self.stopwatch_popup.open()

    # Makes sure the box/window is positioned and sized correctly if function is called.
    def _update_box(self, instance, value):
        if self.box is None:
            return
        self.box.pos = instance.pos
        self.box.size = instance.size

    # update_time function to be called by scheduler.
    def update_time(self, dt):
        self.clock.text = datetime.datetime.now().strftime("%H:%M")
