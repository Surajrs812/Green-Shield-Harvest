import serial
import time

# Setup the serial connection (replace 'COM4' with the actual port your Arduino is connected to)
arduino_port = 'COM4'  # Your Arduino's port on Windows
baud_rate = 9600  # Make sure this matches the Arduino's baud rate

# Initialize the connection to the Arduino
ser = serial.Serial(arduino_port, baud_rate, timeout=1)

def read_arduino_data():
    try:
        if ser.in_waiting > 0:
            # Read a line from the serial output
            line = ser.readline().decode('utf-8').strip()
            return line
    except Exception as e:
        print(f"Error reading data: {e}")
    return None

if __name__ == '__main__':
    print("Starting to read data from Arduino on COM4...")
    time.sleep(2)  # Allow the connection to stabilize

    while True:
        data = read_arduino_data()
        if data:
            # Print the sensor data or relay state received from Arduino
            print(f"Arduino Output: {data}")
        
        time.sleep(1)  # Adjust the delay as needed
