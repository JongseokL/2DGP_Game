from pico2d import *
from map import Map
from car import Car
from civilian import CivilianTraffic
from oil import OilWeapon
from mine import MineWeapon


open_canvas(1100, 880)
road_map = Map()
player_car = Car()
traffic = CivilianTraffic()
oil_weapon = OilWeapon()
mine_weapon = MineWeapon()
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
            oil_weapon.handle_event(event, player_car)
            mine_weapon.handle_event(event, player_car)

    if not running:
        break
    player_car.update(frame_time)
    road_map.update(player_car.travel_distance)
    oil_weapon.update(frame_time, player_car.travel_distance)
    mine_weapon.update(frame_time, player_car.travel_distance)
    traffic.update(frame_time, player_car.travel_distance)
    clear_canvas()
    road_map.draw()
    oil_weapon.draw()
    mine_weapon.draw()
    traffic.draw()
    player_car.draw()
    update_canvas()
    delay(0.01)

close_canvas()
