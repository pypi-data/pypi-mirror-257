import random
from .constants import _KEY_MAPPING, _IMAGES_MAPPING, _IMAGES_NAMES, _KEY_MAPPING_REVERSE
from .resources import resolve_resource_path
from arcade import Window, Sprite, SpriteList, SpriteCircle, SpriteSolidColor, Camera, PhysicsEnginePlatformer
from arcade import get_angle_radians, draw_text, schedule, unschedule, get_distance_between_sprites, get_distance
import sys
from time import time
import math


class Game(Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        self.game_time = 0
        self.running = True
        self.start_time = time()
        self.start_key = None
        self.mouse_x = self.mouse_y = 0
        self.sprites = SpriteList()
        self.camera = GameCamera()
        self.keys = {key: False for key in _KEY_MAPPING}

    def setup(self):
        for s in self.sprites:
            s.position = s.setup_position

    def get_position_from_str(self, sprite, pos):
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
        elif pos == "rand_in":
            position = random.randint(0, self.width), random.randint(0, self.height)
        elif pos == "rand_out":
            while True:
                position = random.randint(-self.width, self.width * 2), random.randint(-self.height,
                                                                                       self.height * 2)
                if not (0 <= position[0] <= self.width and 0 <= position[1] <= self.height):
                    break
        elif pos == "rand_down":
            position = random.randint(int(sprite.width // 2), int(self.width - sprite.width // 2)), \
                       random.randint(-int(sprite.height // 2) - self.height // 2, -int(sprite.height // 2))
        elif pos == "rand_up":
            position = random.randint(int(sprite.width // 2), int(self.width - sprite.width // 2)), \
                       random.randint(int(sprite.height // 2) + self.height,
                                      int(sprite.height // 2) + self.height * 3 // 2)
        elif pos == "rand_left":
            position = random.randint(-int(sprite.width // 2) - self.width // 2, -int(sprite.width // 2)), \
                       random.randint(int(sprite.height // 2), self.height - int(sprite.height // 2))
        elif pos == "rand_right":
            position = random.randint(int(sprite.width // 2) + self.width,
                                      int(sprite.width // 2) + self.width * 3 // 2), \
                       random.randint(int(sprite.height // 2), self.height - int(sprite.height // 2))
        else:
            position = self.width // 2, self.height // 2
        return position

    def add_sprite(self, name, pos="center"):
        path = name
        if name.startswith('image:'):
            if name[6:] in _IMAGES_NAMES:
                path = resolve_resource_path('{}.png'.format(name))
            elif name in _IMAGES_MAPPING:
                path = _IMAGES_MAPPING[name]
        sprite = Actor(path)
        if isinstance(pos, str):
            position = self.get_position_from_str(sprite, pos)
        else:
            position = pos
        sprite.position = sprite.setup_position = position
        sprite.game = self
        self.sprites.append(sprite)
        return sprite

    def add_sprites(self, name=None, pos="center", num=0, int_x=0, int_y=0):
        sprites = Actors()
        for i in range(num):
            s = self.add_sprite(name, pos)
            s.center_x += int_x * i
            s.center_y += int_y * i
            sprites.append(s)
        sprites.game = self
        return sprites

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
        self.camera.use()
        self.sprites.draw()
        mod = sys.modules['__main__']
        if hasattr(mod, 'draw'):
            mod.draw()

    def draw_text(self, text, *args, **kwargs):
        pos = [20, self.height - 40]
        size = 12
        if args:
            pos = args[:2]
            if len(args) > 2:
                size = args[2]
        if kwargs:
            if 'size' in kwargs:
                size = kwargs['size']
        draw_text(text, self.camera.left + pos[0], self.camera.down + pos[1], font_size=size)

    def on_update(self, delta_time):
        if not self.running:
            return
        self.game_time = round(time() - self.start_time, 2)
        mod = sys.modules['__main__']
        if hasattr(mod, 'update'):
            mod.update()
        for s in self.sprites:
            if s.left_key or s.right_key:
                if s.left_key and self.keys[s.left_key] and (not s.right_key or not self.keys[s.right_key]):
                    s.change_x = -s.left_speed
                elif s.right_key and self.keys[s.right_key] and (not s.left_key or not self.keys[s.left_key]):
                    s.change_x = s.right_speed
                else:
                    s.change_x = 0
            if s.up_key or s.down_key:
                if s.up_key and self.keys[s.up_key] and (not s.down_key or not self.keys[s.down_key]):
                    s.change_y = s.up_speed
                elif s.down_key and self.keys[s.down_key] and (not s.up_key or not self.keys[s.up_key]):
                    s.change_y = -s.down_speed
                else:
                    s.change_y = 0
        self.sprites.update()
        self.camera.update_position()

    def repeat_wrapper(self, t):
        mod = sys.modules['__main__']
        if hasattr(mod, 'repeat'):
            mod.repeat()

    def repeat(self, t):
        schedule(self.repeat_wrapper, t)

    def run(self):
        mod = sys.modules['__main__']
        if hasattr(mod, 'setup'):
            mod.setup()
        super().run()

    def over(self):
        self.running = False

    def set_start(self, key):
        self.start_key = key

    def on_key_press(self, key, m):
        for n, k in _KEY_MAPPING.items():
            if key == k:
                self.keys[n] = True
        if (not self.running and key == _KEY_MAPPING["enter"]) or \
                (self.start_key and key == _KEY_MAPPING[self.start_key]):
            self.running = True
            self.start_time = time()
            unschedule(self.repeat_wrapper)
            self.camera.reset()
            mod = sys.modules['__main__']
            if hasattr(mod, 'setup'):
                mod.setup()
            else:
                self.setup()
        for s in self.sprites:
            if s.left_press and key == _KEY_MAPPING[s.left_press]:
                s.change_x = -s.left_speed
            if s.right_press and key == _KEY_MAPPING[s.right_press]:
                s.change_x = s.right_speed
            if s.up_press and key == _KEY_MAPPING[s.up_press]:
                s.change_y = s.up_speed
            if s.down_press and key == _KEY_MAPPING[s.down_press]:
                s.change_y = -s.down_speed
        mod = sys.modules['__main__']
        if hasattr(mod, 'key_press'):
            mod.key_press(_KEY_MAPPING_REVERSE[key])

    def on_key_release(self, key, m):
        for n, k in _KEY_MAPPING.items():
            if key == k:
                self.keys[n] = False

    def on_mouse_motion(self, x, y, dx, dy):
        self.mouse_x = x
        self.mouse_y = y

    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):
        if not self.running:
            return
        mod = sys.modules['__main__']
        if hasattr(mod, 'mouse_click'):
            mod.mouse_click()


class CommonActor:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.left_key = self.right_key = self.down_key = self.up_key = None
        self.left_press = self.right_press = self.down_press = self.up_press = None
        self.left_speed = self.right_speed = self.up_speed = self.down_speed = 0
        self.engine = None

    @property
    def x(self):
        return self.center_x

    @property
    def y(self):
        return self.center_y

    @x.setter
    def x(self, value):
        self.center_x = value

    @y.setter
    def y(self, value):
        self.center_y = value

    def move_left(self, key=None, speed=3, way="press"):
        if key:
            if way == "press":
                self.left_key = key
                self.left_speed = speed
            if way == "once":
                self.left_press = key
                self.left_speed = speed
        else:
            self.change_x = -speed

    def move_right(self, key=None, speed=3, way="press"):
        if key:
            if way == "press":
                self.right_key = key
                self.right_speed = speed
            if way == "once":
                self.right_press = key
                self.right_speed = speed
        else:
            self.change_x = speed

    def move_up(self, key=None, speed=3, way="press"):
        if key:
            if way == "press":
                self.up_key = key
                self.up_speed = speed
            if way == "once":
                self.up_press = key
                self.up_speed = speed
        else:
            self.change_y = speed

    def move_down(self, key=None, speed=3, way="press"):
        if key:
            if way == "press":
                self.down_key = key
                self.down_speed = speed
            if way == "once":
                self.down_press = key
                self.down_speed = speed
        else:
            self.change_y = -speed

    def touch(self, target):
        if isinstance(target, Sprite):
            if self.collides_with_sprite(target):
                return target
        if isinstance(target, SpriteList):
            sprites = Actors()
            for s in self.collides_with_list(target):
                sprites.append(s)
            return sprites
        return False

    def coincide(self, target):
        if get_distance_between_sprites(self, target) < math.sqrt(self.change_x ** 2 + self.change_y ** 2):
            self.position = target.position
            return True
        return False

    def move_to(self, target, speed):
        if isinstance(target, Sprite):
            angle = get_angle_radians(self.center_x, self.center_y, target.center_x, target.center_y)
        else:
            angle = get_angle_radians(self.center_x, self.center_y, target[0], target[1])
        self.change_x = math.sin(angle) * speed
        self.change_y = math.cos(angle) * speed

    def rand_speed(self, a, b):
        current_speed_magnitude = math.sqrt(self.change_x ** 2 + self.change_y ** 2)
        if current_speed_magnitude != 0:
            new_speed_magnitude = random.uniform(a, b)
            ratio = new_speed_magnitude / current_speed_magnitude
            self.change_x *= ratio
            self.change_y *= ratio
        else:
            angle = random.uniform(0, 2 * math.pi)
            self.change_x = math.cos(angle) * random.uniform(a, b)
            self.change_y = math.sin(angle) * random.uniform(a, b)

    def rand_x(self, a, b):
        self.center_x = random.uniform(a, b)

    def rand_y(self, a, b):
        self.center_y = random.uniform(a, b)

    def rotate(self, speed):
        self.change_angle = speed

    def rand_angle(self):
        self.angle = random.randint(0, 359)

    def hide(self):
        self.visible = False

    def reset(self):
        self.game.sprites.remove(self)
        self.game.sprites.append(self)

    def get_score(self, x, y, ran=(0, 10)):
        if self.collides_with_point((x, y)):
            dis = get_distance(x, y, self.x, self.y)
            radius = math.sqrt((self.width // 2) ** 2 + (self.height // 2) ** 2)
            score = math.ceil(ran[0] + (radius - dis) / radius * (ran[1] - ran[0]))
            return int(score)
        return 0

    def touch_point(self, x, y):
        return self.collides_with_point((x, y))

    def set_engine(self, g=0.5, p=None):
        self.engine = PhysicsEnginePlatformer(self, gravity_constant=g, platforms=p)
    
    def update(self):
        if self.engine:
            self.engine.update()
        else:
            super().update()
    
    def jump(self, speed):
        if self.engine:
            self.engine.jump(speed)
    

class Actor(CommonActor, Sprite):
    def copy(self):
        new_sprite = Actor(texture=self.texture)
        new_sprite.position = self.position
        new_sprite.angle = self.angle
        new_sprite.game = self.game
        all_sprites = self.game.sprites
        self.game.sprites = Actors()
        for s in all_sprites:
            self.game.sprites.append(s)
            if s == self:
                self.game.sprites.append(new_sprite)
        return new_sprite


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

    def rotate(self, angle):
        for s in self:
            s.rotate(angle)

    def kill(self):
        for s in self:
            s.kill()

    def hide(self):
        for s in self:
            s.hide()

    def rand_angle(self, step=1):
        angles = list(range(0, 360, step))
        selected = random.sample(angles, len(self))
        for s, a in zip(self, selected):
            s.angle = a

    def set(self, name=None, pos="center", num=0, int_x=0, int_y=0):
        self.clear()
        sprites = self.game.add_sprites(name, pos, num, int_x, int_y)
        for s in sprites:
            self.append(s)

    def clear(self):
        for s in self:
            s.game.sprites.remove(s)
        super().clear()

    def touch_point(self, x, y):
        for s in reversed(self):
            if s.collides_with_point((x, y)):
                return s

    def get_score(self, x, y, ran=(0, 10)):
        for s in reversed(self):
            score = s.get_score(x, y, ran=ran)
            if score > 0:
                return score, s
        return 0, None

    def rand_speed(self, a, b):
        for s in self:
            s.rand_speed(a, b)

    def rand_x(self, a, b):
        for s in self:
            s.rand_x(a, b)

    def rand_y(self, a, b):
        for s in self:
            s.rand_y(a, b)


class GameCamera(Camera):
    def __init__(self):
        super().__init__()
        self.left = self.down = 0
        self.right = self.viewport_width
        self.up = self.viewport_height
        self.change_x = self.change_y = 0

    def move_up(self, speed):
        self.change_y = speed

    def move_down(self, speed):
        self.change_y = -speed

    def move_left(self, speed):
        self.change_x = -speed

    def move_right(self, speed):
        self.change_x = speed

    def update_position(self):
        if self.change_x or self.change_y:
            next_pos = (self.left + self.change_x, self.down + self.change_y)
            self.move(next_pos)
            self.left += self.change_x
            self.right += self.change_x
            self.up += self.change_y
            self.down += self.change_y

    def reset(self):
        self.left = self.down = 0
        self.right = self.viewport_width
        self.up = self.viewport_height
        self.change_x = self.change_y = 0
        self.move((0, 0))
