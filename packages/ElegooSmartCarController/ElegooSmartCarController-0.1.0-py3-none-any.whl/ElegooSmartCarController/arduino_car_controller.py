
import socket
import json
import time

class ArduinoCarController:
    def __init__(self, ip="192.168.4.1", port=100):
        self.ip = ip
        self.port = port
        self.sock = None

    def _connect(self):
        """Establishes connection to the Arduino server."""
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.ip, self.port))
        print(f"Connected to {self.ip} on port {self.port}")

    def _disconnect(self):
        """Closes the socket connection."""
        if self.sock:
            self.sock.close()
            self.sock = None
            print("Disconnected")

    def _send_command(self, command):
        """Sends a JSON-encoded command through the socket."""
        if not self.sock:
            self._connect()
        json_command = json.dumps(command)
        print(f"Sending command: {json_command}")
        self.sock.sendall(json_command.encode())

    def _execute_command(self, command):
        """Sends a command and handles post-command execution, such as delays."""
        self._send_command(command)
        if "T" in command:
            time.sleep(command["T"] / 1000)

    def _create_command(self, n, **kwargs):
        """Creates a command dictionary from provided parameters."""
        command = {"N": n}
        command.update(kwargs)
        return command

    def _map_direction_to_code(self, direction):
        """Maps a textual direction to its corresponding numeric code."""
        direction_map = {
            "forward": 3,
            "backward": 4,
            "left": 1,
            "right": 2
        }
        return direction_map.get(direction.lower(), 0)

    def car_control_time_limit(self, direction, car_speed, duration_ms):
        direction_code = self._map_direction_to_code(direction)
        command = self._create_command(2, D1=direction_code, D2=car_speed, T=duration_ms)
        self._execute_command(command)

    def car_control_no_time_limit(self, direction, car_speed):
        direction_code = self._map_direction_to_code(direction)
        command = self._create_command(3, D1=direction_code, D2=car_speed)
        self._execute_command(command)

    # Placeholder for additional methods based on previous instructions
