import random
import kivy.uix.image
import kivy.app
import kivy.animation
import kivy.uix.label
import kivy.core.audio
import os


class TestApp(kivy.app.App):
    character_killed = False
    num_coins = 5
    num_coins_collected = 0
    coins_ids = {}

    def char_animation_completed(self, *args):
        character_image = self.root.ids['character_image']
        character_image.im_num = 0

    def monst_animation_completed(self, *args):
        monster_image = self.root.ids['monster_image']
        monster_image.im_num = 10
        new_pos = (random.uniform(0, 1 - monster_image.size_hint[0]), random.uniform(0, 1 - monster_image.size_hint[1]))
        self.start_monst_animation(new_pos=new_pos, anim_duration=random.uniform(1.5, 3.5))

    def touch_down_handler(self, *args):
        if not self.character_killed:
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
        character_image.im_num = 0
        char_anim = kivy.animation.Animation(pos_hint={'x': touch_pos[0] - character_image.size_hint[0] / 2,
                                                       'y': touch_pos[1] - character_image.size_hint[1] / 2},
                                             duration=1.5,
                                             t='linear',
                                             im_num=7)
        char_anim.bind(on_complete=self.char_animation_completed)
        char_anim.start(character_image)

    def build(self):
        coin_width = 0.05
        coin_height = 0.05
        section_width = 1.0 / self.num_coins
        for k in range(self.num_coins):
            x = random.uniform(section_width * k, section_width * (k + 1) - coin_width)
            y = random.uniform(0, 1 - coin_height)
            coin = kivy.uix.image.Image(source="coin.png",
                                        size_hint=(coin_width, coin_height),
                                        pos_hint={'x': x, 'y': y},
                                        allow_stretch=True)
            self.root.add_widget(coin, index=-1)
            self.coins_ids['coin' + str(k)] = coin

    def on_start(self):
        music_dir = os.getcwd() + "/music/"
        self.bg_music = kivy.core.audio.SoundLoader.load(music_dir + "bg_music_piano.wav")
        self.bg_music.loop = True
        self.coin_sound = kivy.core.audio.SoundLoader.load(music_dir + "coin.wav")
        self.level_completed_sound = kivy.core.audio.SoundLoader.load(music_dir + "level_completed_flaute.wav")
        self.char_death_sound = kivy.core.audio.SoundLoader.load(music_dir + "char_death_flaute.wav")
        self.bg_music.play()
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
            kivy.animation.Animation.cancel_all(character_image)
            kivy.animation.Animation.cancel_all(monster_image)
            self.bg_music.stop()
            self.char_death_sound.play()
            self.character_killed = True
            character_image.im_num = 91
            char_anim = kivy.animation.Animation(im_num=95)
            char_anim.start(character_image)

    def char_pos_hint(self):
        character_image = self.root.ids['character_image']
        character_center = character_image.center
        gab_x = character_image.width / 3
        gab_y = character_image.height / 3
        coins_to_delete = []
        for coin_key, curr_coin in self.coins_ids.items():
            curr_coin_center = curr_coin.center
            if character_image.collide_widget(curr_coin) and abs(
                    character_center[0] - curr_coin_center[0]) <= gab_x and abs(
                    character_center[1] - curr_coin_center[1]) <= gab_y:
                self.coin_sound.play()
                # print("Coin Collected", coin_key)
                coins_to_delete.append(coin_key)
                self.root.remove_widget(curr_coin)
                self.num_coins_collected += 1
                self.root.ids['num_coins_collected'].text = "Coins " + str(self.num_coins_collected)
                if self.num_coins_collected == self.num_coins:
                    self.bg_music.stop()
                    self.level_completed_sound.play()
                    kivy.animation.Animation.cancel_all(character_image)
                    kivy.animation.Animation.cancel_all(self.root.ids['monster_image'])
                    self.root.add_widget(kivy.uix.label.Label(pos_hint={'x': 0.1, 'y': 0.1},
                                                              size_hint=(0.8, 0.8),
                                                              font_size=90,
                                                              text="Level Completed")
                                         )

        if len(coins_to_delete) > 0:
            for coin_key in coins_to_delete:
                del TestApp.coins_ids[coin_key]


app = TestApp()
app.run()
