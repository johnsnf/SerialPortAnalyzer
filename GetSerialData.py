import serial
import time
import argparse 

parser = argparse.ArgumentParser(description = "This retrieves serial data from the specified port/baud rate and returns it as text. Note data is saved as 'response' variable if run with -i")
parser.add_argument("portName", type = str, help = "Path to the serial device (linux) or COM port (windows)") 
parser.add_argument("--baudRate", default = 9600, type = int, help = "Baud rate, default is 9600")
parser.add_argument("--timeOut", default = 1, type = float, help = "Timeout on serial port connection")

args = parser.parse_args()

timeOut = args.timeOut 
baudRate = args.baudRate 
portName = args.portName 

# Configure the serial connection parameters (adjust port and baudrate as needed)
# port_name = '/dev/cu.usbserial-210'
# port_name = '/dev/cu.your_device_name' # Replace with your actual port name
# baud_rate = 9600 # Replace with your device's baud rate

try:
    # Open the serial port using a 'with' statement to ensure it closes automatically
    with serial.Serial(port=portName, baudrate=baudRate, timeout=timeOut) as ser:
        time.sleep(2) # Give the connection time to establish
        print(f"Serial port {ser.port} opened successfully.")

        # # Example: Write data (encode string to bytes)
        # ser.write(b'Hello from Python\n')
        # print("Data sent: Hello from Python")

        # Example: Read data (decode bytes to string)
        while True:
            if ser.in_waiting > 0:
                response = ser.readline().decode('utf-8').strip()
                print(f"Received: {response}")
                break

except serial.SerialException as e:
    print(f"Error opening or communicating with serial port: {e}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")