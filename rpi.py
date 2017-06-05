#!/usr/bin/python

import time
import picamera
import Adafruit_CharLCD as LCD
import azure
import keys

camera = picamera.PiCamera()

# Initialize the LCD using the pins
lcd = LCD.Adafruit_CharLCDPlate()

lcd.set_color(0.0, 0.0, 1.0)  # Blue
lcd.clear()
lcd.message('Push SELECT')

# Make list of button value, text, and backlight color.
buttons = ( (LCD.SELECT, 'Select', (1,1,1)),
            (LCD.LEFT,   'Left'  , (1,0,0)),
            (LCD.UP,     'Up'    , (0,0,1)),
            (LCD.DOWN,   'Down'  , (0,1,0)),
            (LCD.RIGHT,  'Right' , (1,0,1)) )

print('Press Ctrl-C to quit.')
try:
    while True:
        # Loop through each button and check if it is pressed.
        for button in buttons:
            if lcd.is_pressed(button[0]):
                # Button is pressed, change the message and backlight.
                lcd.clear()
                lcd.message(button[1])
                lcd.set_color(button[2][0], button[2][1], button[2][2])

                camera.capture('img.jpg')
                caption = azure.caption_stored_image('img.jpg')
                print(caption)
                access_token = azure.get_access_token(keys.TT_KEY)
                text = azure.get_translation(caption, "en-us", "ja-jp", access_token)
                print(text)
    
                lcd.set_color(0.0, 0.0, 1.0)  # Blue
                lcd.clear()
                lcd.message(caption[0:16] + "\n" + caption[16:])

except KeyboardInterrupt:
    lcd.set_color(0.0, 0.0, 0.0)  # Off
    lcd.clear()
    lcd.message('Quit')
    print('\nQuit')
