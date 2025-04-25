import csv # Lets us write data into a .csv file
import random # Helps us generate random numbers (to make the simulation feel more real)
from pathlib import Path # A safer way to handle file paths (like where to save the CSV)

# a "Front Camera Simulator" that can generate and save fake data
class FrontCameraSimulator:
    # an instance of the simulator
    def __init__(self, output_path: Path, start_time=100.0, num_frames=2000):
        self.output_path = output_path
        self.start_time = start_time
        self.num_frames = num_frames
    # the heart of the simulator
    def generate_data(self):
        data = []
        timestamp = self.start_time
        speed = 60.0 # starting speed
        frame_id = 100
        signal1_value = 0
        signal1_set = False

        for i in range(self.num_frames):
            jitter = random.uniform(-0.00005, 0.00005) # small random number to make the data feel more real
            timestamp += 0.0277 + jitter
            timestamp = round(timestamp, 6)

            current_frame = frame_id + i

            if speed < 120.0:
                speed = round(speed + 0.08, 2)  # increase the speed slowly until it hits a limit (120.0), 2 is how many digits to keep after the decimal point
            else:
                speed = round(120.0 + random.uniform(-0.05, 0.05), 2)

            yaw_rate = round(random.uniform(-1.0, 1.0), 2)

            if current_frame > 200 and not signal1_set:
                signal1_value = random.randint(1, 15) # choose a random signal1 value between 1 and 15
                signal1_set = True # make sure we only set it once

            signal2 = 0 # default value
            if signal1_value >= 5:
                signal2 = round(80 + random.uniform(-10, 10))  # add some randomness around 80 if signal1 is strong enough

            data.append([
                timestamp, current_frame, speed, yaw_rate, signal1_value, signal2 #  save this frame’s data as a row
            ])
        return data

    def save_to_csv(self):
        data = self.generate_data() # create the data
        with open(self.output_path, mode="w", newline="") as file:
            writer = csv.writer(file) # create CSV writer
            writer.writerow(["Timestamp", "FrameID", "Speed", "YawRate", "Signal1", "Signal2"]) # write column headers
            writer.writerows(data) # write all the data rows

if __name__ == "__main__":
    import argparse # lets us take input when running the script
    parser = argparse.ArgumentParser(description="Simulate Front Camera Device") # description for the help message
    parser.add_argument("output", type=str, help="Path to output CSV file")
    args = parser.parse_args()
    # python f_cam.py f_cam_out.csv
    simulator = FrontCameraSimulator(Path(args.output))
    simulator.save_to_csv()