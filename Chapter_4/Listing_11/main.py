import kivy.app
import kivy.uix.screenmanager


class Screen1(kivy.uix.screenmanager.Screen):
    pass


class Screen2(kivy.uix.screenmanager.Screen):
    pass


class TestApp(kivy.app.App):
    pass


app = TestApp()
app.run()
