from abc import ABC, abstractmethod


class PsAbstract(ABC):
    @abstractmethod
    def init_connection(self):
        pass
    
    @abstractmethod
    def disconnect(self):
        pass

    @abstractmethod
    def ps_on(self):
        pass

    @abstractmethod
    def ps_off(self):
        pass
    
    @abstractmethod
    def get_current(self):
        pass
    
    @abstractmethod
    def get_voltage(self):
        pass
    
    @abstractmethod
    def set_current(self, current: float):
        pass
    
    @abstractmethod
    def set_voltage(self, voltage: float):
        pass
