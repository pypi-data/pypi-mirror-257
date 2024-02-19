from .ps_abstract import PsAbstract
from .ps_configs import *


class PsController(PsAbstract):
    """
    Power Supply controller

    """

    def __init__(self,
                 baudrate=TdkZupConfig.BAUDRATE,
                 delay=TdkZupConfig.DELAY,
                 address=TdkZupConfig.ADDRESS,
                 ps_type=PsTypes.TDK_Z_UP):
        """
        constructor

        Args:
            baudrate (int, optional): COMs baud rate
            delay (float, optional): delay time between serial
                                     interface commands
            address (int, optional): device address
            ps_type (str, optional): device type/model
        """
        self._baudrate = baudrate
        self._delay = delay
        self._address = address
        self._ps_type = ps_type
        self.ps_controller = None

    def init_connection(self):
        """
        Scan COM ports to find ATEN related

        Returns:
            bool: connection to PS status
            
        Raises:
            ValueError
        """
        if self._ps_type == PsTypes.TDK_Z_UP:
            from .tdk_zup_controller import TdkZupController

            self.ps_controller = TdkZupController(self._baudrate,
                                                   self._delay,
                                                   self._address,
                                                   TdkZupConfig.BUFFER_SIZE)
            is_connected = self.ps_controller.init_connection()
            self.ps_controller.set_mode(is_remote=True)
            
        elif self._ps_type == PsTypes.TDK_Z:
            from .tdk_z_controller import TdkZController
            
            self.ps_controller = TdkZController(self._address)
            is_connected = True
            self.ps_controller.set_remote_mode()
            
        else:
            raise ValueError("Can't find device type")
        
        return is_connected
    
    def close_connection(self):
        """
        Disconnect from serial connection
        
        Raises:
            NotImplementedError
        """
        if self._ps_type == PsTypes.TDK_Z_UP:
            raise NotImplementedError
            
        elif self._ps_type == PsTypes.TDK_Z:
            self.ps_controller.close_connection()

    def disconnect(self):
        """
        Disconnect from serial connection
        
        Raises:
            NotImplementedError
        """
        if self._ps_type == PsTypes.TDK_Z_UP:
            self.ps_controller.disconnect()
            
        elif self._ps_type == PsTypes.TDK_Z:
            raise NotImplementedError

    def ps_on(self):
        """
        Set power on
        
        Raises:
            NotImplementedError
        """
        if self._ps_type == PsTypes.TDK_Z_UP:
            self.ps_controller.ps_on()
            
        elif self._ps_type == PsTypes.TDK_Z:
            raise NotImplementedError

    def ps_off(self):
        """
        Set power off
        
        Raises:
            NotImplementedError
        """
        if self._ps_type == PsTypes.TDK_Z_UP:
            self.ps_controller.ps_off()
            
        elif self._ps_type == PsTypes.TDK_Z:
            raise NotImplementedError
            
    def enable_output(self):
        """
        Set power on
        
        Raises:
            NotImplementedError
        """
        if self._ps_type == PsTypes.TDK_Z_UP:
            raise NotImplementedError
            
        elif self._ps_type == PsTypes.TDK_Z:
            self.ps_controller.enable_output()

    def disable_output(self):
        """
        Set power off
        
        Raises:
            NotImplementedError
        """
        if self._ps_type == PsTypes.TDK_Z_UP:
            raise NotImplementedError
            
        elif self._ps_type == PsTypes.TDK_Z:
            self.ps_controller.disable_output()
            
    def ps_reset(self, reset_delay=1, wait_for_user_interaction_callback=None):
        """
        Reset power supply
        
        Raises:
            NotImplementedError

        Args:
            reset_delay (int, optional): delay time after reset. Defaults to 1.
            wait_for_user_interaction_callback (Callable, optional): Callback object instance. 
                                                                     Defaults to None.
        """
        if self._ps_type == PsTypes.TDK_Z_UP:
            self.ps_controller.ps_reset(reset_delay, wait_for_user_interaction_callback)

        elif self._ps_type == PsTypes.TDK_Z:
            raise NotImplementedError
    
    def reset_device(self):
        """
        Reset power supply
        
        Raises:
            NotImplementedError
        """
        if self._ps_type == PsTypes.TDK_Z_UP:
            raise NotImplementedError

        elif self._ps_type == PsTypes.TDK_Z:
            self.ps_controller.reset_device()

    def get_current(self):
        """
        Read power supply current

        Returns:
            float: electrical current value
        """
        return self.ps_controller.get_current()
    
    def get_voltage(self):
        """
        Read power supply voltage

        Returns:
            float: voltage value
        """
        return self.ps_controller.get_voltage()
    
    def set_current(self, current):
        """
        Set power supply current

        Args:
            current (float): electrical current value
        """
        self.ps_controller.set_current(current)
    
    def set_voltage(self, voltage):
        """
        Set power supply voltage

        Args:
            voltage (float): voltage value
        """
        self.ps_controller.set_voltage(voltage)

    def clear_device(self):
        """
        Clear device data

        Raises:
            NotImplementedError
        """
        if self._ps_type == PsTypes.TDK_Z_UP:
            raise NotImplementedError

        elif self._ps_type == PsTypes.TDK_Z:
            self.ps_controller.clear_device()
            
    def get_system_error(self):
        """
        Read system error if exists

        Raises:
            NotImplementedError

        Returns:
            str: system error
        """
        if self._ps_type == PsTypes.TDK_Z_UP:
            raise NotImplementedError

        elif self._ps_type == PsTypes.TDK_Z:
            return self.ps_controller.get_system_error()
    
    def get_lan_ip_address(self):
        """
        Read ps IP address

        Raises:
            NotImplementedError

        Returns:
            str: IP address
        """
        if self._ps_type == PsTypes.TDK_Z_UP:
            raise NotImplementedError

        elif self._ps_type == PsTypes.TDK_Z:
            return self.ps_controller.get_lan_ip_address()
        
    def get_lan_host_name(self):
        """
        Read ps host name

        Raises:
            NotImplementedError

        Returns:
            str: LAN hostname
        """
        if self._ps_type == PsTypes.TDK_Z_UP:
            raise NotImplementedError

        elif self._ps_type == PsTypes.TDK_Z:
            return self.ps_controller.get_lan_host_name()
        
    def get_device_id(self):
        """
        Read device id

        Raises:
            NotImplementedError

        Returns:
            str: device id
        """
        if self._ps_type == PsTypes.TDK_Z_UP:
            raise NotImplementedError

        elif self._ps_type == PsTypes.TDK_Z:
            return self.ps_controller.get_device_id()

    def is_remote(self):
        """
        Check if remote mode is active or not
        
        Raises:
            NotImplementedError

        Returns:
            bool: Remote mode status (enabled/disabled)
        """
        if self._ps_type == PsTypes.TDK_Z_UP:
            return self.ps_controller.is_remote()

        elif self._ps_type == PsTypes.TDK_Z:
            raise NotImplementedError

    def set_mode(self, is_remote):
        """
        Set operation mode - remote or local
        
        Raises:
            NotImplementedError

        Args:
            is_remote (bool): True for remote mode activation
                              False for remote mode deactivation
        """
        if self._ps_type == PsTypes.TDK_Z_UP:
            return self.ps_controller.set_mode(is_remote)

        elif self._ps_type == PsTypes.TDK_Z:
            raise NotImplementedError

    def set_ps_address(self, address):
        """
        Set PS address ID number
        
        Raises:
            NotImplementedError

        Args:
            address (int): address ID number, between 1 and 9
        """
        if self._ps_type == PsTypes.TDK_Z_UP:
            return self.ps_controller.set_ps_address(address)

        elif self._ps_type == PsTypes.TDK_Z:
            raise NotImplementedError

    def is_on(self):
        """
        Checking if the PS is on (output voltage exists)
        
        Raises:
            NotImplementedError

        Returns:
            bool: PS On/Off status
        """
        if self._ps_type == PsTypes.TDK_Z_UP:
            return self.ps_controller.is_on()

        elif self._ps_type == PsTypes.TDK_Z:
            raise NotImplementedError
