#!/usr/bin/env python
import grovepi
import ConfigParser
import serial
from threading import Timer
from werkzeug.datastructures import MultiDict
from sensors import (
    AirQualitySensor,
    HCHOSensor,
    UltrasonicRanger,
    O2Sensor
)
from save import Save
from arduino import ArduinoSensor
import os
<<<<<<< HEAD
<<<<<<< HEAD
=======
>>>>>>> pass checks
import urllib2
import time
import lcd_rgb as lcd
import math
<<<<<<< HEAD
=======
>>>>>>> done
=======
>>>>>>> pass checks

# config object used to read config.ini
config = ConfigParser.ConfigParser()
config.read("config.ini")

reset = 6
grovepi.pinMode(reset, "OUTPUT")


# Watchdog Class
class Watchdog(object):
    def __init__(self, time=20.0):
        ''' Class constructor.
        The "time" argument has the units of seconds. '''
        self._time = time
        return

    def StartWatchdog(self):
        ''' Starts the watchdog timer. '''
        self._timer = Timer(self._time, self._WatchdogEvent)
        self._timer.daemon = True
        self._timer.start()
        return

    def PetWatchdog(self):
        ''' Reset watchdog timer. '''
        self.StopWatchdog()
        self.StartWatchdog()
        return

    def _WatchdogEvent(self):
        '''
        This internal method gets called when the timer triggers.
        A keyboard interrupt is generated on the main thread.
        The watchdog timer is stopped when a previous
        event is tripped.
        '''
        print 'Watchdog event...'
        grovepi.digitalWrite(reset, 1)
        return

    def StopWatchdog(self):
        ''' Stops the watchdog timer. '''
        self._timer.cancel()


# save object that consolidates configuration and where it saves
save = Save(config)

# led pin port used for indicator led
led_pin = 7

# set indicator led
grovepi.pinMode(led_pin, "OUTPUT")
grovepi.chainableRgbLed_init(led_pin, 1)

# ultrasonic ranger pin number
ultrasonic_ranger = 4

# dictionary used to associate sensors names and their objects
sensor_name_dict = MultiDict([
    ("o2_sensor", O2Sensor),
    ("hcho_sensor", HCHOSensor),
    ("ultrasonic_sensor", UltrasonicRanger),
    ("airquality_sensor", AirQualitySensor)
])


sensor_objects = []


def internet_on():
    try:
        urllib2.urlopen('http://216.58.192.142', timeout=5)
        return True
    except urllib2.URLError:
        return False


def initalize_sensors():
    """ read what sensors are attached from the raspberry pi
    from the config and create objects for them
    """
    # read what sensors are attached to the raspberry pi
    sensor_pins = config.items("sensors")

    # iterate and create objects for them
    for value in sensor_pins:
        objects = sensor_name_dict.getlist(value[0])
        for sensor in objects:
            sensor_objects.append(
                sensor(int(value[1]))
            )


def main():
    initalize_sensors()
    count = 0
<<<<<<< HEAD

    # serial used for communication with the arduino
    ser = serial.Serial('/dev/ttyACM0', baudrate=9600, timeout=5)
    grovepi.pinMode(reset, 'OUTPUT')
    # check for internet connection
    internet = None
=======
    reset = 6
    # serial used for communication with the arduino
    ser = serial.Serial('/dev/ttyACM0', baudrate=9600, timeout=5)
    grovepi.pinMode(reset, 'OUTPUT')

    # check for internet connection
    internet = None
    grovepi.digitalWrite(reset, 1)
>>>>>>> pass checks
    lcd.setText("***Welcome***")
    lcd.setRGB(0, 128, 64)
    time.sleep(1)
    lcd.setText("Checking your internet")
    lcd.setRGB(20, 28, 64)
    check = float('nan')
<<<<<<< HEAD
    # try to connect to the internet 10 times
=======
    # try to connect to the internet 40 times
>>>>>>> pass checks
    while True:
        try:
            urllib2.urlopen('https://www.google.com/?gws_rd=ssl', timeout=5)
            internet = True
        except urllib2.URLError:
            internet = False

        if internet:
            break
        time.sleep(1)
<<<<<<< HEAD
        count += 1
        if count == 10:
