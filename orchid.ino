#include <ESP32Servo.h>

Servo myservo;

int servoPin = 13;   // connect servo signal to GPIO 13

void setup() {
  myservo.attach(servoPin);
}

void loop() {

  myservo.write(20);   // move 30 degrees
  delay(1050);         // wait 1 second

  myservo.write(0);    // return to normal position
  delay(1050);         // wait 1 second

}