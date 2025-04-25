import csv
import random # Helps us create random values to make the data more realistics
from pathlib import Path

class SensorSimulator:
    def __init__(self, output_path: Path, start_time=100.0, max_time=160.0):
        self.output_path = output_path # Where we will save the file
        self.start_time = start_time # When the data starts (in seconds)
        self.max_time = max_time # When the data should stop

    def generate_data(self):
        data = [] # Where we will store all the rows
        timestamp = self.start_time
        speed = 60.0 # Start at 60 km/h 

        while timestamp < self.max_time:
            jitter = random.uniform(-0.01, 0.01)
            timestamp += 0.2 + jitter
            timestamp = round(timestamp, 6)

            if speed < 120.0:
                speed = round(speed + 0.56, 2)
            else:
                speed = round(120.0 + random.uniform(-0.1, 0.1), 2)

            data.append([timestamp, speed])
        return data

    def save_to_csv(self):
        data = self.generate_data()
        with open(self.output_path, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Timestamp", "Speed"])
            writer.writerows(data)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Simulate Sensor Device")
    parser.add_argument("output", type=str, help="Path to output CSV file")
    args = parser.parse_args()
    # python sensor.py sensor_out.csv
    simulator = SensorSimulator(Path(args.output))
    simulator.save_to_csv()