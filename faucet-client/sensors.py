import abc
import grovepi
import smbus

# 0 = /dev/i2c-0 (port I2C0), 1 = /dev/i2c-1 (port I2C1)
bus = smbus.SMBus(1)


class DS1307():

    def __init__(self):
        self.MON = 1
        self.TUE = 2
        self.WED = 3
        self.THU = 4
        self.FRI = 5
        self.SAT = 6
        self.SUN = 7
        self.DS1307_I2C_ADDRESS = 0x68

    def decToBcd(self, val):
        return ((val / 10 * 16) + (val % 10))

    def bcdToDec(self,  val):
        return ((val / 16 * 10) + (val % 16))

    def begin(self, news):
        print news

    def startClock(self):
        bus.write_byte(self.DS1307_I2C_ADDRESS, 0x00)
        self.second = bus.read_byte(self.DS1307_I2C_ADDRESS) & 0x7f
        bus.write_byte_data(self.DS1307_I2C_ADDRESS, 0x00, self.second)

        print 'startClock..'

    def stopClock(self):
        bus.write_byte(self.DS1307_I2C_ADDRESS, 0x00)
        self.second = bus.read_byte(self.DS1307_I2C_ADDRESS) | 0x80
        bus.write_byte_data(self.DS1307_I2C_ADDRESS, 0x00, self.second)

        print 'stopClock..'

    def setTime(self):
        data = [self.decToBcd(self.second), self.decToBcd(self.minute),
                self.decToBcd(self.hour), self.decToBcd(self.dayOfWeek),
                self.decToBcd(self.dayOfMonth), self.decToBcd(self.month),
                self.decToBcd(self.year)]

        bus.write_byte(self.DS1307_I2C_ADDRESS, 0x00)
        bus.write_i2c_block_data(self.DS1307_I2C_ADDRESS, 0x00, data)

        print 'setTime..'

    def getTime(self):
        bus.write_byte(self.DS1307_I2C_ADDRESS, 0x00)
        data = bus.read_i2c_block_data(self.DS1307_I2C_ADDRESS, 0x00)
        # A few of these need masks because certain bits are control bits
        self.second = self.bcdToDec(data[0] & 0x7f)
        self.minute = self.bcdToDec(data[1])
        # Need to change this if 12 hour am/pm
        self.hour = self.bcdToDec(data[2] & 0x3f)
        self.dayOfWeek = self.bcdToDec(data[3])
        self.dayOfMonth = self.bcdToDec(data[4])
        self.month = self.bcdToDec(data[5])
        self.year = self.bcdToDec(data[6])
        self.ldt = str(self.hour) + ":" + str(self.minute) + ":" + \
            str(self.second) + " " + str(self.month) + "/" + \
            str(self.dayOfMonth) + "/" + str(self.year)

    def fillByHMS(self, _hour,  _minute,  _second):
        self.hour = _hour
        self.minute = _minute
        self.second = _second

        print 'fillByHMS..'

    def fillByYMD(self, _year,  _month,  _day):
        self.year = _year - 2000
        self.month = _month
        self.dayOfMonth = _day

        print 'fillByYMD..'

    def fillDayOfWeek(self,  _dow):
        self.dayOfWeek = _dow

        print 'fillDayOfWeek..'


class Sensor(object):

    @abc.abstractmethod
    def get_value(self):
        pass

    @abc.abstractmethod
    def get_units(self):
        pass

    @abc.abstractmethod
    def get_sensor_name(self):
        pass

    @abc.abstractmethod
    def get_key(self):
        pass


class AirQualitySensor(Sensor):

    def __init__(self, pin):
        self.pin = pin
        grovepi.pinMode(self.pin, "INPUT")

    def get_value(self):
        return grovepi.analogRead(self.pin)

    def get_units(self):
        return "scalar"

    def get_sensor_name(self):
        return "Grove Air Quality Sensor"

    def get_key(self):
        return "air_quality"


class TemperatureSensor(Sensor):

    def __init__(self, pin):
        self.pin = pin

    def get_value(self):
        temp, humidity = grovepi.dht(self.pin, 1)

        if temp != "NULL":
            temp = temp * 1.8 + 32

        return temp

    def get_units(self):
        return "F"

    def get_sensor_name(self):
        return "Grove Temperature and Humidity Sensor Pro White"

    def get_key(self):
        return "temp"


