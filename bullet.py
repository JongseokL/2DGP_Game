from pathlib import Path

from pico2d import load_image, SDL_KEYDOWN, SDL_KEYUP, SDLK_p


class BulletWeapon:
    def __init__(self):
        path = (Path(__file__).resolve().parent / 'assets' / 'images'
                / 'weapons' / 'bullet_v1.png')
        self.image = load_image(str(path))
        self.bullets = []
        self.key_down = False
        self.width = 3.5
        self.height = 16.25
        self.speed = 600.0

    def handle_event(self, event, car):
        # Beta: one rear-facing shot per press, ignoring keyboard auto-repeat.
        if event.type == SDL_KEYDOWN and event.key == SDLK_p:
            if not self.key_down:
                y = car.y - car.height / 2 - self.height / 2 - 4
                self.bullets.append([car.x, y])
                self.key_down = True
        elif event.type == SDL_KEYUP and event.key == SDLK_p:
            self.key_down = False

    def update(self, frame_time):
        # Projectile speed is relative to the player, independent of road scrolling.
        for bullet in self.bullets:
            bullet[1] -= self.speed * frame_time
        self.bullets = [bullet for bullet in self.bullets
                        if bullet[1] + self.height / 2 > 0]

    def draw(self):
        for x, y in self.bullets:
            self.image.clip_draw(567, 380, 120, 555,
                                 x, y, self.width, self.height)
