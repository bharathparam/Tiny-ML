import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv1D, Dense, Flatten, MaxPooling1D

# load saved data (reuse your preprocess code here)
from preprocess import process_folder

X, y = process_folder("dataset_processed")

# encode labels (A, B, C → 0,1,2)
encoder = LabelEncoder()
y_encoded = encoder.fit_transform(y)

# split data
X_train, X_test, y_train, y_test = train_test_split(
    X, y_encoded, test_size=0.2, random_state=42
)

# build model
model = Sequential([
    Conv1D(32, 3, activation='relu', input_shape=(100, 6)),
    MaxPooling1D(2),
    Conv1D(64, 3, activation='relu'),
    Flatten(),
    Dense(64, activation='relu'),
    Dense(3, activation='softmax')
])

model.compile(
    optimizer='adam',
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)

# train
model.fit(X_train, y_train, epochs=20, validation_data=(X_test, y_test))

# evaluate
loss, acc = model.evaluate(X_test, y_test)
print("Test Accuracy:", acc)
model.save("model.h5")