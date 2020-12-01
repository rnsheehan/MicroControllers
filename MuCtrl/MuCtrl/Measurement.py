# The idea here is to store all the different things you need for Code in one module
# Code can then import the module and call whatever functions are needed
# R. Sheehan 27 - 10 - 2020

MOD_NAME_STR = "Measurement"

# import the necessary modules
import board
import time
import digitalio
from analogio import AnalogOut
from analogio import AnalogIn
import supervisor # for listening to serial ports

# Define the names of the pins being written to and listened to
Vout = AnalogOut(board.A0)
Vin1 = AnalogIn(board.A1)
Vin2 = AnalogIn(board.A2)
Vin3 = AnalogIn(board.A3)
Vin4 = AnalogIn(board.A4)
Vin5 = AnalogIn(board.A5)

# Define the names of the read / write commands
readCmdStr = 'r'; # read data command string for reading max AC input
writeCmdStr = 'w'; # write data command string for writing frequency values
writeAngStrA = 'a'; # write analog output from DCPINA
writeAngStrB = 'b'; # write analog output from DCPINB
readAngStr = 'l'; # read analog input

# Define the constants
Vmax = 3.3 # max AO/AI value
bit_scale = (64*1024) # 64 bits

# Need the following functions to convert voltages to 12-bit readings
# which can be understood by the board

def dac_value(volts):
    # convert a voltage to 10-bit value

    FUNC_NAME = ".dac_value()" # use this in exception handling messages
    ERR_STATEMENT = "Error: " + MOD_NAME_STR + FUNC_NAME

    try:
        if Vmax > 0.0 and bit_scale > 0:
            return int((volts / Vmax)*bit_scale)
        else:
            ERR_STATEMENT = ERR_STATEMENT + "\nvolt, bit scale factors not defined"
            raise Exception
    except Exception as e:
        print(ERR_STATEMENT)
        print(e)

def get_voltage(pin, offset = 0.0):
    # convert pin reading to voltage value
    # correct voltage by substracting offset
    
    FUNC_NAME = ".get_voltage()" # use this in exception handling messages
    ERR_STATEMENT = "Error: " + MOD_NAME_STR + FUNC_NAME

    try:
        if Vmax > 0.0 and bit_scale > 0:
            ret_val = ((pin.value*Vmax)/bit_scale)
            return ret_val - offset if offset > 0.0 else ret_val
        else:
            ERR_STATEMENT = ERR_STATEMENT + "\nvolt, bit scale factors not defined"
            raise Exception
    except Exception as e:
        print(ERR_STATEMENT)
        print(e)

# Determine the zero offset using A0 and A1
def get_zero_offset():
    # Determine the zero offset using A0 and A1
    # Ensure that Vout (A0) is set to zero
    # There is a bit of an offset in voltage between the Read and the Write, 
    # presumably because the pins are floating.
    Vout.value = dac_value(0)
    time.sleep(0.5)
    deltaV = get_voltage(Vin1, 0.0) # offset in the voltage reading at A2 O(10 mV)
    # print("deltaV Reading at A1: ", deltaV)

    return deltaV;

def Blink():
    # The first script that is run using CircuitPy
    # Use this to check that everything is operational
    # The led near the re-set button should flash count_limit times and switch off
    # If this doesn't work something is wrong
    # R. Sheehan 19 - 10 - 2020

    FUNC_NAME = ".Voltage_Divider_Test()" # use this in exception handling messages
    ERR_STATEMENT = "Error: " + MOD_NAME_STR + FUNC_NAME

    try:
        led = digitalio.DigitalInOut(board.D13)
        led.direction = digitalio.Direction.OUTPUT

        count = 0
        count_limit = 20

        while count < count_limit:
            led.value = True
            time.sleep(0.5)
            led.value = False
            time.sleep(0.5)
            count = count + 1
            
    except Exception as e:
        print(ERR_STATEMENT)
        print(e)

