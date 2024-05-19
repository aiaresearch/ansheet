#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>

// 创建一个 PCA9685 对象
Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver();

#define SERVOMIN  150 // 舵机最小 PWM 脉冲宽度 (微秒)
#define SERVOMAX  600 // 舵机最大 PWM 脉冲宽度 (微秒)

// 定义 引脚
const int MPin1 = 11; // 如果你的 Arduino 板上有内置 LED，则连接到数字引脚 13
const int MPin2 = 10;
const int MPin3 = 9;
const int MPin4 = 8;
const int MPin5 = 12;
const int MPin6 = 13;

void setup() {
  // 初始化串口通信
  Serial.begin(9600);
  
  // 初始化 PCA9685
  pwm.begin();
  
  // 设置频率，默认为50Hz
  pwm.setPWMFreq(50);  // 60Hz

  pinMode(MPin1, OUTPUT);
  pinMode(MPin3, OUTPUT);
  pinMode(MPin2, OUTPUT);
  pinMode(MPin4, OUTPUT);
  pinMode(MPin5, OUTPUT);
  pinMode(MPin6, OUTPUT);
  digitalWrite(MPin1, HIGH);
  digitalWrite(MPin2, HIGH);
  digitalWrite(MPin3, HIGH);
  digitalWrite(MPin4, HIGH);
  digitalWrite(MPin5, HIGH);
  digitalWrite(MPin6, HIGH);

  Serial.println("begin");
}

void loop() {
  // 读取串口输入的数字
  if (Serial.available() > 0) {
    int servoIndex = Serial.parseInt(); // 读取串口输入的数字，确定是哪个舵机
    if (servoIndex >= 1 && servoIndex <= 4) { // 确保输入的数字在0到3之间
      // 驱动对应的舵机
      moveServoToDegree(servoIndex, 0);
      delay(1000); // 等待1秒
      moveServoToDegree(servoIndex, 55);
      delay(8000); // 保持3秒
      moveServoToDegree(servoIndex, 0);
      // 输出当前舵机的角度到串口
      Serial.print("Servo ");
      Serial.print(servoIndex);
      Serial.println(" is moved.");
      delay(20);
    } else if (servoIndex == 98) {
      moveServoToDegree(4, 0);  // 将舵机转到0度位置
      moveServoToDegree(1, 0);
      moveServoToDegree(2, 0);
      moveServoToDegree(3, 0);     
      delay(1000); // 等待1秒
    } else if (servoIndex == 99) {
      moveServoToDegree(4, 80);  // 将舵机转到90度位置
      moveServoToDegree(1, 80);
      moveServoToDegree(2, 80);
      moveServoToDegree(3, 80);
      delay(1000); // 等待1秒
    } else if(servoIndex == 100) {
      digitalWrite(MPin1, LOW);
      digitalWrite(MPin2, LOW);
      digitalWrite(MPin3, LOW);
      digitalWrite(MPin4, LOW);
      digitalWrite(MPin5, LOW);
      digitalWrite(MPin6, LOW);
      Serial.println("stop.");
    }else if(servoIndex == 101){
      digitalWrite(MPin1, HIGH);
      digitalWrite(MPin2, HIGH);
      digitalWrite(MPin3, HIGH);
      digitalWrite(MPin4, HIGH);
      digitalWrite(MPin5, HIGH);
      digitalWrite(MPin6, HIGH);
      Serial.println("start.");
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
