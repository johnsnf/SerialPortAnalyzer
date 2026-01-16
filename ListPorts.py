import serial.tools.list_ports

def list_serial_ports():
    """
    Lists serial port names and descriptions

    :returns:
        A list of strings with the port name and description
    """
    ports = serial.tools.list_ports.comports()
    return [port.device for port in ports]

if __name__ == '__main__':
    available_ports = list_serial_ports()
    print("Available serial ports:")
    for port in available_ports:
        print(port)