def Voltage_Divider_Test():
    # Check the operation of the voltage-dividers and buffer amplifiers
    # that are attached to the various inputs of the board
    # R. Sheehan 23 - 10 - 2020

    FUNC_NAME = ".Voltage_Divider_Test()" # use this in exception handling messages
    ERR_STATEMENT = "Error: " + MOD_NAME_STR + FUNC_NAME

    try:
        # determine the zero offset
        deltaV = get_zero_offset()

        # define the voltage-divider scaling
        Vscale = (5.0/3.0)

        # Read the values here
        # Determine the readings at pins A2, A3, A4, A5
        Vin1val = get_voltage(Vin1, deltaV)
        Vin2val = get_voltage(Vin2, deltaV)
        Vin3val = get_voltage(Vin3, deltaV)
        Vin4val = get_voltage(Vin4, deltaV)
        Vin5val = get_voltage(Vin5, deltaV)

        print("deltaV Reading at A1: ", deltaV)
        print("Reading at A2: ", Vin2val, ", Real Reading at A2: ", Vin2val*Vscale)
        print("Reading at A2: ", Vin3val, ", Real Reading at A2: ", Vin3val*Vscale)
        print("Reading at A2: ", Vin4val, ", Real Reading at A2: ", Vin4val*Vscale)
        print("Reading at A2: ", Vin5val, ", Real Reading at A2: ", Vin5val*Vscale)
    except Exception as e:
        print(ERR_STATEMENT)
        print(e)

def Current_Source_Measurement():
    # this method performs the current-source measurements
    # R. Sheehan 23 - 10 - 2020

    FUNC_NAME = ".Current_Source_Measurement()" # use this in exception handling messages
    ERR_STATEMENT = "Error: " + MOD_NAME_STR + FUNC_NAME

    try:
        deltaV = get_zero_offset()

        # define the voltage-divider scaling
        Vscale = (5.0/3.0)

        # Set the output value here
        Vset = 0.0
        R1 = (54.9/1000.0) # units of kOhm
        R2 = (10.3/1000.0) # units of kOhm
        R3 = (4.8/1000.0) # units of kOhm
        ratio = R2 / (R1*R3)
        Rload = (10.0/1000.0) # unit of kOhm
        Vout.value = dac_value(Vset)

        # Read the values here
        # Determine the readings at pins A2, A3, A4, A5
        Vin1val = get_voltage(Vin1, deltaV)
        Vin2val = get_voltage(Vin2, deltaV)
        Vin3val = get_voltage(Vin3, deltaV)
        Vin4val = get_voltage(Vin4, deltaV)
        Vin5val = get_voltage(Vin5, deltaV)

        time.sleep(1.0) # give the board time to power everything

        # print the real readings
        print("\nVset: ",Vin1val)
        print("Vctrl: ",Vin2val*Vscale)
        print("VR3: ",Vin3val*Vscale - Vin4val*Vscale)
        print("IR3 Measured: ",(Vin3val*Vscale - Vin4val*Vscale)/R3)
        print("Iload predicted: ",Vin1val * ratio)
        print("Vload predicted: ",Vin1val * ratio * Rload)
        print("Vload: ", Vin5val*Vscale)

    except Exception as e:
        print(ERR_STATEMENT)
        print(e)

def Cuffe_Iface():
    # method that listens for input from LabVIEW and responds appropriately
    # John Cuffe 10 - 10 - 2020
    # Edited R. Sheehan 27 - 10 - 2020

    FUNC_NAME = ".Cuffe_Iface()" # use this in exception handling messages
    ERR_STATEMENT = "Error: " + MOD_NAME_STR + FUNC_NAME

    try:
        while True:
            if supervisor.runtime.serial_bytes_available:   # Listens for a serial command
                command = input()
                if command.startswith(writeAngStrA):        # If the command starts with writeAngStrA it knows it is an output (Write)
                    try:                                    # In case user inputs NAN somehow
                        SetVoltage = float(command[1:])     # Everything after the writeAngStrA is the voltage
                        if SetVoltage >= 0.0 and SetVoltage < 3.3: # Sets limits on the Output voltage to board specs
                            Vout.value = dac_value(SetVoltage) # Set the voltage
                        else:
                            Vout.value = dac_value(0.0) # Set the voltage to zero in the event of SetVoltage range error
                    except ValueError:
                        ERR_STATEMENT = ERR_STATEMENT + '\nVin must be a float'
                        raise Exception
                elif command.startswith(readAngStr):        # If the command starts with readAngStr it knows user is looking for Vin. (Read)
                    # in the scheme I have set up
                    # A1 measures Ground, A2 measures Vctrl-high, A3 measures Vr3-high, A4 measures Vr3-low, A5 measures Vrl-high
                    # Measurement at ground can be substracted off where required
                    print(get_voltage(Vin1), get_voltage(Vin2), get_voltage(Vin3), get_voltage(Vin4), get_voltage(Vin5)) # Prints to serial to be read by LabView
                    #print(get_voltage(Vin2))
                    #print(Vin1.value)
                else:
                    print(get_voltage(Vin1), get_voltage(Vin2), get_voltage(Vin3), get_voltage(Vin4), get_voltage(Vin5)) # Prints to serial to be read by LabView
                    #print(get_voltage(Vin2))
                    #print(Vin1.value)
    except Exception as e:
        print(ERR_STATEMENT)
        print(e)

