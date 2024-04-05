# Untitled - By: john - Fri Mar 29 2024

import pyb # Import module for board related functions
import sensor # Import the module for sensor related functions
import image # Import module containing machine vision algorithms
import time # Import module for tracking elapsed time

sensor.reset() # Resets the sensor
sensor.set_pixformat(sensor.RGB565) # Sets the sensor to RGB
sensor.set_framesize(sensor.QVGA) # Sets the resolution to 320x240 px
sensor.set_vflip(True) # Flips the image vertically
sensor.set_hmirror(True) # Mirrors the image horizontally
sensor.skip_frames(time = 2000) # Skip some frames to let the image stabilize

# Define the min/max LAB values we're looking for
thresholdsGreenBall = (0, 41, -128, -11, -128, 37)
img = sensor.snapshot() # Takes a snapshot and saves it in memory

clock = time.clock()

while(True):
    clock.tick()
    img = sensor.snapshot()


    # Find blobs with a minimal area of 50x50 = 2500 px
    # Overlapping blobs will be merged
    blobs = img.find_blobs([thresholdsGreenBall], area_threshold=2500, merge=True)
    # Draw blobs
    for blob in blobs:
        # Draw a rectangle where the blob was found
        img.draw_rectangle(blob.rect(), color=(0,255,0))
        # Draw a cross in the middle of the blob
        img.draw_cross(blob.cx(), blob.cy(), color=(0,255,0))
        print("Cord : " , blob.cx(), blob.cy())
        print("Pixels: " , blob.pixels())
