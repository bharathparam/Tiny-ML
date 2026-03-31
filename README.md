# Tiny-ML
# ✍️ Air Writing Recognition using ESP32 + MPU6050 (Edge AI)

A real-time **air-writing recognition system** built using an **ESP32** and **MPU6050**, powered by a custom-trained machine learning model running **fully on-device (edge AI)**.

---

## 🚀 Overview

This project allows you to:

* Draw letters (A, B, C) in the air
* Capture motion using MPU6050 (accelerometer + gyroscope)
* Process data on ESP32
* Run inference using a TinyML model
* Predict the drawn letter in real time

👉 No internet required.
👉 Entire system runs on-device = **true edge computing**

---

## 🧠 System Pipeline

```text
MPU6050 → Data Collection → Preprocessing → ML Model → Prediction
```

---

## 🧰 Hardware Used

* ESP32
* MPU6050 (Accelerometer + Gyroscope)
* USB cable

---

## 🔌 Wiring

```text
MPU6050 → ESP32

VCC → 3.3V  
GND → GND  
SDA → GPIO21  
SCL → GPIO22  
```

---

## 📊 Data Collection

We collected motion data using ESP32 and saved it as CSV.

Each sample contains:

```text
ax, ay, az, gx, gy, gz
```

Each gesture = **100 timesteps**

---

### 📁 Dataset Structure

```text
dataset/
 ├── A/
 ├── B/
 ├── C/
```

Each folder contains multiple `.csv` files.

---

## ⚙️ Preprocessing

* Fixed sequence length → 100 samples
* 6 features per timestep
* Shape:

```text
(100, 6)
```

Flattened to:

```text
600 input features
```

---

## 🤖 Model Training

We trained a neural network using Python (TensorFlow/Keras).

### Example Model:

```python
model = Sequential([
    Flatten(input_shape=(100, 6)),
    Dense(64, activation='relu'),
    Dense(32, activation='relu'),
    Dense(3, activation='softmax')
])
```

---

## 🔄 Convert to TFLite

```python
converter = tf.lite.TFLiteConverter.from_keras_model(model)
tflite_model = converter.convert()

with open("model.tflite", "wb") as f:
    f.write(tflite_model)
```

---

## ⚡ Deployment (Edge Impulse)

Instead of manually handling TensorFlow Lite on ESP32:

👉 We used **Edge Impulse** for deployment

### Steps:

1. Upload `.tflite` model
2. Configure:

   * Input: `(100, 6)`
   * Output: `A, B, C`
   * Type: Classification
3. Select:

   ```text
   Deployment → Arduino Library
   ```
4. Download library
5. Install in Arduino IDE

---

## 💻 Arduino Code (Inference)

```cpp
#include <BHAIRAVA-project-1_inferencing.h>
#include <Wire.h>
#include <MPU6050.h>

MPU6050 mpu;

#define SAMPLES 100
#define FEATURES 600

float features[FEATURES];

void setup() {
  Serial.begin(115200);
  Wire.begin();

  mpu.initialize();

  if (!mpu.testConnection()) {
    Serial.println("MPU6050 failed!");
    while (1);
  }

  Serial.println("Ready. Press key to start...");
}

void loop() {

  if (Serial.available() == 0) return;
  Serial.read();

  Serial.println("Start gesture...");
  delay(500);

  int index = 0;

  for (int i = 0; i < SAMPLES; i++) {
    int16_t ax, ay, az, gx, gy, gz;
    mpu.getMotion6(&ax, &ay, &az, &gx, &gy, &gz);

    features[index++] = ax;
    features[index++] = ay;
    features[index++] = az;
    features[index++] = gx;
    features[index++] = gy;
    features[index++] = gz;

    delay(20);
  }

  signal_t signal;
  signal.total_length = FEATURES;

  signal.get_data = [](size_t offset, size_t length, float *out_ptr) {
    memcpy(out_ptr, features + offset, length * sizeof(float));
    return 0;
  };

  ei_impulse_result_t result;

  run_classifier(&signal, &result, false);

  Serial.println("Predictions:");

  int best = 0;
  float max_val = 0;

  for (size_t i = 0; i < EI_CLASSIFIER_LABEL_COUNT; i++) {
    Serial.print(result.classification[i].label);
    Serial.print(": ");
    Serial.println(result.classification[i].value);

    if (result.classification[i].value > max_val) {
      max_val = result.classification[i].value;
      best = i;
    }
  }

  Serial.print("Final: ");
  Serial.println(result.classification[best].label);
}
```

---

## 🧪 Testing Procedure

1. Open Serial Monitor
2. Press any key
3. Draw a letter in air
4. Wait for prediction

Example output:

```text
Predictions:
A: 0.82
B: 0.10
C: 0.08

Final: A
```

---

## ⚠️ Important Learnings

### 🔥 1. Data Consistency is EVERYTHING

```text
Training data ≠ Real data → Bad predictions
```

---

### 🔥 2. Normalization Matters

Model was trained on normalized data
But ESP32 initially used raw values → mismatch

---

### 🔥 3. Why Edge Impulse?

Manual TFLite on ESP32 caused:

* dependency issues
* flatbuffers errors
* compatibility problems

👉 Edge Impulse solved all of it

---

## 🚀 Future Improvements

* Add normalization on ESP32
* Support full alphabet (A–Z)
* Add button instead of serial trigger
* Real-time streaming prediction
* Gesture smoothing

---

## 🧠 What This Project Demonstrates

* Edge AI deployment
* Sensor data processing
* TinyML pipeline
* Embedded ML systems

---

## 🙌 Final Result

```text
Air gesture → ESP32 → AI model → Letter prediction
```

---

## ⭐ If You Like This Project

* Star the repo ⭐
* Share with others 🚀
* Build your own extensions 🔥

---

## 👨‍💻 Author

Built with curiosity and persistence 💡
