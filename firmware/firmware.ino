#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>

void moveServoToDegree();

// 创建一个 PCA9685 对象
Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver();

#define SERVOMIN  150 // 舵机最小 PWM 脉冲宽度 (微秒)
#define SERVOMAX  600 // 舵机最大 PWM 脉冲宽度 (微秒)

// 定义 引脚
#define MPin1 11
#define MPin2 10
#define MPin3 9
#define MPin4 8
#define MPin5 12
#define MPin6 13

int raising_countdown[4];
int resetting_countdown[4];
int data;

void set_motor(int value) {
    digitalWrite(MPin1, value);
    digitalWrite(MPin2, value);
    digitalWrite(MPin3, value);
    digitalWrite(MPin4, value);
    digitalWrite(MPin5, value);
    digitalWrite(MPin6, value);
}

void setup() {
  // 初始化串口通信
  Serial.begin(9600);

  // 初始化 PCA9685
  pwm.begin();
  pwm.setPWMFreq(50);   // 设置频率，默认为50Hz

  // Motor
  pinMode(MPin1, OUTPUT);
  pinMode(MPin3, OUTPUT);
  pinMode(MPin2, OUTPUT);
  pinMode(MPin4, OUTPUT);
  pinMode(MPin5, OUTPUT);
  pinMode(MPin6, OUTPUT);
  set_motor(LOW);

  // Countdown
  for (int i = 0; i < 4; i++) {
      raising_countdown[i] = 0;
      resetting_countdown[i] = 0;
  }

  Serial.println("Init done.");
}

void loop() {
    delay(1);
    // Update countdown
    for (int i = 0; i < 4; i++) {
        if (raising_countdown[i] > 0) {
            raising_countdown[i]--;
            if (raising_countdown[i] == 0) {
                moveServoToDegree(i + 1, 50);
                Serial.print("Raising servo No. ");
                Serial.println(i + 1);
<<<<<<< HEAD
                Serial.print("Current countdown value ");
                Serial.println(resetting_countdown[i]);
=======
>>>>>>> ab8e2b460c4263b305da4ca61667c745e5cd355d
                // resetting_countdown[i] += 3000;
            }
        }
        // Servo i is up.
<<<<<<< HEAD
        if ((raising_countdown[i] == 0) && (resetting_countdown[i] > 0)) {
            resetting_countdown[i]--;
            if (resetting_countdown[i] == 0) {
=======
        if (raising_countdown[i] == 0 && resetting_countdown[i] > 0) {
            resetting_countdown[i]--;
            if (raising_countdown[i] == 0) {
>>>>>>> ab8e2b460c4263b305da4ca61667c745e5cd355d
                moveServoToDegree(i + 1, 0);
                Serial.print("Resetting servo No. ");
                Serial.println(i + 1);
            }
        }
    }

  // Handle serial command
  if (Serial.available() > 0) {
    data = Serial.read();
<<<<<<< HEAD
    if (data >= '0')
        data -= '0';
    Serial.print("Received data: ");
    Serial.println(data);
    // Servo movement schedule
    if (data >= 1 && data <= 4) {
        // No movement has already been scheduled
        if (raising_countdown[data-1] == 0) {
            raising_countdown[data-1] = 1000 * data ; // DELAY BEFORE RAISING
            Serial.print("Schedule new movement on servo No. ");
            Serial.println(data);
        }
        resetting_countdown[data-1] += 5000; // DELAY BEFORE RESETTING
=======
    // Servo movement schedule
    if (data >= 1 && data <= 4) { // 确保输入的数字在0到3之间
        // No movement has already been scheduled
        if (raising_countdown[data-1] == 0) {
            raising_countdown[data-1] = 1000 * data + 3000;
            Serial.print("Schedule new movement on servo No. ");
            Serial.println(data);
        }
        resetting_countdown[data-1] += 3000;
>>>>>>> ab8e2b460c4263b305da4ca61667c745e5cd355d
        Serial.print("Add 3000ms to resetting countdown of servo No.");
        Serial.print(data);
        Serial.print(", current countdown value ");
        Serial.println(resetting_countdown[data-1]);

    }

    // Servo reset
<<<<<<< HEAD
    if (data == 5) {
=======
    if (data == 11) {
>>>>>>> ab8e2b460c4263b305da4ca61667c745e5cd355d
        moveServoToDegree(1, 0);
        moveServoToDegree(2, 0);
        moveServoToDegree(3, 0);
        moveServoToDegree(4, 0);
        Serial.println("Resetted all servo.");
    }
<<<<<<< HEAD
    if (data == 6) {
      moveServoToDegree(4, 85);  // 将舵机转到90度位置
      moveServoToDegree(1, 85);
      moveServoToDegree(2, 85);
      moveServoToDegree(3, 85);
=======
    if (data == 12) {
      moveServoToDegree(4, 50);  // 将舵机转到90度位置
      moveServoToDegree(1, 50);
      moveServoToDegree(2, 50);
      moveServoToDegree(3, 50);
>>>>>>> ab8e2b460c4263b305da4ca61667c745e5cd355d
      Serial.println("Raised all servo.");
    }

    // Motor control
    // Stop motors
<<<<<<< HEAD
    if (data == 7) {
        set_motor(LOW);
        Serial.println("Powered off motors");
    }
    if(data == 8){
=======
    if (data == 13) {
        set_motor(LOW);
        Serial.println("Powered off motors");
    }
    if(data == 14){
>>>>>>> ab8e2b460c4263b305da4ca61667c745e5cd355d
        set_motor(HIGH);
        Serial.println("Powered on motors");
    }
  }
}

// 函数：将舵机转到指定角度
void moveServoToDegree(uint8_t servoNum, uint16_t degree) {
  // 将角度转换为 PWM 脉冲
  uint16_t pulse = map(degree, 0, 180, SERVOMIN, SERVOMAX);

  // 设置 PCA9685 通道的 PWM 脉冲
  pwm.setPWM(servoNum, 0, pulse);
}
