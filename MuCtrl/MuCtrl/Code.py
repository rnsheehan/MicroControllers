# This script is for testing the operation of the current source controlled by the Itsy-Bitsy M4
# R. Sheehan 23 - 10 - 2020

# import the necessary modules
import board
import time
from analogio import AnalogOut
from analogio import AnalogIn
import supervisor # for listening to serial ports

# Methods for making the measurements are defined in the file Measurement.py
import Measurement

#Measurement.Ser_Test()

#Measurement.First_Script()

Measurement.Cuffe_Iface() # This is for the Current Source Measurement

#Measurement.AC_Read() # This is trying to read a sine wave

#Measurement.AC_Max() # Find the max value being input to some channel

#Measurement.Voltage_Divider_Test()
#Measurement.Current_Source_Measurement()
#Measurement.IO_Simple()

