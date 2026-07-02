from src.dispatcher import Dispatcher
from src.train import Train

class Simulation:
    def __init__(self, line):
        self.line = line
        self.time = 0
        self.trains = []
        self.dispatcher = Dispatcher(self)
        
        self.spawn_timer = 0
        self.spawn_interval = 180
        self.trains_spawned = 0
        self.max_trains = 30

    def add_train(self, train):
        self.trains.append(train)
        
    def _spawn_train(self):
        if self.trains_spawned >= self.max_trains:
            return
            
        if self.spawn_timer <= 0:
            # Check if starting position is safe (no train within 200m)
            safe = True
            for t in self.trains:
                if t.position_m < 200:
                    safe = False
                    break
                    
            if safe:
                t_type = "EXPRESS" if self.trains_spawned % 2 == 1 else "LOCAL"
                t_id = f"{t_type[0]}{self.trains_spawned // 2 + 1}"
                
                new_train = Train(
                    id=t_id,
                    train_type=t_type,
                    current_station=self.line.stations[0],
                    position_m=0.0,
                    state="DWELL",
                    timer=20
                )
                self.add_train(new_train)
                print(f"[{self.time}s] Spawner: Deployed {t_id} ({t_type}) at {self.line.stations[0].name}")
                
                self.trains_spawned += 1
                self.spawn_timer = self.spawn_interval
        else:
            self.spawn_timer -= 1

    def _remove_finished_trains(self):
        last_station = self.line.stations[-1]
        last_pos_m   = last_station.km * 1000
        to_remove = []
        for train in self.trains:
            # Son istasyonda DWELL tamamlandıysa (timer bitti) çıkar
            if (train.current_station and
                    train.current_station.id == last_station.id and
                    train.state == "DWELL" and
                    train.timer <= 0):
                to_remove.append(train)

        for train in to_remove:
            self.trains.remove(train)
            print(f"[{self.time}s] {train.id} ({train.train_type}) hattan çıktı ({last_station.name})")

    def tick(self):
        self._spawn_train()
        self.dispatcher.update()
        for train in self.trains:
            train.update()
        self._remove_finished_trains()
        self.time += 1

    def run(self, seconds):
        print("Starting Simulation...")
        for _ in range(seconds):
            self.tick()
        print(f"Simulation finished. Time = {self.time} seconds")