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
    def __init__(self, spawn_loc, start_wave=1, interwave=2):
        self.spawn_loc = spawn_loc
        self.current_wave_number = start_wave
        self.interwave = 60 * interwave
        self.delay = 0
        self.current_wave = None

    def update(self, enemies):
        if self.current_wave is None:
            self.delay = self.interwave
            self.current_wave = Wave(self.current_wave_number, self.spawn_loc)
            pygame.event.post(pygame.event.Event(WAVE_STARTED, wave=self.current_wave))
        elif self.current_wave.enemies > 0:
            self.current_wave.update(enemies)
        elif len(enemies.sprites()) <= 0 and self.delay > 0:
            self.delay -= 1
        elif len(enemies.sprites()) <= 0 and self.delay <= 0:
            self.current_wave = None
            self.current_wave_number += 1
