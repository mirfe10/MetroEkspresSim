from dataclasses import dataclass

@dataclass
class Station:
    id: int
    name: str
    km: float

    express_stop: bool = False

    has_pocket_track: bool = True

    dwell_time: int = 20

    main_line_occupied: bool = False

    pocket_track_occupied: bool = False