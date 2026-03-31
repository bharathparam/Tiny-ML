import os
import numpy as np

TARGET_LEN = 100

def load_csv(file):
    return np.loadtxt(file, delimiter=',')

def resample(data, target_len):
    indices = np.linspace(0, len(data)-1, target_len).astype(int)
    return data[indices]

def process_folder(folder):
    X = []
    y = []

    for label in ['A', 'B', 'C']:   # fixed labels
        path = os.path.join(folder, label)

        files = sorted(os.listdir(path))[:10]  # take ONLY 10 samples

        for file in files:
            file_path = os.path.join(path, file)

            data = load_csv(file_path)

            if len(data) < 20:
                continue

            data = resample(data, TARGET_LEN)

            X.append(data)
            y.append(label)

    return np.array(X), np.array(y)

X, y = process_folder("dataset")

print("Shape:", X.shape)
print("Labels count:", {label: list(y).count(label) for label in set(y)})