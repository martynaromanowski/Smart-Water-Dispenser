from machine import Pin
import time
from time import sleep
from s2pico_oled import OLED
from machine import Pin, I2C
from hx711 import HX711

i2c = I2C(0, sda=Pin(8), scl=Pin(9))
oled = OLED(i2c, Pin(18))

#for load cell
DT = 17  #for data
SCK = 16  #for clock

#for pump
pump = Pin(14, Pin.OUT) #push tube is marked by orange tape

#for buzzer
buzzer = Pin(11, Pin.OUT, Pin.PULL_UP)

#initializing switches for numpad 0-9 and enter
one = Pin(1, Pin.IN, Pin.PULL_UP)
two = Pin(2, Pin.IN, Pin.PULL_UP)
three = Pin(3, Pin.IN, Pin.PULL_UP)
four = Pin(4, Pin.IN, Pin.PULL_UP)
five = Pin(5, Pin.IN, Pin.PULL_UP)
six = Pin(6, Pin.IN, Pin.PULL_UP)
seven = Pin(7, Pin.IN, Pin.PULL_UP)
eight = Pin(38, Pin.IN, Pin.PULL_UP)
nine = Pin(37, Pin.IN, Pin.PULL_UP)
zero = Pin(36, Pin.IN, Pin.PULL_UP)
enter = Pin(35, Pin.IN, Pin.PULL_UP)

#for load cell
pin_OUT = Pin(12, Pin.IN, pull=Pin.PULL_DOWN)
pin_SCK = Pin(13, Pin.OUT)
hx711 = HX711(pin_SCK, pin_OUT)

userAmt = "" #setting default amount for user input

#methods for pump
def pump_on(): #turns pump on
    pump.value(0)
    
def pump_off(): #turns pump off
    pump.value(1)
#pump logic is inverted; pump.value(0) turns the pump on and pump.value(1) turns it off

while True:
    pump_off() #ensures pump is off during user input
    
    if one.value() == 0: #0 indicates its pressed
        userAmt += "1" #enters a #, in this case 1, to userAmt
        sleep(0.5) #debounce delay
        
    if two.value() == 0: 
        userAmt += "2"
        sleep(0.5)
        
    if three.value() == 0: 
        userAmt += "3"
        sleep(0.5)
        
    if four.value() == 0: 
        userAmt += "4"
        sleep(0.5)
        
    if five.value() == 0:
        userAmt += "5"
        sleep(0.5)
        
    if six.value() == 0:
        userAmt += "6"
        sleep(0.5)

    if seven.value() == 0:
        userAmt += "7"
        sleep(0.5)
        
    if eight.value() == 0:
        userAmt += "8"
        sleep(0.5)
        
    if nine.value() == 0:
        userAmt += "9"
        sleep(0.5)
        
    if zero.value() == 0:
        userAmt += "0"
        sleep(0.5)
    
    if enter.value() == 0:
        userAmt = int(userAmt) #converts userAmt to int so it can be numerically worked with
        break #leaves while True loop
    
    sleep(0.5)
    print(userAmt) #prints user input for feedback

#for load cell
hx = HX711(d_out=DT, pd_sck=SCK)
hx.tare() #auto tare
hx.set_scale(7050) #scale for calibration

print("Scale is ready. Place weight on it.")

while True:
    weight = hx.get_units(10)  #average of 10 readings
    calibrated_weight = float(weight) * 16.68 #ratio for calibration
    print(f"Weight: {calibrated_weight:.2f} grams") #prints weight in grams

    while userAmt > calibrated_weight: #while the load cell weight is less than the userAmt
        weight = hx.get_units(10) #continue reading weight
        calibrated_weight = float(weight) * 16.68
        print(f"Amount Dispensed: {calibrated_weight:.2f} mL") #continue printing weight
        pump.on() #keep pump on

    if userAmt <= calibrated_weight: #when the load cell detects the userAmt
        buzzer.on() #turn buzzer on
        pump.off() #turn pump off
        sleep(2) #keep buzzer on for 2 seconds
        buzzer.off() #turn buzzer off after 2 seconds
        break 
    
    
    

        

        
