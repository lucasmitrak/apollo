#include "Arduino.h"
#include "Wire.h"
#include "MutichannelGasSensor.h"
#include "Seeed_BMP280.h"
#include "MLX90615.h"
#include <I2cMaster.h>
#include <Digital_Light_TSL2561.h>
#define SDA_PIN 11   //define the SDA pin
#define SCL_PIN 10   //define the SCL pin

SoftI2cMaster i2c(SDA_PIN, SCL_PIN);
MLX90615 mlx90615(DEVICE_ADDR, &i2c);

const int arduino_reset=4;
const int button = 3;
const int pir = 2;
const int loudness = 14;
const int light = 4;
const int flame = 18;
const int dust = 8;
const int sw=12;
#define DHT11_PIN 0 // ADC PIN 0

unsigned long duration;
unsigned long starttime;
unsigned long sampletime_ms = 2000;
unsigned long lowpulseoccupancy = 0;
float ratio = 0;
float concentration = 0;
unsigned long read_last;
int gc_smoke, gc_co,gc_co_blood,gc_smoke_al, gc_temp, gc_hum;
unsigned char incomingByte[21];
unsigned long time_gc_flush;
bool bytes_finished=false;
int byte_count=0;
float bright=0;
float bright_last=0;
int buttonState = LOW;
long last_debounce_time=0;
long last_flame_time=0;
long debounce_delay=50;
long flame_delay=50;
bool flame_last=false;
int buttontemp = -1;
float temperature;
float pressure;
float altitude;
<<<<<<< HEAD
unsigned int bug=0;
BMP280 bmp280;
static uint32_t prevTime;
uint32_t curTime = millis();
=======
BMP280 bmp280;
>>>>>>> Update arduino.ino
void setup()
{
    //hard reset for relay set as output
    pinMode(arduino_reset,OUTPUT);
    //golf comcast begin
    Serial3.begin(57600);
    //set infared sensor to work as I2C
    DDRF |= _BV(DHT11_PIN);
    PORTF |= _BV(DHT11_PIN);
    //I2C begins communication
    Wire.begin();
    //begin multichannel gas sensor
    //the default I2C address of the slave is 0x04
    gas.begin(0x04);
    gas.powerOn();
    //initializing sensor
    TSL2561.init();
    //timer for response time
    read_last=millis();
    //communicating with raspberry pi
    Serial.begin(9600);
    //setting buttons and pir as input
    pinMode(button,INPUT);
    pinMode(pir,INPUT);
    //Hardware interrupts
    attachInterrupt(digitalPinToInterrupt(pir), motion_detected, RISING);
    attachInterrupt(digitalPinToInterrupt(button), button_change, CHANGE);
    bmp280.init();
    //Multichannel Gas sensor initalization
    pinMode(12, INPUT);
    //Dust Sensor initialization
    pinMode(dust,INPUT);
    starttime = millis();
    //switch
    pinMode(sw, INPUT);
    //Flame Sensor initialization
    pinMode(flame,INPUT);
    attachInterrupt(digitalPinToInterrupt(flame), flame_change, CHANGE);
}
void sendSensorData(long c, int code, unsigned d=500)
{
<<<<<<< HEAD
    if(c <10000000){
        unsigned long data=(unsigned long)code*10000000 + c;
        Serial.print(data);
        Serial.print("\n");
    }
=======
    
        unsigned long data=(unsigned long)code*10000000 + c;
        Serial.print(data);
        Serial.print("\n");
    
>>>>>>> Update arduino.ino
    
    delay(d);
}
/**flushing serial data from serial port
in order to get new data afterwards
and avoid duplicate sent data**/
void serialFlush()
{
    for (int i = 0; i < 10; i++) {
        while (Serial.available() > 0) {
           Serial.read();
            delay(1);
        }
        delay(1);
    }
}
void motion_detected()
{   time_counter();
    ++bug;
    bug_check();
    sendSensorData(0, 26, 0);
}
void flame_change()
{   time_counter();
    ++bug;
    bug_check();
    int flame_state = digitalRead(flame);
    if ((millis() - last_flame_time) > flame_delay) {
        //if the flame has been detected
        if ((flame_state == HIGH) && (!flame_last)) {
            sendSensorData(1, 22, 0);
            //we need to change the state
            flame_last = !flame_last;
            //set the current time
            last_flame_time = millis();
        }
        //if the flame has been turned off
        else if ((flame_state == LOW) && (flame_last)) {
            
            //we need to change the state
            flame_last = !flame_last;
            //set the current time
            last_flame_time = millis();
        }
    }
}
void button_change()
<<<<<<< HEAD
{   time_counter();
    ++bug;
    bug_check();
=======
{
>>>>>>> Update arduino.ino
    buttonState = digitalRead(button);
    if ( (millis() - last_debounce_time) > debounce_delay) {
    
    //if the button has been pressed
    if ( (buttonState == HIGH) && (buttontemp < 0) ) {
 
      sendSensorData(0, 24, 0);
      
     
      
      buttontemp = -buttontemp; // we need to change the state
      last_debounce_time = millis(); //set the current time
    }
    else if ( (buttonState == LOW) && (buttontemp > 0) ) {
 
     sendSensorData(0, 25, 0);
      
      buttontemp = -buttontemp; //we need to change the state
      last_debounce_time= millis(); //set the current time
    }//close if/else
 
  }
<<<<<<< HEAD
}
void bug_check()
{
  if (bug>=5)
  {
    
    digitalWrite(arduino_reset,HIGH);
  }
}
void time_counter()
{
  if ( curTime - prevTime >= 24*60*60*1000UL )
  {
    
    prevTime = curTime;
    digitalWrite(arduino_reset,HIGH);
    
  }
=======
>>>>>>> Update arduino.ino
}
void interrupt_check()
{
    //if arduino gets no response in ten seconds from raspberry pi,
    //it will reset it
    bug=0;
    if (millis()> read_last +300000) {
        sendSensorData(0, 55, 0);
        //total circuit reset by turning on relay to cut power
        digitalWrite(arduino_reset,HIGH);
        read_last=millis();
    }
    //every second, flushes serial data coming from golf comcast
    if (millis() >time_gc_flush+1000) {
        byte_count=0;
        //flush golf comcast
        Serial3.flush();
        time_gc_flush = millis();
    }
    //while it can read from the serial, read the incoming bytes
    while(Serial3.available()>0) {
        incomingByte[byte_count] = Serial3.read();
        byte_count++;
        //read until got 21 total values in incoming stream
        //if so, bytes finished is true
        if (byte_count>=21) {
            byte_count=0;
            bytes_finished=true;
        }
        time_gc_flush = millis();
    }
    //check bytes finished and surrounding values are zero
    if((bytes_finished) && ((incomingByte[0]==0) && (incomingByte[21]==0))) {
        /*all from golf comcast
        converting bytes to decimal value by
        combining two numbers using OR statement binary shift*/
        int raw_byte=0;
        //smoke
        raw_byte = incomingByte[3] | incomingByte[2] << 8;
            gc_smoke=raw_byte;
        //carbon monoxide
        raw_byte = incomingByte[13] | incomingByte[12] << 8;
            gc_co=raw_byte;
        //temperature
        raw_byte = incomingByte[7] | incomingByte[6] << 8;
            gc_temp=raw_byte;
        //humidity
        raw_byte = incomingByte[9] | incomingByte[8] << 8;
            gc_hum=raw_byte;
        // CO in blood
        raw_byte = incomingByte[15] | incomingByte[14] << 8;
            gc_co_blood=raw_byte;
        // Smoke output after algorithm
        raw_byte = incomingByte[19] | incomingByte[18] << 8;
            gc_smoke_al=raw_byte;
        //set bytes_finished back to false
        bytes_finished=false;
    }
    //get bright value
    bright=TSL2561.readVisibleLux();
    //checking if difference from last brightness is greater than 50
    if (((bright - bright_last)/bright_last) > 0.1) {
        sendSensorData(bright, 27, 250);
        bright_last = bright;
    }
}
<<<<<<< HEAD


=======
>>>>>>> Update arduino.ino
byte read_dht11_dat()
{
    byte i = 0;
    byte result=0;
    for(i=0; i< 8; i++) {
<<<<<<< HEAD
=======
        //wait for 50ms
>>>>>>> Update arduino.ino
        while(!(PINF & _BV(DHT11_PIN)));
        delayMicroseconds(30);
        if(PINF & _BV(DHT11_PIN))
            result |=(1<<(7-i));
        //wait '1' finish
        while((PINF & _BV(DHT11_PIN)));
    }
    return result;
}
void loop()
{
  // reset approximately 6 hours
  time_counter();
    // wait for input
    while (Serial.available() ==0)
        interrupt_check();
    serialFlush();
    read_last=millis();
    
    //get the pressure
    pressure = bmp280.getPressure();
    //uncompensated calculated measured in meters
    altitude = bmp280.calcAltitude(pressure);
    //convert temperature
   // temperature =((float)temperature * 1.8) + 32.0;
    sendSensorData((long)pressure, 60, 0);
    sendSensorData((long)altitude, 61, 0);
    
    //waiting for response back from raspberry pi
    while (Serial.available() ==0)
        interrupt_check();
    serialFlush();
    read_last=millis();
   byte dht11_dat[5];
    byte dht11_in;
    byte i;
    // start condition
    // 1. pull-down i/o pin from 18ms
    PORTF &= ~_BV(DHT11_PIN);
    delay(18);
    PORTF |= _BV(DHT11_PIN);
    delayMicroseconds(40);

   byte dht11_dat[5];
    byte dht11_in;
    byte i;
    // start condition
    // 1. pull-down i/o pin from 18ms
    PORTF &= ~_BV(DHT11_PIN);
    delay(18);
    PORTF |= _BV(DHT11_PIN);
    delayMicroseconds(40);

    DDRF &= ~_BV(DHT11_PIN);
    delayMicroseconds(40);

    dht11_in = PINF & _BV(DHT11_PIN);
    delayMicroseconds(80);

    dht11_in = PINF & _BV(DHT11_PIN);
    delayMicroseconds(80);
    // now ready for data reception
    for (i=0; i<5; i++)
    dht11_dat[i] = read_dht11_dat();

    DDRF |= _BV(DHT11_PIN);
    PORTF |= _BV(DHT11_PIN);

    byte dht11_check_sum = dht11_dat[0]+dht11_dat[1]+dht11_dat[2]+dht11_dat[3];
    // check check_sum
    long xhum=dht11_dat[0];
    sendSensorData(xhum, 30, 1000);
    //get the temperature
    long temperature= dht11_dat[2];
    temperature =((float)temperature * 1.8) + 32.0;
    sendSensorData(temperature, 29, 1000);
    //wait for response from raspberry pi
    while (Serial.available() ==0)
        interrupt_check();
    serialFlush();
    read_last=millis();
    /***************************************************************
     Multichannel gas Sensor
    ****************************************************************/
    sendSensorData(gas.measure_NH3(), 11);
    sendSensorData(gas.measure_CO(), 12);
    sendSensorData(gas.measure_NO2(), 13);
    sendSensorData(gas.measure_C3H8(), 14);
    sendSensorData(gas.measure_C4H10(), 15);
    //sendSensorData(gas.measure_CH4(), 16);
    sendSensorData(gas.measure_H2(), 17);
    sendSensorData(gas.measure_C2H5OH(), 18);
  
    /***************************************************************
    Dust  Sensor
    ****************************************************************/
    starttime = millis();
    while((millis()-starttime) < sampletime_ms) {
        duration = pulseIn(dust, LOW);
        lowpulseoccupancy = lowpulseoccupancy+duration;
    }
    ratio = lowpulseoccupancy/(sampletime_ms*10.0);
    concentration = 1.1*pow(ratio,3)-3.8*pow(ratio,2)+520*ratio+0.62; // using spec sheet curve
    //0.62 is the default value, thus it is checked for before sending out the data
    if (concentration != 0.62)
        sendSensorData(concentration, 23, 250);
    lowpulseoccupancy = 0;
    //end dust sensor
    //send raspberry pi the code that denotes the end of the gas sensor
    sendSensorData(0, 65, 0);
    Serial3.flush();
    //waiting for response back from raspberry pi
    while (Serial.available() ==0)
        interrupt_check();
    serialFlush();
    read_last=millis();
    //variables used in interrupt
    sendSensorData(gc_smoke, 32, 0);
    sendSensorData(gc_co, 33, 0);
    gc_temp =(((float)gc_temp/100.0) * 1.8) + 32.0;
    sendSensorData(gc_temp, 34, 0);
    gc_hum=((float)gc_hum/100.0);
    sendSensorData(gc_hum, 35, 0);
    sendSensorData(gc_co_blood, 36, 0);
    sendSensorData(gc_smoke_al, 37, 0);
    //waiting for response back from raspberry pi
    while (Serial.available() ==0)
        interrupt_check();
    serialFlush();
    read_last=millis();
    // Reading switch postion
    sendSensorData(digitalRead(sw), 90, 0);
    //waiting for response back from raspberry pi
    while (Serial.available() ==0)
        interrupt_check();
    serialFlush();
    read_last=millis();
    // INfrared Temperature Sensor
    float obj=mlx90615.getTemperature(MLX90615_OBJECT_TEMPERATURE);
    obj=obj*1.8 +32.0;
    sendSensorData(obj, 68, 0);
  //Serial.print("Ambient temperature: ");
    float amb=mlx90615.getTemperature(MLX90615_AMBIENT_TEMPERATURE);
    amb=amb*1.8 + 32.0;
    sendSensorData(amb, 69, 0);
    //waiting for response back from raspberry pi
    while (Serial.available() ==0)
        interrupt_check();
    serialFlush();
    read_last=millis();
    // Reading switch postion
    sendSensorData(digitalRead(sw), 90, 0);
    //waiting for response back from raspberry pi
    while (Serial.available() ==0)
        interrupt_check();
    serialFlush();
    read_last=millis();
    // INfrared Temperature Sensor
    float obj=mlx90615.getTemperature(MLX90615_OBJECT_TEMPERATURE);
    obj=obj*1.8 +32.0;
    sendSensorData(obj, 68, 0);
  //Serial.print("Ambient temperature: ");
    float amb=mlx90615.getTemperature(MLX90615_AMBIENT_TEMPERATURE);
    amb=amb*1.8 + 32.0;
    sendSensorData(amb, 69, 0);
    //waiting for response back from raspberry pi
    while (Serial.available() ==0)
        interrupt_check();
    serialFlush();
    read_last=millis();
    //code for raspberry pi sensors to send their values
    sendSensorData(0, 31, 0);
}
