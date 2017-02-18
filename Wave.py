from Enemies import *


class Wave:
    def __init__(self, number, spawn_loc):
        self.number = number
        self.enemies = 2*number + 3
        self.delay = int(120/number)
        self.current_time = 0
        self.time_until_next_spawn = 0
        self.spawn_loc = spawn_loc

    def update(self, enemies):
        if self.time_until_next_spawn <= 0 and self.enemies >= 1:
            self.time_until_next_spawn = self.delay
            enemy = createEnemy(self.spawn_loc)
            enemies.add(enemy)
            self.enemies -= 1
        else:
            self.time_until_next_spawn -= 1


class WaveHandler:
    def __init__(self, spawn_loc, start_wave=0):
        self.spawn_loc = spawn_loc
        self.current_wave_number = start_wave
        self.current_wave = None
        self.in_wave = False

    def start_wave(self):
        self.in_wave = True
        self.current_wave_number += 1
        self.current_wave = Wave(self.current_wave_number, self.spawn_loc)

    def update(self, enemies):
        if self.in_wave:
            self.current_wave.update(enemies)

