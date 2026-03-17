#include <ESP32Servo.h>

Servo myServo;

int servoPin = 18;

void setup() {
  Serial.begin(115200);

  myServo.setPeriodHertz(50); 
  myServo.attach(servoPin, 500, 2400);

  myServo.write(0);
}

void loop() {

  if (Serial.available()) {
    char command = Serial.read();

    if (command == 'F') {
      myServo.write(90);
    }

    if (command == 'H') {
      myServo.write(0);
    }
  }

}