from dataclasses import dataclass
from src.station import Station

@dataclass
class Train:
    id: str
    train_type: str  # "LOCAL" or "EXPRESS"
    current_station: Station
    
    position_m: float = 0.0
    speed: float = 0.0  # m/s
    
    # Physics parameters
    acceleration: float = 1.0  # m/s^2
    deceleration: float = 1.0  # m/s^2
    max_speed: float = 22.22  # m/s (80 km/h)
    
    # State management
    state: str = "DWELL"  # DWELL, WAITING_FOR_EXPRESS, RUNNING
    timer: int = 20
    
    # Control variables set by dispatcher
    target_stop_m: float = 0.0
    speed_limit: float = 22.22
    
    def update(self):
        if self.state in ["DWELL", "WAITING_FOR_EXPRESS"]:
            if self.timer > 0:
                self.timer -= 1
            # Dispatcher changes state to RUNNING when safe to depart.
            self.speed = 0.0
            
        elif self.state == "RUNNING":
            distance_to_target = self.target_stop_m - self.position_m
            
            # If target is behind us somehow, we must stop immediately
            if distance_to_target <= 0.5:
                self.position_m = self.target_stop_m
                self.speed = 0.0
            else:
                # Calculate required braking distance
                # v^2 = u^2 + 2as => distance = v^2 / (2a)
                braking_distance = (self.speed ** 2) / (2 * self.deceleration)
                
                # Add a small buffer to braking distance to ensure we stop in time
                if distance_to_target <= braking_distance + (self.speed * 1.0): 
                    # Brake
                    self.speed = max(0.0, self.speed - self.deceleration)
                else:
                    # Accelerate
                    target_speed = min(self.max_speed, self.speed_limit)
                    if self.speed < target_speed:
                        self.speed = min(target_speed, self.speed + self.acceleration)
                    elif self.speed > target_speed:
                        self.speed = max(target_speed, self.speed - self.deceleration)
                        
            # Update position
            self.position_m += self.speed