

from pyb import UART, LED

import sensor
import time

sensor.reset()  # Reset and initialize the sensor.
sensor.set_pixformat(sensor.RGB565)  # Set pixel format to RGB565 (or GRAYSCALE)
sensor.ioctl(sensor.IOCTL_SET_FOV_WIDE, True)
sensor.set_framesize(sensor.HQVGA)  # Set frame size to QVGA (320x240)
sensor.skip_frames(time=2000)  # Wait for settings take effect.

r_LED = LED(1)  # The red LED
g_LED = LED(2)  # The green LED
b_LED = LED(3)  # The blue LED
g_LED.on()
r_LED.off()
b_LED.off()
clock = time.clock()  # Create a clock object to track the FPS.
uart = UART("LP1", 115200, timeout_char=2000) # (TX, RX) = (P1, P0) = (PB14, PB15)
x = 0
y = 0

def checksum(arr, initial= 0):
    """ The last pair of byte is the checksum on iBus
    """
    sum = initial
    for a in arr:
        sum += a
    checksum = 0xFFFF - sum
    chA = checksum >> 8
    chB = checksum & 0xFF
    return chA, chB

def IBus_message(message_arr_to_send):
    msg = bytearray(32)
    msg[0] = 0x20
    msg[1] = 0x40
    for i in range(len(message_arr_to_send)):
        msg_byte_tuple = bytearray(message_arr_to_send[i].to_bytes(2, 'little'))
        msg[int(2*i + 2)] = msg_byte_tuple[0]
        msg[int(2*i + 3)] = msg_byte_tuple[1]

    # Perform the checksume
    chA, chB = checksum(msg[:-2], 0)
    msg[-1] = chA
    msg[-2] = chB

    uart.write(msg)

def refreshIbusConnection():
    if uart.any():
        uart_input = uart.read()




while True:
    ############### Color detection here ###############

    #put color detection and such here

    clock.tick()  # Update the FPS clock.
    thresholdsGreenBall = (0, 100, -128, -13, -128, 37)
    img = sensor.snapshot()  # Take a picture and return the image.
    print(clock.fps())  # Note: OpenMV Cam runs about half as fast when connected
    # to the IDE. The FPS should increase once disconnected.


#    color_is_detected = False # replace this with your method
    blobs = img.find_blobs([thresholdsGreenBall], area_threshold=2500, merge=True)
    # Draw blobs
    largest_blob = None
    max_size = 0

#    for blob in blobs:
#        # Draw a rectangle where the blob was found
#        img.draw_rectangle(blob.rect(), color=(0,255,0))
#        # Draw a cross in the middle of the blob
#        img.draw_cross(blob.cx(), blob.cy(), color=(0,255,0))
#        x = blob.cx()
#        y = blob.cy()

##        print("Cord : " , blob.cx(), blob.cy())
##        print("Pixels: " , blob.pixels())

    # Identify the largest blob
    for blob in blobs:
        if blob.pixels() > max_size:
            max_size = blob.pixels()
            largest_blob = blob

    # Check if a largest blob is detected
    if largest_blob:
        img.draw_rectangle(largest_blob.rect(), color=(0, 255, 0))
        img.draw_cross(largest_blob.cx(), largest_blob.cy(), color=(0, 255, 0))
        color_is_detected = True
        x = largest_blob.cx()  # Center x of the largest blob
        y = largest_blob.cy()  # Center y of the largest blob
        pixels_w = largest_blob.w()  # Width of the largest blob
        pixels_h = largest_blob.h()  # Height of the largest blob
    else:
        color_is_detected = False
        x = y = pixels_w = pixels_h = 0  # Reset coordinates if no blob is detected

    # Set the flag based on detection
    flag = 1 if color_is_detected else 0


    flag = 0
    if (color_is_detected):
        g_LED.off()
        r_LED.off()
        b_LED.on()
        flag = 1 # when a color is detected make this flag 1
    else:
        g_LED.on()
        r_LED.off()
        b_LED.off()
    pixels_x = x # put your x center in pixels
    pixels_y = y # put your y center in pixels
    pixels_w = pixels_w  # put your width in pixels (these have almost no affect on control (for now))
    pixels_h = pixels_h # put your height center in pixels (these have almost no affect on control (for now))
    ###############################


    messageToSend = [flag, pixels_x, pixels_y, pixels_w, pixels_h]

    print(f"messageToSend = [flag: {flag}, pixels_x: {pixels_x}, pixels_y: {pixels_y}, pixels_w: {pixels_w}, pixels_h: {pixels_h}]")


    IBus_message(messageToSend)
    refreshIbusConnection()
