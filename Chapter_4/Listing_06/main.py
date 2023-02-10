'''
Doing the inheritance inside
the KV file limits the capabilities of the new class, as we can’t write functions inside it.
'''

import kivy.app
import kivy.uix.label
import kivy.uix.boxlayout


class MyLayout(kivy.uix.boxlayout.BoxLayout):
    pass


class CustomLabel(kivy.uix.label.Label):
    pass


class TestApp(kivy.app.App):
    pass


app = TestApp()
app.run()
