class Dispatcher:
    def __init__(self, simulation):
        self.simulation = simulation

    def update(self):
        for train in self.simulation.trains:
            self._control_train(train)

    def is_in_pocket_track(self, train):
        if train.train_type == "EXPRESS":
            return False
        # Local train is in pocket track if it's close to a station (within 150m)
        for station in self.simulation.line.stations:
            station_pos_m = station.km * 1000
            if abs(train.position_m - station_pos_m) < 150:
                return True
        return False

    def _get_train_ahead(self, train):
        closest_train = None
        min_dist = float('inf')
        
        for other in self.simulation.trains:
            if other == train: continue
            
            dist = other.position_m - train.position_m
            if 0 < dist < min_dist:
                # If 'train' is EXPRESS, it ignores LOCAL trains that are in pocket tracks
                if train.train_type == "EXPRESS" and self.is_in_pocket_track(other):
                    continue
                
                closest_train = other
                min_dist = dist
                
        return closest_train

    def _get_next_stop(self, train):
        current_km = train.current_station.km if train.current_station else -1.0
        for station in self.simulation.line.stations:
            # Look for stations strictly after the current station
            if station.km > current_km: 
                if train.train_type == "LOCAL":
                    return station
                elif train.train_type == "EXPRESS" and station.express_stop:
                    return station
        return None

    def _is_express_approaching(self, local_train, current_station):
        if not current_station:
            return False
            
        # Eğer bulunduğumuz durak zaten bir ekspres durağıysa, arkaya bakmadan çık.
        # Çünkü ekspres tren transit geçmeyecek, bu durağa yanaşacak.
        if current_station.express_stop:
            return False
            
        current_idx = -1
        for i, station in enumerate(self.simulation.line.stations):
            if station.id == current_station.id:
                current_idx = i
                break
                
        if current_idx <= 0:
            return False  # İlk istasyonda beklemeye gerek yok
            
        previous_station = self.simulation.line.stations[current_idx - 1]
        previous_station_pos_m = previous_station.km * 1000
        
        for express in self.simulation.trains:
            if express.train_type != "EXPRESS": continue
            
            # Eğer ekspres tren önceki istasyona vardıysa (veya geçtiyse) ve hala bizim arkamızdaysa
            if previous_station_pos_m <= express.position_m < local_train.position_m:
                # Seçilen Kural: Ekspres durakta kapıları açık bekliyorsa (DWELL), lokal tren onu beklemesin.
                if express.state == "DWELL":
                    continue
                    
                # Hızlanmaya Hazırlık Kuralı: Ekspres tren 150 metreden daha fazla yaklaştıysa,
                # lokal tren kapılarını kapatıp kalkışa başlasın. Zaten kendi 150 metrelik 
                # cep hattından çıkana kadar ekspres onu çoktan geçmiş olacak.
                if local_train.position_m - express.position_m <= 150:
                    continue
                    
                return True
                
        return False

    def _control_train(self, train):
        # 1. State Management at Stations
        current_station = None
        for station in self.simulation.line.stations:
            if abs(train.position_m - (station.km * 1000)) < 1.0 and train.speed < 0.1:
                current_station = station
                break
                
        if current_station and train.state == "RUNNING":
            # Train has just arrived
            train.state = "DWELL"
            train.timer = current_station.dwell_time
            train.current_station = current_station
            print(f"[{self.simulation.time}s] {train.id} ({train.train_type}) arrived at {current_station.name}")

        if train.state in ["DWELL", "WAITING_FOR_EXPRESS"]:
            if train.train_type == "LOCAL":
                if self._is_express_approaching(train, current_station):
                    if train.state != "WAITING_FOR_EXPRESS":
                        print(f"[{self.simulation.time}s] {train.id} is WAITING FOR EXPRESS at {current_station.name}")
                    train.state = "WAITING_FOR_EXPRESS"
                else:
                    if train.timer <= 0:
                        train.state = "RUNNING"
                        print(f"[{self.simulation.time}s] {train.id} departed {current_station.name}")
                    else:
                        train.state = "DWELL"
            else:
                # Express train
                if train.timer <= 0:
                    train.state = "RUNNING"
                    print(f"[{self.simulation.time}s] {train.id} departed {current_station.name}")

        # 2. Movement Authority (if running)
        if train.state == "RUNNING":
            train_ahead = self._get_train_ahead(train)
            
            # End of line
            authority_m = self.simulation.line.stations[-1].km * 1000
            
            # Traffic ahead
            if train_ahead:
                safe_distance_m = train_ahead.position_m - 200
                if safe_distance_m < authority_m:
                    authority_m = safe_distance_m
                    
            # Next stop
            next_station = self._get_next_stop(train)
            if next_station:
                station_pos_m = next_station.km * 1000
                if station_pos_m <= authority_m:
                    train.target_stop_m = station_pos_m
                else:
                    train.target_stop_m = authority_m
            else:
                train.target_stop_m = authority_m