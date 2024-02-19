import unittest
from unittest.mock import patch, MagicMock
from opsys_ps_controller.tdk_z_controller import TdkZController


class Test(unittest.TestCase):
    @ classmethod
    def setUp(self):
        pass

    @ classmethod
    def setUpClass(cls):
        pass

    @ classmethod
    def tearDownClass(cls):
        pass

    @ patch.object(TdkZController, 'get_device_id')
    def test_get_device_id(self, ps_mock: MagicMock):
        ps_conn = TdkZController('GPIB0::1::INSTR', True)
        ps_conn.get_device_id()
        ps_mock.assert_called_once_with()
        
    @ patch.object(TdkZController, 'close_connection')
    def test_close_connection(self, ps_mock: MagicMock):
        ps_conn = TdkZController('GPIB0::1::INSTR', True)
        ps_conn.close_connection()
        ps_mock.assert_called_once_with()

    @ patch.object(TdkZController, 'enable_output')
    def test_enable_output(self, ps_mock: MagicMock):
        ps_conn = TdkZController('GPIB0::1::INSTR', True)
        ps_conn.enable_output()
        ps_mock.assert_called_once_with()

    @ patch.object(TdkZController, 'disable_output')
    def test_disable_output(self, ps_mock: MagicMock):
        ps_conn = TdkZController('GPIB0::1::INSTR', True)
        ps_conn.disable_output()
        ps_mock.assert_called_once_with()

    @ patch.object(TdkZController, 'reset_device')
    def test_reset_device(self, ps_mock: MagicMock):
        ps_conn = TdkZController('GPIB0::1::INSTR', True)
        ps_conn.reset_device()
        ps_mock.assert_called_once_with()

    @ patch.object(TdkZController, 'get_current')
    def test_get_current(self, ps_mock: MagicMock):
        ps_conn = TdkZController('GPIB0::1::INSTR', True)
        ps_conn.get_current()
        ps_mock.assert_called_once_with()

    @ patch.object(TdkZController, 'set_current')
    def test_set_current(self, ps_mock: MagicMock):
        ps_conn = TdkZController('GPIB0::1::INSTR', True)
        current = 2
        ps_conn.set_current(current=current)
        ps_mock.assert_called_once_with(current=2)

    @ patch.object(TdkZController, 'get_voltage')
    def test_get_voltage(self, ps_mock: MagicMock):
        ps_conn = TdkZController('GPIB0::1::INSTR', True)
        ps_conn.get_voltage()
        ps_mock.assert_called_once_with()

    @ patch.object(TdkZController, 'set_voltage')
    def test_set_voltage(self, ps_mock: MagicMock):
        ps_conn = TdkZController('GPIB0::1::INSTR', True)
        voltage = 12
        ps_conn.set_voltage(voltage=voltage)
        ps_mock.assert_called_once_with(voltage=12)

    @ patch.object(TdkZController, 'set_remote_mode')
    def test_is_remote(self, ps_mock: MagicMock):
        ps_conn = TdkZController('GPIB0::1::INSTR', True)
        ps_conn.set_remote_mode()
        ps_mock.assert_called_once_with()



if __name__ == '__main__':
    unittest.main()
