import socket
import json
import picar_4wd as fc
import time

HOST = "192.168.3.49"  # IP address of your Raspberry PI
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)

def read_sensor_data():
    # Simulated function to read sensor data from your Raspberry Pi
    # Replace this with actual code to read sensor data

    # TODO we need to intersept the keycodes (w a s d)
    # and then we can tell the car to move in a direction

    pi_data = fc.utils.pi_read()

    return {
        'speed': fc.speed_val(),
        'cpu temperature': pi_data['cpu_temperature'],
        'battery': f"{pi_data['battery']}v/8.4v"
    }


def movement_handle(actions):
    for action in actions:
        if action in ["left", "right", "up", "down"]:
            if action == "none":
                continue
            elif action == "left":
                fc.turn_left(50)
                time.sleep(0.93)
                fc.stop()
            elif action == "right":
                fc.turn_right(50)
                time.sleep(0.93)
                fc.stop()
            elif action == "down":
                fc.turn_right(50)
                time.sleep(1.05)
                fc.stop()
            fc.forward(50)
            time.sleep(0.10)
            fc.stop()
        else:
            raise Exception("Unknown action")

            
def parse_actions(client):
    # returns: list of "left, right, up, down, or none"
    data = client.recv(1024)
    directions = data.decode().strip().split('\n')
    return directions


def send_sensor_data_to_clients():
    while True:
        # Read sensor data
        sensor_data = read_sensor_data()
        
        # Convert sensor data to JSON
        json_data = json.dumps(sensor_data)
        l = []

        
        # Send JSON data to all connected clients
        for client in clients:
            try:
                l += parse_actions(client)
                client.sendall(json_data.encode())
            except:
                clients.remove(client)
        time.sleep(1)  # Adjust the interval as per your requirement
        movement_handle( l )

clients = []

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()

    try:
        while True:
            client, client_addr = s.accept()
            print("Connected to:", client_addr)
            clients.append(client)
            
            # Start sending sensor data to clients
            send_sensor_data_to_clients()
            
    except Exception as e:
        print("Error:", e)
    finally:
        s.close()
