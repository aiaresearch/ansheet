

import serial
import time

# 设置串口参数
ser = serial.Serial(
    port='COM3',  # 你的串口号，例如'/dev/ttyUSB0' 或者 'COM1'
    baudrate=9600,  # 波特率，这里设置为9600
    timeout=1  # 超时设置
)

# 等待一会儿，确保串口已经打开
time.sleep(2)

try:
    # 发送字符'a'到串口
    ser.write(b'a')
    print("Sent 'a' over serial")
    time.sleep(5)
    ser.write(b'b')
    print("Sent 'b' over serial")

except Exception as e:
    print("Error:", e)
finally:
    # 关闭串口连接
    ser.close()