def Ser_Test():
    # method that prints a data reading continuously
    # Trying to get Python to read data from port
    # R. Sheehan 30 - 11 - 2020

    FUNC_NAME = ".Ser_Test()" # use this in exception handling messages
    ERR_STATEMENT = "Error: " + MOD_NAME_STR + FUNC_NAME

    try:
       print("Test String")
    except Exception as e:
        print(ERR_STATEMENT)
        print(e)

def AC_Read():
    # The idea is to investigate exactly what the sample rate of the IBM4 is
    # CircuitPython is a ReadOnly filesystem, this means that it cannot create files on its drive
    # It can only write info to the console / buffer
    # This buffer can be read by LabVIEW
    # The aim here is to get the IBM4 to read an AC signal continuously and then write the data being read
    # To the console and then read this console data into LabVIEW
    # To speed up the process I will not perform any voltage conversions here
    # This can be done quite easily in LabVIEW
    # I want to be able to read AC signals on at least 2 channels.
    # This works to some extent the IBM4 is not able to sample at high enough frequency
    # R. Sheehan 30 - 1 - 2020

    FUNC_NAME = "AC_Read.()" # use this in exception handling messages
    ERR_STATEMENT = "Error: " + MOD_NAME_STR + FUNC_NAME

    try:
        while True:
            if supervisor.runtime.serial_bytes_available:   # Listens for a serial command
                command = input()
                if command.startswith(readCmdStr):  # If the command starts with readCmdStr it knows user is looking for Vin. (Read)
                    count = 0
                    count_lim = 500
                    #count_lim = 3e+4 # i think this is close to the upper limit
                    bit_readings_1 = []
                    #bit_readings_2 = []
                    start_time = time.time() # start the clock
                    while count < count_lim:
                        #bit_readings_1.append(Vin1.value) # no voltage conversions here
                        bit_readings_1.append(Vin2.value) # no voltage conversions here
                        count = count + 1
                    elapsed_time = (time.time() - start_time)

                    delta_T = float(elapsed_time / count_lim)

                    # output the data to the buffer
                    count = 0
                    print("Elapsed Time: %(v1)0.15f"%{"v1":elapsed_time})
                    print("Time-step: %(v1)0.15f"%{"v1":delta_T})
                    print("Start")
                    for i in range(0, count_lim, 1):
                        print(bit_readings_1[i])
                    print("End")
                    del bit_readings_1
                else:
                    raise Exception        
    except Exception as e:
        print(ERR_STATEMENT)
        print(e)

def AC_Max():
    # The IBM4 is not able to accurately sample a sine wave
    # The aim now is to see if IBM4 can find the largest value of a sine wave
    # in a given reading request period
    # R. Sheehan 3 - 11 - 2020

    FUNC_NAME = "AC_Max.()" # use this in exception handling messages
    ERR_STATEMENT = "Error: " + MOD_NAME_STR + FUNC_NAME

    try:
        while True:
            if supervisor.runtime.serial_bytes_available:   # Listens for a serial command
                command = input()
                if command.startswith(readCmdStr):                # If the command starts with readCmdStr it knows user is looking for Vin. (Read)
                    #print(get_voltage(Vin1), get_voltage(Vin2), get_voltage(Vin3), get_voltage(Vin4), get_voltage(Vin5)) # Prints to serial to be read by LabView
                    max_val = 0.0
                    count = 0
                    count_lim = 500
                    while count < count_lim:
                        t1 = get_voltage(Vin2) # read the voltage from the pin
                        if t1 > max_val: max_val = t1
                        count = count + 1
                        time.sleep(0.001)                        
                    print(max_val)
                else:
                    raise Exception        
    except Exception as e:
        print(ERR_STATEMENT)
        print(e)

def IO_Simple():
    # Check to ensure that ports A0 and A1 are working correctly
    # R. Sheehan 27 - 10 - 2020

    FUNC_NAME = ".IO_Simple()" # use this in exception handling messages
    ERR_STATEMENT = "Error: " + MOD_NAME_STR + FUNC_NAME

    try:
        deltaV = get_zero_offset()

        Vset = 2.315

        Vout.value = dac_value(Vset) # tell A0 to output Vset Volts
        time.sleep(0.1) # pause for 100 ms
        print("Reading A1: ",get_voltage(Vin1, 0.0)) # Read the value that is input into A1
        
    except Exception as e:
        print(ERR_STATEMENT)
        print(e)
