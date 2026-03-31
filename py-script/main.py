import serial
import os

PORT = '/dev/cu.usbserial-0001'
BAUD = 115200

label = input("Enter label (A/B/C): ").upper()

ser = serial.Serial(PORT, BAUD)

os.makedirs(f"dataset/{label}", exist_ok=True)

sample_count = 1
recording = False
data = []

print("Waiting for button presses...")

while True:
    line = ser.readline().decode(errors='ignore').strip()

    if line == "START":
        print(f"\nRecording sample {sample_count}...")
        recording = True
        data = []

    elif line == "END":
        print("Saving sample...")

        filename = f"dataset/{label}/{label}_{sample_count}.csv"
        with open(filename, "w") as f:
            for row in data:
                f.write(row + "\n")

        print(f"Saved: {filename} ({len(data)} rows)")

        sample_count += 1
        recording = False

    elif recording:
        parts = line.split(',')
        if len(parts) == 6:
            data.append(line)