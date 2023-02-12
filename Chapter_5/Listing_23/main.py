import random

import kivy.app
import kivy.animation


class TestApp(kivy.app.App):
    def char_animation_completed(self, *args):
        character_image = self.root.ids['character_image']
        character_image.im_num = 0

    def monst_animation_completed(self, *args):
        monster_image = self.root.ids['monster_image']
        monster_image.im_num = 10
        new_pos = (random.uniform(0, 1 - monster_image.size_hint[0]), random.uniform(0, 1 - monster_image.size_hint[1]))
        self.start_monst_animation(new_pos=new_pos, anim_duration=random.uniform(1.5, 3.5))

    def touch_down_handler(self, *args):
        self.start_char_animation(args[1].spos)

    def change_char_im(self):
        character_image = self.root.ids['character_image']
        character_image.source = str(int(character_image.im_num)) + ".png"

    def change_monst_im(self):
        monster_image = self.root.ids['monster_image']
        monster_image.source = str(int(monster_image.im_num)) + ".png"

    def start_monst_animation(self, new_pos, anim_duration):
        monster_image = self.root.ids['monster_image']
        monst_anim = kivy.animation.Animation(pos_hint={'x': new_pos[0], 'y': new_pos[1]},
                                              im_num=17,
                                              duration=anim_duration)
        monst_anim.bind(on_complete=self.monst_animation_completed)
        monst_anim.start(monster_image)

    def start_char_animation(self, touch_pos):
        character_image = self.root.ids['character_image']
        char_anim = kivy.animation.Animation(pos_hint={'x': touch_pos[0] - character_image.size_hint[0] / 2,
                                                       'y': touch_pos[1] - character_image.size_hint[1] / 2},
                                             duration=1.5,
                                             t='linear',
                                             im_num=7)
        char_anim.bind(on_complete=self.char_animation_completed)
        char_anim.start(character_image)

    def on_start(self):
        monster_image = self.root.ids['monster_image']
        new_pos = (random.uniform(0.0, 1 - monster_image.size_hint[0]),
                   random.uniform(0.0, 1 - monster_image.size_hint[1]))
        self.start_monst_animation(new_pos=new_pos, anim_duration=random.uniform(1.5, 3.5))

    def monst_pos_hint(self):
        character_image = self.root.ids['character_image']
        monster_image = self.root.ids['monster_image']

        character_center = character_image.center
        monster_center = monster_image.center
        gab_x = character_image.width / 2
        gab_y = character_image.height / 2

        if character_image.collide_widget(monster_image) and \
                abs(character_center[0] - monster_center[0]) <= gab_x and \
                abs(character_center[1] - monster_center[1]) <= gab_y:
            print("Character Killed")


app = TestApp()
app.run()
