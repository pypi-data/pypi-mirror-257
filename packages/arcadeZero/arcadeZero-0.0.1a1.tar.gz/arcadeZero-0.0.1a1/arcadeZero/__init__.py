import random
from .constants import _KEY_MAPPING, _IMAGES_MAPPING, _IMAGES_NAMES
from arcade import Window, Sprite, SpriteList, SpriteCircle, SpriteSolidColor
from arcade import get_angle_radians, draw_text, schedule
import sys
from time import time
import math


class Game(Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        self.game_time = 0
        self.running = True
        self.start_time = time()
        self.sprites = SpriteList()
        self.keys = {key: False for key in _KEY_MAPPING}

    def setup(self):
        for s in self.sprites:
            s.position = s.setup_position
            s.stop()
        self.running = True
        self.start_time = time()

    def add_sprite(self, name, pos="center"):
        path = name
        if name.startswith('image:'):
            name = name[6:]
            if name in _IMAGES_NAMES:
                from importlib.resources import path
                with path('arcadeZero.resources.images', '{}.png'.format(name)) as img_path:
                    path = img_path
            elif name in _IMAGES_MAPPING:
                path = _IMAGES_MAPPING[name]
        sprite = Actor(path)
        if isinstance(pos, str):
            if pos == "center":
                position = self.width // 2, self.height // 2
            elif pos == "left":
                position = sprite.width // 2, self.height // 2
            elif pos == "right":
                position = self.width - sprite.width // 2, self.height // 2
            elif pos == "top":
                position = self.width // 2, self.height - sprite.height // 2
            elif pos == "bottom":
                position = self.width // 2, sprite.height // 2
        else:
            position = pos
        sprite.position = sprite.setup_position = position
        self.sprites.append(sprite)
        return sprite

    def add_stars(self, size, pos, num=1):
        stars = Actors()
        for _ in range(num):
            sprite = ActorCircle(radius=size, color=(255, 192, 0), soft=True)
            if isinstance(pos, str):
                if pos == "center":
                    position = self.width // 2, self.height // 2
                elif pos == "left":
                    position = size, self.height // 2
                elif pos == "right":
                    position = self.width - size, self.height // 2
                elif pos == "top":
                    position = self.width // 2, self.height - size
                elif pos == "bottom":
                    position = self.width // 2, size
                elif pos == "rand_in":
                    position = random.randint(0, self.width), random.randint(0, self.height)
                elif pos == "rand_out":
                    while True:
                        position = random.randint(-self.width, self.width * 2), random.randint(-self.height, self.height * 2)
                        if not (0 <= position[0] <= self.width and 0 <= position[1] <= self.height):
                            break
            else:
                position = pos
            sprite.position = sprite.setup_position = position
            stars.append(sprite)
            self.sprites.append(sprite)
        return stars

    def on_draw(self):
        self.clear()
        self.sprites.draw()
        mod = sys.modules['__main__']
        if hasattr(mod, 'draw'):
            mod.draw()

    def draw_text(self, text, *args):
        pos = [20, self.height - 40]
        size = 12
        if args:
            pos = args[:2]
            if len(args) > 2:
                size = args[2]
        draw_text(text, pos[0], pos[1], font_size=size)

    def on_update(self, delta_time):
        if not self.running:
            return
        self.game_time = round(time() - self.start_time, 2)
        mod = sys.modules['__main__']
        if hasattr(mod, 'update'):
            mod.update()
        for s in self.sprites:
            if s.left_key or s.right_key or s.up_key or s.down_key:
                if s.left_key and self.keys[s.left_key] and (not s.right_key or not self.keys[s.right_key]):
                    s.change_x = -s.left_speed
                elif s.right_key and self.keys[s.right_key] and (not s.left_key or not self.keys[s.left_key]):
                    s.change_x = s.right_speed
                else:
                    s.change_x = 0
                if s.up_key and self.keys[s.up_key] and (not s.down_key or not self.keys[s.down_key]):
                    s.change_y = s.up_speed
                elif s.down_key and self.keys[s.down_key] and (not s.up_key or not self.keys[s.up_key]):
                    s.change_y = -s.down_speed
                else:
                    s.change_y = 0
        self.sprites.update()

    # def run(self):
    #     mod = sys.modules['__main__']
    #     if hasattr(mod, 'setup'):
    #         mod.setup()
    #     super().run()

    def over(self):
        self.running = False

    def on_key_press(self, key, m):
        for n, k in _KEY_MAPPING.items():
            if key == k:
                self.keys[n] = True
        if not self.running and key == _KEY_MAPPING["enter"]:
            self.setup()

    def on_key_release(self, key, m):
        for n, k in _KEY_MAPPING.items():
            if key == k:
                self.keys[n] = False


class CommonActor:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.left_key = None
        self.right_key = None
        self.down_key = None
        self.up_key = None
        self.left_speed = self.right_speed = self.up_speed = self.down_speed = 0

    def move_left(self, key, speed=3):
        self.left_key = key
        self.left_speed = speed

    def move_right(self, key, speed=3):
        self.right_key = key
        self.right_speed = speed

    def move_up(self, key, speed=3):
        self.up_key = key
        self.up_speed = speed

    def move_down(self, key, speed=3):
        self.down_key = key
        self.down_speed = speed

    def touch(self, target):
        if isinstance(target, Sprite):
            return self.collides_with_sprite(target)
        if isinstance(target, SpriteList):
            return self.collides_with_list(target)
        return False

    def move_to(self, target, speed):
        angle = get_angle_radians(self.center_x, self.center_y, target.center_x, target.center_y)
        self.center_x += math.sin(angle) * speed
        self.center_y += math.cos(angle) * speed


class Actor(CommonActor, Sprite):
    pass


class ActorCircle(CommonActor, SpriteCircle):
    pass


class ActorRect(CommonActor, SpriteSolidColor):
    pass


class Actors(SpriteList):
    def __init__(self):
        super().__init__()

    def move_to(self, target, speed):
        for s in self:
            s.move_to(target, speed)

