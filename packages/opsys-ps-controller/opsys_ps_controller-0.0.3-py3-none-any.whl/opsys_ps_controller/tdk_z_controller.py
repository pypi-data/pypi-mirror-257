import pyvisa
 

class TdkZController:
    """
    TDK Lambda LAN Power Supply controller

    """

    def __init__(self, address, is_unit_test=False):
        if is_unit_test:
            self.device = None
        else:
            self.rm = pyvisa.ResourceManager()
            self.device = self.rm.open_resource(address)

    def _send_command(self, command):
        self.device.write(command)

    def _read_response(self):
        response = self.device.read()
        return response.strip()
    
    def _query(self, command):
        self.device.write(command)
        response = self.device.read()
        return response.strip()

    def get_device_id(self):
        """
        Read device id
        """
        self._send_command('*IDN?')
        return self._read_response()
   
    def reset_device(self):
        """
        Reset power supply
        """
        self._send_command(':*RST')
   
    def clear_device(self):
        """
        Clear device data
        """
        self._send_command(':*CLS')
 
    def set_remote_mode(self):
        self._send_command('SYST:REM REM')
   
    def get_system_error(self):
        return self._query('SYST:ERROR?')
 
    def get_lan_ip_address(self):
        return self._query('SYSTem:COMM:LAN:IP?')
 
    def get_lan_host_name(self):
        return self._query('SYST:COMM:LAN:HOST?')
   
    def set_voltage(self, voltage):
        """
        Set power supply voltage

        Args:
            voltage (float): voltage value
        """
        self._send_command(f':VOLT {voltage}')
 
    def set_current(self, current):
        """
        Set power supply current

        Args:
            current (float): electrical current value
        """
        self._send_command(f':CURR {current} MA')
 
    def enable_output(self):
        """
        Set power on
        """
        self._send_command(':OUTP:STAT ON')
        
    def disable_output(self):
        """
        Set power off
        """
        self._send_command(':OUTP:STAT OFF')
 
    def get_voltage(self):
        """
        Read power supply voltage

        Returns:
            float: voltage value
        """
        self._send_command('MEAS:VOLT?')
        return round(float(self._read_response()), 2)
 
    def get_current(self):
        """
        Read power supply current

        Returns:
            float: electrical current value
        """
        self._send_command('MEAS:CURR?')
        return round(float(self._read_response()), 2)
 
    def close_connection(self):
        """
        Disconnect from serial connection
        """
        self.device.close()
