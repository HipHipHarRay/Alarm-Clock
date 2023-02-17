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


class ClockApp(App):
    def build(self):
        self.sm = ScreenManager()
        self.sm.add_widget(HomePage(name='home'))
        return self.sm


class AlarmPopup(Popup):
    def __init__(self, **kwargs):
        super(AlarmPopup, self).__init__(**kwargs)
        # Popup windows require a title or display no title.
        self.title = "Set Alarm"

        # As a popup can only have one widget I created a boxlayout that can handle multiple widgets.
        layout = BoxLayout(orientation='vertical')

        # Design for text input widget for alarm, called into the layout.
        self.alarm_input = TextInput(
            hint_text="HH:MM",
            multiline=False,
            size_hint=(1, 0.5),
            pos_hint={'center_x': 0.5, 'center_y': 0.35})
        layout.add_widget(self.alarm_input)

        # Design for alarm set button, called into the layout.
        self.set_alarm_button = Button(
            text="Set Alarm",
            size_hint=(1, 0.5),
            pos_hint={'center_x': 0.5, 'center_y': 0.65},
            on_press=self.set_alarm)
        layout.add_widget(self.set_alarm_button)

        # Set size of overall layout.
        self.add_widget(layout)
        self.size_hint = (0.2, 0.2)

    # Function to retrieve alarm_input, split it into hours and minutes and turn the strings into integers, threaded the function alarm with the newly split user input.
    def set_alarm(self, instance):
        alarm_time = self.alarm_input.text
        alarm_hour, alarm_minute = map(int, alarm_time.split(":"))
        alarm_thread = threading.Thread(
            target=self.alarm, args=(alarm_hour, alarm_minute))
        alarm_thread.start()
        # To stop once the alarm has gone off.
        self.dismiss()

    # alarm fucntion continuously checks the current time and plays a sound when the desired alarm time is reached. The method runs in a separate thread so that it can run concurrently with the rest of the program.
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


class StopwatchPopup(Popup):
    def __init__(self, **kwargs):
        super(StopwatchPopup, self).__init__(**kwargs)
        self.title = "Stopwatch"
        self.time = 0
        # start_time will store the time when the stopwatch starts
        self.start_time = None
        self.update_stopwatch_thread = None

        layout = BoxLayout(orientation='vertical')

        # Need to add a back button to go back to the homepage when finished (can currently use esc).

        # Widget design to display the time on the stopwatch.
        self.stopwatch = Label(
            text="0.00",
            font_name="Calibrib.ttf",
            outline_color=(1, 1, 0, 0),
            font_size=200,
            bold=True,
            size_hint=(0.7, 0.5),
            pos_hint={"center_x": 0.5, "center_y": 0.70})
        layout.add_widget(self.stopwatch)

        # Button widget design for the start button.
        self.start_button = Button(
            text="Start",
            font_name="Calibrib.ttf",
            font_size=40,
            size_hint=(0.5, 0.13),
            pos_hint={"center_x": 0.5, "center_y": 0.42})
        # Triggers the calling of 'start_stopwatch' function when the start button is pressed.
        self.start_button.bind(on_press=self.start_stopwatch)
        layout.add_widget(self.start_button)

        # Button widget design for the stop button.
        self.stop_button = Button(
            text="Stop",
            font_name="Calibrib.ttf",
            font_size=40,
            size_hint=(0.5, 0.13),
            pos_hint={"center_x": 0.5, "center_y": 0.28})
        # Triggers the calling of 'stop_stopwatch' function when the stop button is pressed.
        self.stop_button.bind(on_press=self.stop_stopwatch)
        layout.add_widget(self.stop_button)

        # Button widget design for the restart button.
        self.reset_button = Button(
            text="Reset",
            font_name="Calibrib.ttf",
            font_size=40,
            size_hint=(0.5, 0.13),
            pos_hint={'center_x': 0.5, 'center_y': 0.14})
        # Triggers the calling of 'restart_stopwatch' function when the restart button is pressed.
        self.reset_button.bind(on_press=self.reset_stopwatch)
        layout.add_widget(self.reset_button)

        self.add_widget(layout)

    # Function called when start button is pressed if time is none (0:00), to record the start time and run a separate thread (update_time) to update the screen timer.
    def start_stopwatch(self, instance):
        if not self.start_time:
            self.start_time = time.time()
            self.update_stopwatch_thread = threading.Thread(
                target=self.update_stopwatch)
            self.update_stopwatch_thread.start()
        else:
            self.start_time = None

    # Updates the displayed time every 0.01 seconds based on current time and the start_time variable recorded in start_stopwatch function, until start_time = none.
    def update_stopwatch(self):
        while self.start_time:
            self.time = time.time() - self.start_time
            # The "{:.2f}" format string specifies that the time should be displayed with two decimal places.
            self.stopwatch.text = "{:.2f}".format(self.time)
            time.sleep(0.01)

    # Check the start_time is not none, if so it sets it back to none. The join()method is used to ensure the thread completes before continuing to next line and stopping the update by changing start_time to none
    def stop_stopwatch(self, instance):
        if self.start_time:
            self.start_time = None
            if self.update_stopwatch_thread:
                self.update_stopwatch_thread.join()
                self.update_stopwatch_thread = None

    # Reset the stopwatch display and stop any running stopwatch update thread. First returns start_time to none stopping the clock, and then returns update_stopwatch to none so the clock reads 0:00. Uses join() method as well.
    def reset_stopwatch(self, instance):
        self.start_time = None
        self.time = 0
        self.stopwatch.text = "{:.2f}".format(self.time)
        if self.update_stopwatch_thread:
            self.update_stopwatch_thread.join()
            self.update_stopwatch_thread = None


class StopwatchApp(App):
    def build(self):
        self.sm = ScreenManager()
        self.sm.add_widget(StopwatchPopup(name='Stopwatch'))
        return self.sm


if __name__ == "__main__":
    ClockApp().run()
