#!/usr/bin/env python


class ArduinoSensor():

    def __init__(self, line):
        # read sensor code
        self.code = self.read_code(line)
        # read sensor value
        self.value = self.read_value(line)
        # set sensor identifiers
        self.set_key()
        self.set_units()
        self.set_name()

    # static method so no object is created when checking buffer
    @staticmethod
    def check(read_serial):
        if read_serial is not None:
            return read_serial
        else:
            return False

    def get_value(self):
        return self.value

    def get_key(self):
        return self.key

    def get_units(self):
        return self.units

    def get_sensor_name(self):
        return self.name

    def get_code(self):
        return self.code

    def read_code(self, line):
        """ read the arduino sensor code from the buffer
        """
        # converting ascii to decimal for first two slots
        first = ord(line[0]) - 48
        second = ord(line[1]) - 48
        # the first and second numbers are used to determine the code
        code = (10 * first) + second
        return code

    def read_value(self, line):
        """ read the arduino sensor value from the buffer
        """
        # value is actual reading of ardiono sensor in the buffer
        value = 0
        # slot is integer at the index
        slot = 0
        # start at 2 for index which is offset by the code
        # end at 9 because that is how many digit slots there are
        for x in xrange(2, 9):
            # slot is the integer at the index
            slot = ord(line[x]) - 48
            # value is the integer times ten to the power of its placement in
            value += slot * (10**(8 - x))
        if self.code == 33:
            value = ((value*3.3/4095)-0.3) / (0.002416)
        elif self.code == 34:
            value = (value/100.0)*1.8 + 32
        elif self.code == 35:
            value = value/100
        return value

    def set_key(self):
        if self.code == 0:
            self.key = None
        elif self.code == 11:
            self.key = 'NH3'
        elif self.code == 12:
            self.key = 'CO'
        elif self.code == 13:
            self.key = 'NO2'
        elif self.code == 14:
            self.key = 'C3H8'
        elif self.code == 15:
            self.key = 'C4H10'
        elif self.code == 16:
            self.key = 'CH4'
        elif self.code == 17:
            self.key = 'H2'
        elif self.code == 18:
            self.key = 'C2H5OH'
        elif self.code == 19:
            self.key = 'MQ9'
        elif self.code == 20:
            self.key = 'MQ5'
        elif self.code == 21:
            self.key = 'MQ3'
        elif self.code == 22:
            self.key = 'FLAME'
        elif self.code == 23:
            self.key = 'DUST'
        elif self.code == 24:
            self.key = 'Button Pressed'
        elif self.code == 25:
            self.key = 'Button Released'
        elif self.code == 26:
            self.key = 'Motion Detected'
        elif self.code == 27:
            self.key = 'Brightness'
        elif self.code == 29:
            self.key = 'Temperature'
        elif self.code == 30:
            self.key = 'Humidity'
        elif self.code == 32:
            self.key = 'Smoke'
        elif self.code == 33:
            self.key = 'CO'
        elif self.code == 34:
            self.key = 'Temperature'
        elif self.code == 35:
            self.key = 'Humidity'
        elif self.code == 36:
            self.key = 'CO Blood'
        elif self.code == 37:
            self.key = 'Smoke Algorithm'
        elif self.code == 60:
            self.key = 'Pressure'
        elif self.code == 61:
            self.key = 'Altitude'
        elif self.code == 68:
            self.key = 'Temperature'
        elif self.code == 69:
            self.key = 'Temperature'
        elif self.code == 90:
            self.key = 'Switch'
        else:
            self.key = None

    def set_units(self):
        if self.code == 0:
            self.units = None
        elif (11 <= self.code <= 21):
            self.units = 'PPM'
        elif self.code == 22:
            self.units = 'BOOLEAN'
        elif self.code == 23:
            self.units = 'pcs'
        elif self.code == 24:
            self.units = 'ON'
        elif self.code == 25:
            self.units = 'OFF'
        elif self.code == 26:
            self.units = 'Movement'
        elif self.code == 27:
            self.units = 'lumens'
        elif self.code == 29:
            self.units = 'F'
        elif self.code == 30:
            self.units = '%'
        elif self.code == 32:
            self.units = 'na'
        elif self.code == 33:
            self.units = 'ppm'
        elif self.code == 34:
            self.units = 'F'
        elif self.code == 35:
            self.units = '%'
        elif self.code == 36:
            self.units = 'PPM'
        elif self.code == 37:
            self.units = 'na'
        elif self.code == 60:
            self.units = 'pa'
        elif self.code == 61:
            self.units = 'm'
        elif self.code == 68:
            self.units = 'F'
        elif self.code == 69:
            self.units = 'F'
        elif self.code == 90:
            self.units = 'ON/OFF'
        else:
            self.units = None

    def set_name(self):
        if self.code == 0:
            self.name = None
        elif (11 < self.code < 18):
            self.name = 'Multichannel gas sensor'
        elif self.code == 19:
            self.name = 'MQ9 SENSOR'
        elif self.code == 20:
            self.name = 'MQ3 SENSOR'
        elif self.code == 21:
            self.name = 'FLAME SENSOR'
        elif self.code == 22:
            self.name = ' FLAME SENSOR'
        elif self.code == 23:
            self.name = 'DUST SENSOR'
        elif self.code == 24:
            self.name = 'Push Button'
        elif self.code == 25:
            self.name = 'Push Button'
        elif self.code == 26:
            self.name = 'PIR Sensor'
        elif self.code == 27:
            self.name = 'Brightness Sensor'
        elif self.code == 29:
            self.name = 'Temperature and Humidity Sensor'
        elif self.code == 30:
            self.name = 'Temperature and Humidity Sensor'
        elif (32 <= self.code <= 37):
            self.name = 'Golf CC'
        elif self.code == 60:
            self.name = 'grove digital barometer'
        elif self.code == 61:
            self.name = 'grove digital barometer'
        elif self.code == 68:
            self.name = 'Infared object Temperature'
        elif self.code == 69:
            self.name = 'Infrared Ambient Temperature'
        elif self.code == 90:
            self.name = 'Grove Switch'
        else:
            self.name = None
