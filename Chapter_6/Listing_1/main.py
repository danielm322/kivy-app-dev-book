import random
import kivy.uix.image
import kivy.app
import kivy.uix.screenmanager
import kivy.animation


class TestApp(kivy.app.App):
    def screen_on_pre_enter(self, screen_num):
        coin_width = 0.05
        coin_height = 0.05
        curr_screen = self.root.screens[screen_num]
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
        curr_screen = self.root.screens[screen_num]
        monster_image = curr_screen.ids['monster_image_lvl' + str(screen_num)]
        new_pos = (random.uniform(0.0, 1 - monster_image.size_hint[0]),
                   random.uniform(0.0, 1 - monster_image.size_hint[1]))
        self.start_monst_animation(monster_image=monster_image,
                                   new_pos=new_pos,
                                   anim_duration=random.uniform(1.5, 3.5))

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
