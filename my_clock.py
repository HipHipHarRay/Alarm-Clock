import datetime
import winsound
from kivy.app import App
from kivy.graphics import Color, Rectangle
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
import threading


class HomePage(FloatLayout):

    def __init__(self, **kwargs):
        super(HomePage, self).__init__(**kwargs)

        self.time = datetime.datetime.now().strftime("%H:%M")
        self.date = datetime.datetime.now().strftime("%d-%m-%Y")

        self.clock = Label(
            text=self.time,
            font_name="Calibrib.ttf",
            outline_color=(1, 1, 0, 0),
            font_size=200,
            bold=True,
            size_hint=(.7, .50),
            pos_hint={'center_x': .5, 'center_y': .7})

        self.alarm_button = Button(
            text="Alarm",
            font_name="Calibrib.ttf",
            outline_color=(1, 1, 0, 0),
            font_size=60,
            bold=True,
            size_hint=(.7, .15),
            pos_hint={'center_x': .5, 'center_y': .3},
            on_press=lambda x: AlarmPopup().open())

        self.timer_button = Button(
            text="Timer",
            font_name="Calibrib.ttf",
            outline_color=(1, 1, 0, 0),
            font_size=60,
            bold=True,
            size_hint=(.7, .15),
            pos_hint={'center_x': .5, 'center_y': .15})

        self.add_widget(self.clock)
        self.add_widget(self.alarm_button)
        self.add_widget(self.timer_button)

    def refresh(self):
        self.clock.text = self.time

    def set_interval(func, sec):
        def func_wrapper():
            set_interval(func, sec)
            func()
            t = threading.Timer(sec, func_wrapper)
            t.start()
            return t
    set_interval(refresh,1000)


class AlarmPopup(Popup):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


        self.text_input = TextInput(
            text="Alarm",
            hint_text="HH:MM",
            multiline=False,
            font_name="Calibrib.ttf",
            size_hint=(.5, .3),
            pos_hint={'center_x': .5, 'center_y': .7})

        self.set_alarm_button = Button(
            text="Set Alarm",
            font_name="Calibrib.ttf",
            outline_color=(1, 1, 0, 0),
            font_size=60,
            bold=True,
            size_hint=(.5, .15),
            pos_hint={'center_x': .5, 'center_y': .15})

        self.content = FloatLayout(
            self.add_widget(self.text_input)
            # self.add_widget(self.set_alarm_button)
        )

    def set_alarm(self, instance):
        alarm_time = self.text_input.text
        main_time = datetime.datetime.now().strftime("%H:%M")
        if alarm_time == main_time:
            winsound.Beep(500, 5000)
            self.text_input.text = ''


class MainApp(App):

    def build(self):
        self.root = root = HomePage()
        root.bind(size=self._update_rect, pos=self._update_rect)

        with root.canvas.before:
            Color(0, 0.45, 0.85, 0.2)  # Colours range from 0-1 not 0-255
            self.rect = Rectangle(size=root.size, pos=root.pos)
        return root

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size


if __name__ == '__main__':
    MainApp().run()
