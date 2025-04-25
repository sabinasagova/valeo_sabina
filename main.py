from pathlib import Path
from f_cam import FrontCameraSimulator # Imports the camera simulator from another file/module called f_cam.py
from sensor import SensorSimulator
from resim import ReprocessingDevice

def main():
    output_dir = Path.cwd() # Get the current working directory (the folder you're running the script from) "current working directory"
    f_cam_out = output_dir / "f_cam_out.csv" # The output file for the front camera data
    sensor_out = output_dir / "sensor_out.csv"
    resim_out = output_dir / "resim_out.csv"

    print("Generating f_cam data...") # Just a message so the user knows what's happening
    cam = FrontCameraSimulator(f_cam_out) # Create a camera simulator with the output path
    cam.save_to_csv() # Generate and save the front camera data into the CSV

    print("Generating sensor data...")
    sensor = SensorSimulator(sensor_out)
    sensor.save_to_csv()

    print("Processing resim data...")
    resim = ReprocessingDevice(f_cam_out, sensor_out, resim_out)
    resim.process()

    print("Done. Output saved to:", resim_out) # Let the user know everything is complete, and where the final file is saved

if __name__ == "__main__":
    main() # Call the main function to run everything