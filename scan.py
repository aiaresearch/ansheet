import sane 
import cv2

def init():
    depth = 8
    mode = 'gray'

#
# Initialize sane
#
    ver = sane.init()
    print('SANE version:', ver)

#
# Get devices
#
    devices = sane.get_devices()
    print('Available devices:', devices)

#
# Open first device
#
    dev = sane.open(devices[0][0])
    dev.source='ADF Back'
    return dev

def scan(dev):
    im=dev.arr_scan()
    cv2.imwrite('image/img.jpg',im)