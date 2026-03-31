import os
import numpy as np

INPUT_FOLDER = "dataset"
OUTPUT_FOLDER = "dataset_processed"
TARGET_LEN = 100

def load_csv(file):
    return np.loadtxt(file, delimiter=',')

def resample(data, target_len):
    indices = np.linspace(0, len(data)-1, target_len).astype(int)
    return data[indices]

def normalize(data):
    mean = np.mean(data, axis=0)
    std = np.std(data, axis=0) + 1e-8
    return (data - mean) / std

for label in ['A', 'B', 'C']:
    input_path = os.path.join(INPUT_FOLDER, label)
    output_path = os.path.join(OUTPUT_FOLDER, label)

    os.makedirs(output_path, exist_ok=True)

    files = sorted(os.listdir(input_path))[:10]

    for i, file in enumerate(files):
        file_path = os.path.join(input_path, file)

        data = load_csv(file_path)

        if len(data) < 20:
            continue

        data = resample(data, TARGET_LEN)
        data = normalize(data)

        save_path = os.path.join(output_path, f"{label}_{i+1}.csv")
        np.savetxt(save_path, data, delimiter=',')

print("✅ Processed dataset created safely!")