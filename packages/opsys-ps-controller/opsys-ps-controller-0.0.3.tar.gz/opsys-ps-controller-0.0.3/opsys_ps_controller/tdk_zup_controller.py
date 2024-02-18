import time
import re
import serial
from .ps_abstract import PsAbstract

# avoid COMs detection at deployment
try:
    import serial.tools.list_ports
except Exception as e:
    print(e)


class TdkZupController(PsAbstract):
    """
    ATEN Power Supply controller

    """

    def __init__(self, baudrate=9600, delay=0.5, address=1, buffer_size=9):
        """
        constructor

        Args:
            baudrate (int): COMs baud rate
            delay (float): delay time between serial interface
                                     commands.
            address (int): device address
            buffer_size (int): serial data fixed buffer size
        """
        self._baudrate = baudrate
        self._delay = delay
        self._address = f":ADR0{address};".encode('ascii')
        self._buffer_size = buffer_size

    def init_connection(self):
        """
        Scan COM ports to find ATEN related

        Returns:
            bool: connection to PS status
        """
        try:
            ports = serial.tools.list_ports.comports()
            for port, description, hwid in sorted(ports):
                print("{}: {} [{}]".format(port, description, hwid))
                if ("ATEN USB to Serial Bridge" in description):
                    try:
                        is_conn = self.is_connected(port)
                        if not is_conn:
                            return is_conn
                        self.conn.timeout = self._delay
                        self.is_on()  # will fail in case it's not a PS
                        print('Serial connection established')
                        return is_conn
                    except:
                        pass
        except:
            print(
                "Fail to connect!\nPlease make sure you have ATEN driver installed\nhttps://www.aten.com/global/en/supportcenter/info/downloads/?action=display_product&pid=575"
            )
        return False

    def is_connected(self, port):
        """
        Check if the port is open

        Args:
            port (str): COM port name

        Returns:
            bool: connection status - True if connected,
                  else False
        """
        number_of_retries = 3
        
        for _ in range(number_of_retries):
            try:
                self.conn = serial.Serial(port, self._baudrate)
                return True
            except Exception as error:
                if 'PermissionError(13' in str(error):
                    self.conn.close()
                    time.sleep(self._delay)
                    self.conn = serial.Serial(port, self._baudrate)
                    return True
        return False

    def disconnect(self):
        """
        Disconnect from serial connection
        """
        self.conn.close()

    def read_buffer(self, remove_header=b""):
        """
        Read and format buffer output

        Args:
            remove_header (str): binary string - output mesage header
                                 required to remove

        Returns:
            str: output binary string with value requested 
        """
        output = b""  # init binary string

        for _ in range(self._buffer_size):  # read from buffer
            output += self.conn.read()
        # format output
        return output.rstrip(b'\r\n').lstrip(b'\r\n').lstrip(remove_header) if len(remove_header) else \
            re.findall("\d+\.\d+", str(output))[0]

    def init_buffer(self):
        """
        Choose address and clear buffer before send
        """
        time.sleep(self._delay)
        self.conn.write(self._address)
        time.sleep(self._delay)
        self.conn.write(b":DCL;")
        time.sleep(self._delay)

    def ps_on(self):
        """
        Set power on

        """
        self.init_buffer()
        self.conn.write(b":OUT1;")

    def ps_off(self):
        """
        Set power off

        """
        self.init_buffer()
        self.conn.write(b":OUT0;")

    def ps_reset(self, reset_delay=1, wait_for_user_interaction_callback=None):
        """
        Reset power supply

        Args:
            reset_delay (int, optional): delay time after reset. Defaults to 1.
            wait_for_user_interaction_callback (Callable, optional): Callback object instance. 
                                                                     Defaults to None.
        """
        try:
            self.ps_off()
            print("Please wait while the system is restart...")
            self.ps_on()
            time.sleep(reset_delay)
        except:
            if wait_for_user_interaction_callback is not None:
                wait_for_user_interaction_callback(
                    "Power cycle the system, press 'OK' after system is ready")
            else:
                input("Power cycle the system, press 'OK' after system is ready\n")

    def get_current(self):
        """
        Read power supply current

        Returns:
            float: electrical current value
        """
        self.init_buffer()
        self.conn.write(b":CUR?;")
        return float(self.read_buffer())

    def get_voltage(self):
        """
        Read power supply voltage

        Returns:
            float: voltage value
        """
        self.init_buffer()
        self.conn.write(b":VOL?;")
        return float(self.read_buffer())

    def set_current(self, current):
        """
        Set power supply current

        Args:
            current (float): electrical current value

        """
        print(f'Set current to: {current}')
        msg_header = "0" if current < 10 else ""
        current = f":CUR{msg_header}{float(current)}0;".encode('ascii')
        self.init_buffer()
        self.conn.write(current)

    def set_voltage(self, voltage):
        """
        Set power supply voltage

        Args:
            voltage (float): voltage value

        """
        print(f'Set voltage to: {voltage}')
        msg_header = "0" if voltage < 10 else ""
        voltage = f":VOL{msg_header}{float(voltage)}00;".encode('ascii')
        self.init_buffer()
        self.conn.write(voltage)

    def is_remote(self):
        """
        Check if remote mode is active or not

        Returns:
            bool: Remote mode status (enabled/disabled)
        """
        self.init_buffer()
        self.conn.write(b":RMT?;")
        current_mode = self.read_buffer(remove_header=b"RM")
        if current_mode == b"1":
            print('The PS is in remote mode')
            return True
        else:
            print('The PS is not in remote mode')
        return False

    def set_mode(self, is_remote):
        """
        Set operation mode - remote or local

        Args:
            is_remote (bool): True for remote mode activation
                              False for remote mode deactivation
        """
        print('Set remote mode')
        mode = f":RMT{int(is_remote)};".encode('ascii')
        self.init_buffer()
        self.conn.write(mode)

    def set_ps_address(self, address):
        """
        Set PS address ID number

        Args:
            address (int): address ID number, between 1 and 9
        """
        self._address = f":ADR0{int(address)};".encode('ascii')
        self.init_buffer()
        print(f'Set PS address to 0{self._address}')
        self.conn.write(self._address)

    def is_on(self):
        """
        Checking if the PS is on (output voltage exists)

        Returns:
            bool: PS On/Off status
        """
        self.init_buffer()
        self.conn.write(b":OUT?;")
        return bool(self.read_buffer(remove_header=b'OT'))
