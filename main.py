from pico2d import *


open_canvas(800, 600)

running = True

while running:
    for event in get_events():
        if event.type == SDL_QUIT or (event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE):
            running = False

    delay(0.01)

close_canvas()