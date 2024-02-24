import socket
import json

HOST = "192.168.3.49"  # IP address of your Raspberry PI
PORT = 65432  # The port used by the server

def receive_sensor_data():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        
        try:
            while True:
                # Send a request for sensor data to the server
                s.sendall(b"request_sensor_data")
                
                # Receive data from the server
                data = s.recv(1024)
                
                # Decode the received JSON data
                sensor_data = json.loads(data.decode())
                
                # Process the received sensor data (print or use it as needed)
                print("Received sensor data:", sensor_data)
        except KeyboardInterrupt:
            print("Keyboard interrupt detected. Exiting...")
        except Exception as e:
            print("An error occurred:", e)

if __name__ == "__main__":
    receive_sensor_data()