class HumiditySensor(Sensor):

    def __init__(self, pin):
        self.pin = pin

    def get_value(self):
        temp, humidity = grovepi.dht(self.pin, 1)
        return humidity

    def get_units(self):
        return "%"

    def get_sensor_name(self):
        return "Grove Temperature and Humidity Sensor Pro White"

    def get_key(self):
        return "humidity"


class LightSensor(Sensor):

    def __init__(self, pin):
        self.pin = pin
        grovepi.pinMode(self.pin, "INPUT")

    def get_value(self):
        return grovepi.analogRead(self.pin)

    def get_units(self):
        return "lumens"

    def get_sensor_name(self):
        return "Grove Light Sensor"

    def get_key(self):
        return "Light intensity"

    def get_change(self):
        return 0


class MQ2Sensor(Sensor):

    def __init__(self, pin):
        self.pin = pin
        grovepi.pinMode(self.pin, "INPUT")

    def get_value(self):
        amp = (float)(grovepi.analogRead(self.pin) * 5.0 / 1024.0)

        return amp

    def get_units(self):
        return "ppm"

    def get_sensor_name(self):
        return "Grove MQ2 Sensor"

    def get_key(self):
        return "Combustion gas and smoke"

    def get_change(self):
        return 1


class HCHOSensor(Sensor):

    def __init__(self, pin):
        self.pin = pin
        grovepi.pinMode(self.pin, "INPUT")

    def get_value(self):
        return grovepi.analogRead(self.pin) * 5.0 / 1024.0

    def get_units(self):
        return "ppm"

    def get_sensor_name(self):
        return "Grove HCHO Sensor"

    def get_key(self):
        return "HCHO"


class O2Sensor(Sensor):

    def __init__(self, pin):
        self.pin = pin
        grovepi.pinMode(self.pin, "INPUT")

    def readConcentration(self, analogpin):
        MeasuredVout = grovepi.analogRead(analogpin) * (5.0 / 1024.0)
        Concentration = self.FmultiMap(MeasuredVout)
        Concentration_Percentage = Concentration * 100
        return Concentration_Percentage

    def FmultiMap(self, val):
        """ The O2 Concentration in percentage is calculated based on wiki page Graph

        The data from the graph is extracted using WebPlotDigitizer
        http://arohatgi.info/WebPlotDigitizer/app/

        VoutArray[] and O2ConArray[] are these extracted data. Using MultiMap,
        the data is interpolated to get the O2 Concentration in percentage.

        The O2 Concentration in percentage is an approximation and depends on
        the accuracy of Graph used.

        This code uses MultiMap implementation from
        http://playground.arduino.cc/Main/MultiMap
        """

        VoutArray = [0.30769, 20.00000, 40.00000,
                     60.00000, 120.61538, 186.76923]
        O2ConArray = [0.00018, 2.66129, 5.32258, 8.05300, 16.19851, 25.15367]
        # take care the value is within range
        # val = constrain(val, VoutArray[0], VoutArray[size-1]);
        if val <= VoutArray[0]:
            return O2ConArray[0]
        if val >= VoutArray[-1]:
            return O2ConArray[-1]

        # search right interval
        pos = 1
        while val > VoutArray[pos]:
            pos += 1

        # this will handle all exact "points" in the VoutArray array
        if val == VoutArray[pos]:
            return O2ConArray[pos]

        # interpolate in the right segment for the rest
        return (val - VoutArray[pos - 1]) * (
            O2ConArray[pos] - O2ConArray[pos - 1]
        ) / (VoutArray[pos] - VoutArray[pos - 1]) + O2ConArray[pos - 1]

    def get_value(self):
        return self.readConcentration(self.pin)

    def get_units(self):
        return "%"

    def get_sensor_name(self):
        return "Grove O2 Sensor"

    def get_key(self):
        return "O2"


class UltrasonicRanger(Sensor):

    def __init__(self, pin):
        self.pin = pin

    def get_value(self):
        return grovepi.ultrasonicRead(self.pin)

    def get_units(self):
        return "cm"

    def get_sensor_name(self):
        return "Grove Ultrasonic Ranger"

    def get_key(self):
        return "Ultrasonic Ranger"


class FlameSensor(Sensor):

    def __init__(self, pin):
        self.pin = pin
        grovepi.pinMode(self.pin, "INPUT")

    def get_value(self):
        return grovepi.digitalRead(self.pin) == 1

    def get_units(self):
        return "fire"

    def get_sensor_name(self):
        return "Grove Flame  Sensor"

    def get_key(self):
        return "Flame Detected"
