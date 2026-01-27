#include <ESP32Servo.h>

Servo myServo;

const int servoPin = 18;   // GPIO 18
char data;

void setup() {
  Serial.begin(9600);
  myServo.attach(servoPin);
  myServo.write(0);        // Initial position
}

void loop() {
  if (Serial.available()) {
    data = Serial.read();

    if (data == '1') {
      myServo.write(90);   // Mouth open
    }
    else if (data == '0') {
      myServo.write(0);    // Mouth closed
    }
  }
}
