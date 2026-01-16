import serial
import serial.tools.list_ports
import time
import argparse 

parser = argparse.ArgumentParser(description = "Sweeps through typical baudrates and sees if the data is meaningful, in an attempt to determine baud rate of serial communication")
parser.add_argument("portName", type = str, help = "Path to the serial device (linux) or COM port (windows)") 
parser.add_argument("--sleepTime", default = 2, type = float, help = "Sleep time between trials to give port time to reset")
parser.add_argument("--timeOut", default = 1, type = float, help = "Timeout on serial port connection")
parser.add_argument("--printResponse", default = False, type = bool, help = "Print out the response of each baud rate")
parser.add_argument("--forceRunAll", default = False, type = bool, help = "Runs through all of the predefined baud despite response found")

args = parser.parse_args()

sleepTime = args.sleepTime 
portName = args.portName 
timeOut = args.timeOut 
printResponse = args.printResponse 
forceRunAll = args.forceRunAll #THIS NEEDS TO BE ADDED AT ANOTHER TIME
#Need to make it fail with 115200. Somethings not right with what its returning
#Need to just have a scan mode that prints all outputs for my own interpretation

def find_baud_rate(port_name, command=b''):
    """
    Tries common baud rates to communicate with a serial device.
    Send a specific command if the device requires a prompt to respond.
    """
    # List of common standard baud rates
    common_baud_rates = [
        9600, 115200, 19200, 38400, 57600, 4800, 2400, 1200
    ]
    # common_baud_rates = [
    #     115200, 19200, 38400, 57600, 4800, 2400, 1200
    # ]

    print(f"Testing port: {port_name}")
    print("-"*40)

    for baud_rate in common_baud_rates:
        print(f'Testing baud rate: {baud_rate}')
        try:
            # Open the serial port with a short timeout
            ser = serial.Serial(port_name, baudrate=baud_rate, timeout=timeOut)
            time.sleep(sleepTime) # Give the device/port time to reset/initialize

            # Clear buffers
            ser.reset_input_buffer()
            ser.reset_output_buffer()

            if command:
                ser.write(command)
                response = ser.read(50) # Read up to 50 bytes
            else:
                response = ser.read_until(b'\r\n') # Read until newline or timeout

            ser.close()

            # Check if the response looks like valid, non-garbled data
            if printResponse:
                print(str(response))
                
            if response and not all(c < 128 for c in response): # Check for non-ASCII characters
                 continue # Likely garbled data, wrong baud rate

            if response:
                try:
                    decoded_response = response.decode('utf-8').strip()
                    
                    #Stripping out null characters
                    decoded_response = decoded_response.strip('\x0000')
                    
                    if decoded_response == '':
                        continue
                    if decoded_response:
                        print(f"Success at {baud_rate} baud. Response: {decoded_response}")
                        return baud_rate, response
                except UnicodeDecodeError:
                    continue # Still might be garbled

        except (serial.SerialException, OSError) as e:
            # Handle cases where the port cannot be opened at all
            print(f"Could not open port at {baud_rate} baud: {e}")
            continue

    return None, None

found_rate,response = find_baud_rate(portName)

if found_rate:
    print(f"\nDevice baud rate is likely: {found_rate}")
else:
    print("\nCould not determine baud rate automatically.")