# import serial

# serial = serial.Serial('COM3', 9600)
# serial.open()
# serial.write(b'a') # 写入数据
# serial.close()
# # data = serial.readline() # 读取数据
# #print(data)

import serial
import time
import argparse


# 设置串口参数
ser = serial.Serial(
        port="/dev/ttyUSB0",  # 你的串口号，例如'/dev/ttyUSB0' 或者 'COM1'
        baudrate=9600,  # 波特率，这里设置为9600
        timeout=1,  # 超时设置
    )

def serial_write(number):
    ser.write(str(number).encode('ascii'))
    print("Sent", number, "over serial")

def set_motor(on=True):
    if on:
        serial_write(8)
    else:
        serial_write(7)

def raise_all_servo():
    serial_write(6)

def reset_all_servo():
    serial_write(5)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--motor_on", action="store_true", help="Turn the motor on")
    parser.add_argument("--motor_off", action="store_true", help="Turn the motor off")
    # Number of servo motors 1-4
    parser.add_argument("--raise_servo", type=int, help="Raise all servo motors")
    parser.add_argument("--reset", action="store_true", help="Reset all servo motors")

    args = parser.parse_args()

    time.sleep(3)
    if args.motor_on:
        set_motor(on=True)
    if args.motor_off:
        set_motor(on=False)
    if args.raise_servo:
        raise_all_servo()
    if args.reset:
        reset_all_servo()
    time.sleep(7)

