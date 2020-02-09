from picamera import PiCamera
from gpiozero import LED, Button
from time import sleep

print("Cerebro: Testing Camera ...")

# This assumes its a Pi platform
camera = PiCamera()

camera.rotation = 180

camera.start_preview()
#camera.start_recording('/home/pi/Desktop/video.h264')

sleep(5)

image_path='/tmp/project_cerebro/media/test_camera.jpg'
camera.capture(image_path)

#camera.stop_recording()
camera.stop_preview()

print("Image is now captured and available in: %s" % image_path)

print("Now, trying the green led ...")
led=LED(27)
led.on()
sleep(5)
led.off()

print("Now, trying the yellow led ...")
led=LED(26)
led.on()
sleep(5)
led.off()

print("finished led testing!")

print("Now, trying the green button for 10 secs ...")
led=LED(27)
button=Button(17)
button.when_pressed=led.on
button.when_released=led.off
sleep(10)
print("green button/led testing completed.")

print("Now, trying the yellow button for 10 secs ...")
led=LED(26)
button=Button(16)
button.when_pressed=led.on
button.when_released=led.off
sleep(10)
print("yellow button/led testing completed.")

print("finished led testing!")
