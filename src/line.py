import csv
from src.station import Station


class Line:
    def __init__(self):
        self.stations = []
        self.segments = []

    def load_stations(self, path):
        with open(path, "r", encoding="utf-8-sig") as file:
            reader = csv.DictReader(file)

            for row in reader:
                station = Station(
                    id=int(row["id"]),
                    name=row["name"],
                    km=float(row["km"]),
                    express_stop=row["express_stop"] == "True"
                )

                self.stations.append(station)

    def load_segments(self, path):
        with open(path, "r", encoding="utf-8-sig") as file:
            reader = csv.DictReader(file)

            for row in reader:
                self.segments.append({
                    "from": int(row["from_id"]),
                    "to": int(row["to_id"]),
                    "distance": float(row["distance_m"]),
                    "speed_limit": float(row["speed_limit"]),
                    "dwell_time": int(row["dwell_time"])
                })