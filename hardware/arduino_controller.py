import logging
from typing import List, Optional, Dict, Any

logger = logging.getLogger("classmate.hardware")

class ArduinoController:
    """
    Serial Communication Controller for Arduino Uno.
    Sends protocol commands to display messages on LCD and trigger physical LED/haptic alerts.
    Works seamlessly in offline/disconnected mode when hardware is absent.
    """
    def __init__(self, port: Optional[str] = None, baudrate: int = 9600):
        self.port = port
        self.baudrate = baudrate
        self.serial_conn = None
        self.is_connected = False
        self.last_sent_command = None
        self.connection_message = "Hardware: Not Connected"

        if self.port:
            self.connect(self.port)

    @staticmethod
    def list_available_ports() -> List[str]:
        """List active serial COM ports available on system."""
        try:
            import serial.tools.list_ports
            ports = serial.tools.list_ports.comports()
            return [port.device for port in ports]
        except Exception as e:
            logger.warning(f"Error scanning serial ports: {e}")
            return []

    def connect(self, port_name: str) -> bool:
        """Establish serial connection to specified COM port."""
        self.port = port_name
        try:
            import serial
            self.serial_conn = serial.Serial(port_name, self.baudrate, timeout=1)
            self.is_connected = True
            self.connection_message = f"Connected on {port_name}"
            logger.info(f"Connected to Arduino on {port_name}")
            return True
        except Exception as e:
            self.is_connected = False
            self.serial_conn = None
            self.connection_message = "Hardware: Not Connected"
            logger.warning(f"Could not connect to Arduino on {port_name}: {e}")
            return False

    def disconnect(self):
        """Close serial connection safely."""
        if self.serial_conn and self.serial_conn.is_open:
            try:
                self.serial_conn.close()
            except Exception:
                pass
        self.is_connected = False
        self.serial_conn = None
        self.connection_message = "Hardware: Not Connected"

    def send_event_command(self, priority_data: Dict[str, Any]) -> bool:
        """
        Send protocol event keyword to Arduino via serial.
        Protocol commands:
          DIRECT_ADDRESS
          QUESTION
          ANNOUNCEMENT
          BELL
          EMERGENCY
          NORMAL
        """
        event_type = priority_data.get("event_type", "NORMAL_LECTURE")
        cmd_map = {
            "DIRECT_ADDRESS": "DIRECT_ADDRESS\n",
            "QUESTION": "QUESTION\n",
            "ANNOUNCEMENT": "ANNOUNCEMENT\n",
            "INSTRUCTION": "ANNOUNCEMENT\n",
            "CLASS_BELL": "BELL\n",
            "EMERGENCY_ALARM": "EMERGENCY\n",
            "NORMAL_LECTURE": "NORMAL\n"
        }

        command = cmd_map.get(event_type, "NORMAL\n")
        self.last_sent_command = command.strip()

        if not self.is_connected or self.serial_conn is None:
            # Graceful disconnected state log
            logger.info(f"[SIMULATED SERIAL] Sent command: '{self.last_sent_command}' (Arduino Disconnected)")
            return False

        try:
            self.serial_conn.write(command.encode('utf-8'))
            self.serial_conn.flush()
            logger.info(f"[HARDWARE SERIAL] Successfully sent command '{self.last_sent_command}' to {self.port}")
            return True
        except Exception as e:
            logger.error(f"Failed to write to Arduino serial port: {e}")
            self.is_connected = False
            self.connection_message = "Hardware: Disconnected (Error)"
            return False