=======
        count += count
        if count == 40:
>>>>>>> pass checks
            lcd.setText("Sorry no internet connection")
            lcd.setRGB(152, 4, 255)
            time.sleep(1)
            lcd.setText("Type:sudo python test.py")
            lcd.setRGB(0, 128, 64)
            time.sleep(120)
            count = 0
    print sensor_objects
    lcd.setText("You are all set")
    lcd.setRGB(20, 28, 64)
    time.sleep(10)
    lcd.setText("System Restart")
    lcd.setRGB(47, 47, 256)
<<<<<<< HEAD
    w = Watchdog(20.0)
    w.StartWatchdog()
=======
>>>>>>> pass checks
    ser.flushInput()
    ser.write('2')

    while True:
        try:
            # reading serial data from arduino
            read_serial = ser.readline()
            # check for event using static method
            check = ArduinoSensor.check(read_serial)
            # if there is something in the buffer
            if check:
                # create default arduino sensor object
                arduinoSensor = ArduinoSensor(check)
<<<<<<< HEAD

                if arduinoSensor.get_code() != 65 \
                        or arduinoSensor.get_code() != 31\
                        or arduinoSensor.get_code() != 55:
                    print arduinoSensor.get_sensor_name(),\
                         arduinoSensor.get_value()
                    text = str(arduinoSensor.get_key()) + " = " \
                        + str(arduinoSensor.get_value())
                    lcd.setText(text)
                    lcd.setRGB(200, 128, 0)
                if arduinoSensor.get_code() < 22 or \
                        arduinoSensor.get_code() > 26:
                    w.PetWatchdog()
                    print"dog petted"
=======
                # if told to do arduino sensors
>>>>>>> pass checks
                if arduinoSensor.get_code() == 31:
                    try:
                        # iterate through sensors, get its value, and save
                        for sensor in sensor_objects:
                            value = sensor.get_value()
                            if value != 0 and not math.isnan(value)\
                                    and value != "Null":
                                # printing previous value
                                print sensor.get_key(), "  ", value
                                stemp = sensor.get_key() + " =" + str(value)
                                lcd.setText(stemp)
                                lcd.setRGB(128, 128, 128)
                                # use save object to save sensor value
                                save.save(sensor, value)
                                time.sleep(0.5)
<<<<<<< HEAD
                        ser.write('2')
=======
                                ser.write('2')
>>>>>>> pass checks
                    except IOError:
                        pass
                elif arduinoSensor.get_code() == 65:
                    ser.write('2')
                elif arduinoSensor.get_code() == 55:
                    os.system('/sbin/shutdown -r now')
<<<<<<< HEAD
                elif arduinoSensor.get_code() == 61:
                    # use polymorphism in the function to save arduino data
                    save.save(arduinoSensor, arduinoSensor.get_value())
                    ser.write('2')
                elif arduinoSensor.get_code() == 29:
                    # use polymorphism in the function to save arduino data
                    save.save(arduinoSensor, arduinoSensor.get_value())
                    ser.write('2')
                elif arduinoSensor.get_code() == 69:
                    # use polymorphism in the function to save arduino data
                    save.save(arduinoSensor, arduinoSensor.get_value())
                    ser.write('2')
                elif arduinoSensor.get_code() == 37:
                    # use polymorphism in the function to save arduino data
                    save.save(arduinoSensor, arduinoSensor.get_value())
                    ser.write('2')
                elif arduinoSensor.get_code() == 90:
                    # use polymorphism in the function to save arduino data
                    save.save(arduinoSensor, arduinoSensor.get_value())
                    ser.write('2')
                else:
                    # use polymorphism in the function to save arduino data
                    save.save(arduinoSensor, arduinoSensor.get_value())
=======
                else:
                    # use polymorphism in the function to save arduino data
                    save.save(arduinoSensor, arduinoSensor.get_value())

>>>>>>> pass checks
        except IOError:
            ser.flushInput()
            ser.write('2')
        except TypeError:
            ser.flushInput()
            ser.write('2')
        except KeyboardInterrupt:
            # display light if there is a keyboard interrupt before exiting
            # program is ending on user input so close and exit
            save.close()
            exit()
        except IndexError:
            pass

if __name__ == "__main__":
    main()
