from pico2d import *
from map import Map
from car import Car


open_canvas(1100, 880)
road_map = Map()
player_car = Car()
running = True
previous_time = get_time()

while running:
    current_time = get_time()
    frame_time = min(current_time - previous_time, 0.05)
    previous_time = current_time

    for event in get_events():
        if event.type == SDL_QUIT or (event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE):
            running = False
        else:
            player_car.handle_event(event)

    if not running:
        break
    player_car.update(frame_time)
    clear_canvas()
    road_map.draw()
    player_car.draw()
    update_canvas()
    delay(0.01)

close_canvas()
