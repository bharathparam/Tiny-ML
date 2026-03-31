#include <Wire.h>
#include <MPU6050.h>

MPU6050 mpu;

const int SAMPLE_SIZE = 100;

void setup() {
  Serial.begin(115200);
  Wire.begin();
  mpu.initialize();

  Serial.println("Press any key to start recording...");
}

void loop() {
  if (Serial.available()) {
    Serial.read(); // clear input

    Serial.println("START");

    for (int i = 0; i < SAMPLE_SIZE; i++) {
      int16_t ax, ay, az, gx, gy, gz;
      mpu.getMotion6(&ax, &ay, &az, &gx, &gy, &gz);

      Serial.print(ax); Serial.print(",");
      Serial.print(ay); Serial.print(",");
      Serial.print(az); Serial.print(",");
      Serial.print(gx); Serial.print(",");
      Serial.print(gy); Serial.print(",");
      Serial.println(gz);

      delay(50); // keep consistent timing
    }

    Serial.println("END");
    Serial.println("Done. Press again.");
  }
}