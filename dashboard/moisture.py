#!/usr/bin/env python
import PCF8591 as ADC
import time
import smbus
import sqlite3 as sql


def setup():
	ADC.setup(0x48)

def loop():
	con = sql.connect("IoTDatabase.db")
	c = con.cursor()
	while True:
                bus = smbus.SMBus(1)
                reading = ADC.read(2)
#		print (reading)
		#ADC.write(ADC.read(0))
		value = ((0.641025641)*reading)
		moistureLevel = (100 - value)*2
                if moistureLevel > 100:
                        moistureLevel = 100
		#print (value)
                print('Soil Moisture is %f%%'%(moistureLevel))
                localtime = time.asctime( time.localtime(time.time()) )
		c.execute('insert into soilMoisture(date, reading) values(?, ?)',(localtime,moistureLevel))
		con.commit()
#                f = open("moistureCollector.txt", "a")
#                f.write(str(localtime)+ '\t')
#                f.write(str(moistureLevel)+'\n')
#                f.close()        
 		time.sleep(1)
               

def destroy():
	ADC.write(0)

if __name__ == "__main__":
	try:
		setup()
		loop()
	except KeyboardInterrupt:
		destroy()
