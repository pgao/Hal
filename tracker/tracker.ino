#include <Servo.h>

using namespace std;

int pan_port = 5;
int tilt_port = 2;

Servo pan_servo;
Servo tilt_servo;
char serialData;

void setup() {
  pan_servo.attach(pan_port);
  tilt_servo.attach(tilt_port);
  Serial.begin(9600);
  moveTo(tilt_servo, 110);
  moveTo(pan_servo, 90);
}

int orientation = 1;

void loop() {
  int y = 0; //move x or y motor
  int neg = 0; //negative or positive movement
  int distance = 0; //how far to move
  while(Serial.available()) {
    serialData = Serial.read();
    //Serial.print(serialData);
    if(serialData >= '0' && serialData <= '9') {
      Serial.print("serialData number is ");
      Serial.println(serialData);
      Serial.print("neg is ");
      Serial.println(neg);
      distance = serialData - '0';
      if(neg == 1) {
        distance = -distance;
      }
      if(y == 0) {
        Serial.print("moving pan motor with distance ");
        Serial.println(distance);
        moveServo(pan_servo, -distance);
      }
      else if(y == 1) {
        moveServo(tilt_servo, distance);
      }
    }
    else if(serialData == 'x') {
      y = 0;
    }
    else if(serialData == 'y') {
      y = 1;
      neg = 0;
      distance = 0;
    }
    else if(serialData == '-') {
      neg = 1;
      //Serial.println("Negative number");
    }
    else {
      Serial.print("\n");
    }
  }
  //moveServo(tilt_servo, inc);
  //moveServo(pan_servo, orientation);
}

void moveServo(Servo servo, int delta) {
  int previousValue = servo.read();
  int newValue = previousValue + delta;
  if (newValue > 180 || newValue < 30) {
    orientation = -orientation;
    return;
  }
  servo.write(newValue);
}

void moveTo(Servo servo, int newPos) {
  if (newPos > 180 || newPos < 30) {
    return;
  }
  else {
    servo.write(newPos);
  }
}
