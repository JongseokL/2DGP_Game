from pico2d import *
from map import Map
from car import Car


open_canvas(1350, 1080)

road_map = Map()
player_car = Car()
running = True

while running:
    for event in get_events():
        if event.type == SDL_QUIT or (event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE):
            running = False

    clear_canvas()
    road_map.draw()
    player_car.draw()
    update_canvas()

    delay(0.01)

close_canvas()
