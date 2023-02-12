import kivy.app
import kivy.animation


class TestApp(kivy.app.App):
    def touch_down_handler(self, *args):
        self.start_char_animation(args[1].spos)

    def change_char_im(self):
        character_image = self.root.ids['character_image']
        character_image.source = str(int(character_image.im_num)) + ".png"

    def start_char_animation(self, touch_pos):
        character_image = self.root.ids['character_image']
        char_anim1 = kivy.animation.Animation(pos_hint={'x': touch_pos[0], 'y': touch_pos[1]},
                                              size_hint=(0.2, 0.2),
                                              duration=1.5,
                                              t='in_quad',
                                              im_num=7)
        char_anim2 = kivy.animation.Animation(pos_hint={'x': 0.8, 'y': 0.2})
        all_anim = char_anim1 + char_anim2
        all_anim.repeat = True
        all_anim.start(character_image)

    def stop_animation(self):
        character_image = self.root.ids['character_image']
        kivy.animation.Animation.cancel_all(character_image)


app = TestApp()
app.run()
