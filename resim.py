import csv # Lets us read and write CSV files 
from pathlib import Path

class ReprocessingDevice:
    def __init__(self, f_cam_path: Path, sensor_path: Path, output_path: Path):
        self.f_cam_path = f_cam_path
        self.sensor_path = sensor_path
        self.output_path = output_path

    def load_sensor_data(self):
        with open(self.sensor_path, newline="") as file:
            reader = csv.DictReader(file)  # reads CSV as a list of dictionaries
            return [(float(row["Timestamp"]), float(row["Speed"])) for row in reader]

    def load_f_cam_data(self):
        with open(self.f_cam_path, newline="") as file:
            reader = csv.DictReader(file)
            return list(reader) # keep each row as a dictionary

    def find_latest_sensor_speed(self, sensor_data, cam_timestamp):
        latest_speed = 0
        for timestamp, speed in sensor_data:
            if timestamp <= cam_timestamp:
                latest_speed = speed # update if sensor timestamp is before or equal to the camera frame
            else:
                break # stop once we pass the current camera timestamp
        return latest_speed

    def process(self):
        sensor_data = self.load_sensor_data() # get list of (timestamp, speed)
        cam_data = self.load_f_cam_data() # get list of dictionaries from the camera CSV

        with open(self.output_path, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Timestamp", "FrameID", "Speed", "YawRate", "Signal1", "Signal2"])

            for row in cam_data:
                cam_ts = float(row["Timestamp"])
                cam_speed = float(row["Speed"])
                sensor_speed = self.find_latest_sensor_speed(sensor_data, cam_ts) # get matching sensor speed
                avg_speed = round((cam_speed + sensor_speed) / 2, 2) # average the two speeds, round to 2 decimal places
                writer.writerow([row["Timestamp"], row["FrameID"], avg_speed, row["YawRate"], row["Signal1"], row["Signal2"]])

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Reprocessing Device")
    parser.add_argument("f_cam", type=str, help="Path to f_cam_out.csv")
    parser.add_argument("sensor", type=str, help="Path to sensor_out.csv")
    parser.add_argument("output", type=str, help="Path to resim_out.csv")
    args = parser.parse_args()
    # python resim.py f_cam_out.csv sensor_out.csv resim_out.csv
    processor = ReprocessingDevice(Path(args.f_cam), Path(args.sensor), Path(args.output))
    processor.process()