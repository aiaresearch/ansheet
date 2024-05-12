import ctypes
import sane
import cv2
import numpy as np

SCANNER_NAME = b"YourScannerName"
SOURCE_OPT = b"your_source_option"
SOURCE_STR = b"your_source_string"

def init():
    sane.init()
    # print("SANE version code:", sane.version_code())

def init_device():
    global handle, parameters, option
    handle = sane.open(SCANNER_NAME)
    parameters = handle.get_parameters()
    option = handle.get_option_descriptor(SOURCE_OPT)
    handle.control_option(SOURCE_OPT, sane.ACTION_SET_VALUE, SOURCE_STR)

def scan():
    # print("Starting the scanning process")
    handle.start()
    max_length = parameters.bytes_per_line * parameters.lines
    buffer = ctypes.create_string_buffer(max_length)
    total_bytes = 0
    while True:
        status, data = handle.read(max_length)
        if status == sane.STATUS_EOF or not data:
            break
        elif status != sane.STATUS_GOOD:
            print("Error:", sane.strstatus(status))
            return None
        buffer[total_bytes:total_bytes+len(data)] = data
        total_bytes += len(data)

    image = np.zeros((parameters.lines, parameters.pixels_per_line), dtype=np.uint8)
    for y in range(parameters.lines):
        for x in range(parameters.pixels_per_line):
            byte_index = x // 8 + y * parameters.bytes_per_line
            bit_index = 7 - (x % 8)
            bit_value = ~(buffer[byte_index] >> bit_index) & 1
            image[y, x] = bit_value * 255

    # print("Image created, rows={}, cols={}".format(image.shape[0], image.shape[1]))
    # print("Image mean intensity:", np.mean(image))
    # cv2.imwrite("test.png", image)
    return image

def release():
    handle.close()
    sane.exit()

if __name__ == "__main__":
    init()
    init_device()
    scanned_image = scan()
    release()
