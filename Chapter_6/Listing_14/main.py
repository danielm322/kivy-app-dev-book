import functools
import random
import kivy.uix.image
import kivy.app
import kivy.uix.screenmanager
import kivy.animation
import kivy.clock
import kivy.core.audio
from os import getcwd

class TestApp(kivy.app.App):
    def screen_on_pre_enter(self, screen_num):
        coin_width = 0.05
        coin_height = 0.05
        curr_screen = self.root.screens[screen_num]
        curr_screen.character_killed = False
        curr_screen.num_coins_collected = 0
        curr_screen.ids['character_image_lvl' + str(screen_num)].im_num = 0
        curr_screen.ids['monster_image_lvl' + str(screen_num)].im_num = 10
        curr_screen.ids['num_coins_collected_lvl' + str(screen_num)].text = "Coins 0"
        for key, coin in curr_screen.coins_ids.items():
            curr_screen.ids['layout_lvl' + str(screen_num)].remove_widget(coin)
        curr_screen.coins_ids = {}
        section_width = 1.0 / curr_screen.num_coins
        for k in range(curr_screen.num_coins):
            x = random.uniform(section_width * k, section_width * (k + 1) - coin_width)
            y = random.uniform(0, 1 - coin_height)
            coin = kivy.uix.image.Image(source="graphics/coin.png",
                                        size_hint=(coin_width, coin_height),
                                        pos_hint={'x': x, 'y': y}, allow_stretch=True)
            curr_screen.ids['layout_lvl' + str(screen_num)].add_widget(coin, index=-1)
            curr_screen.coins_ids['coin' + str(k)] = coin

    def screen_on_enter(self, screen_num):
        music_dir = getcwd() + "/music/"
        self.bg_music = kivy.core.audio.SoundLoader.load(music_dir + "bg_music_piano.wav")
        self.bg_music.loop = True
        self.coin_sound = kivy.core.audio.SoundLoader.load(music_dir + "coin.wav")
        self.level_completed_sound = kivy.core.audio.SoundLoader.load(music_dir + "level_completed_flaute.wav")
        self.char_death_sound = kivy.core.audio.SoundLoader.load(music_dir + "char_death_flaute.wav")
        self.bg_music.play()
        
        curr_screen = self.root.screens[screen_num]
        monster_image = curr_screen.ids['monster_image_lvl' + str(screen_num)]
        new_pos = (random.uniform(0.0, 1 - monster_image.size_hint[0]),
                   random.uniform(0.0, 1 - monster_image.size_hint[1]))
        self.start_monst_animation(monster_image=monster_image,
                                   new_pos=new_pos,
                                   anim_duration=random.uniform(1.5, 3.5))

    def screen_on_pre_leave(self, screen_num):
        curr_screen = self.root.screens[screen_num]
        curr_screen.ids['monster_image_lvl' + str(screen_num)].pos_hint = {'x': 0.8, 'y': 0.8}
        curr_screen.ids['character_image_lvl' + str(screen_num)].pos_hint = {'x': 0.2, 'y': 0.6}

    def start_monst_animation(self, monster_image, new_pos, anim_duration):
        monst_anim = kivy.animation.Animation(pos_hint={'x': new_pos[0], 'y': new_pos[1]},
                                              im_num=17,
                                              duration=anim_duration)
        monst_anim.bind(on_complete=self.monst_animation_completed)
        monst_anim.start(monster_image)

    def monst_animation_completed(self, *args):
        monster_image = args[1]

        monster_image.im_num = 10
        new_pos = (random.uniform(0.0, 1 - monster_image.size_hint[0]),
                   random.uniform(0.0, 1 - monster_image.size_hint[1]))
        self.start_monst_animation(monster_image=monster_image,
                                   new_pos=new_pos,
                                   anim_duration=random.uniform(1.5, 3.5))

    def monst_pos_hint(self, monster_image):
        screen_num = int(monster_image.parent.parent.name[5:])
        curr_screen = self.root.screens[screen_num]
        character_image = curr_screen.ids['character_image_lvl' + str(screen_num)]
        character_center = character_image.center
        monster_center = monster_image.center
        gab_x = character_image.width / 2
        gab_y = character_image.height / 2
        if character_image.collide_widget(monster_image) and \
                abs(character_center[0] - monster_center[0]) <= gab_x and \
                abs(character_center[1] - monster_center[1]) <= gab_y and \
                curr_screen.character_killed == False:
            self.bg_music.stop()
            self.char_death_sound.play()
            curr_screen.character_killed = True
            kivy.animation.Animation.cancel_all(character_image)
            kivy.animation.Animation.cancel_all(monster_image)
            character_image.im_num = 91
            char_anim = kivy.animation.Animation(im_num=95)
            char_anim.start(character_image)
            kivy.clock.Clock.schedule_once(functools.partial(self.back_to_main_screen, curr_screen.parent), 3)

    def back_to_main_screen(self, screenManager, *args):
        screenManager.current = "main"

    def touch_down_handler(self, screen_num, args):
        curr_screen = self.root.screens[screen_num]
        if not curr_screen.character_killed:
            self.start_char_animation(screen_num, args[1].spos)

    def start_char_animation(self, screen_num, touch_pos):
        curr_screen = self.root.screens[screen_num]
        character_image = curr_screen.ids['character_image_lvl' + str(screen_num)]
        character_image.im_num = 0
        char_anim = kivy.animation.Animation(pos_hint={'x': touch_pos[0] - character_image.size_hint[0] / 2,
                                                       'y': touch_pos[1] - character_image.size_hint[1] / 2},
                                             im_num=7)
        char_anim.bind(on_complete=self.char_animation_completed)
        char_anim.start(character_image)

    def char_animation_completed(self, *args):
        character_image = args[1]
        character_image.im_num = 0

    def change_monst_im(self, monster_image):
        screen_num = int(monster_image.parent.parent.name[5:])
        monster_image.source = "graphics/entities/" + str(int(monster_image.im_num)) + ".png"

    def char_pos_hint(self, character_image):
        screen_num = int(character_image.parent.parent.name[5:])
        character_center = character_image.center
        gab_x = character_image.width / 3
        gab_y = character_image.height / 3
        coins_to_delete = []
        curr_screen = self.root.screens[screen_num]
        for coin_key, curr_coin in curr_screen.coins_ids.items():
            curr_coin_center = curr_coin.center
            if character_image.collide_widget(curr_coin) and\
                    abs(character_center[0] - curr_coin_center[0]) <= gab_x and\
                    abs(character_center[1] - curr_coin_center[1]) <= gab_y:
                self.coin_sound.play()
                coins_to_delete.append(coin_key)
                curr_screen.ids['layout_lvl' + str(screen_num)].remove_widget(curr_coin)
                curr_screen.num_coins_collected = curr_screen.num_coins_collected + 1
                curr_screen.ids['num_coins_collected_lvl' + str(screen_num)].text = "Coins " + str(curr_screen.num_coins_collected)
                if curr_screen.num_coins_collected == curr_screen.num_coins:
                    self.bg_music.stop()
                    self.level_completed_sound.play()
                    kivy.animation.Animation.cancel_all(character_image)
                    kivy.clock.Clock.schedule_once(functools.partial(self.back_to_main_screen, curr_screen.parent), 3)
                    kivy.animation.Animation.cancel_all(curr_screen.ids['monster_image_lvl' + str(screen_num)])
                    curr_screen.ids['layout_lvl' + str(screen_num)].add_widget(kivy.uix.label.Label(pos_hint={'x': 0.1, 'y':0.1}, size_hint=(0.8, 0.8), font_size=90, text="Level Completed"))

        if len(coins_to_delete) > 0:
            for coin_key in coins_to_delete:
                del curr_screen.coins_ids[coin_key]

    def change_char_im(self, character_image):
        character_image.source = "graphics/entities/" + str(int(character_image.im_num)) + ".png"


class MainScreen(kivy.uix.screenmanager.Screen):
    pass


class Level1(kivy.uix.screenmanager.Screen):
    character_killed = False
    num_coins = 5
    num_coins_collected = 0
    coins_ids = {}


class Level2(kivy.uix.screenmanager.Screen):
    character_killed = False
    num_coins = 8
    num_coins_collected = 0
    coins_ids = {}


app = TestApp()
app.run()
