import unittest
from unittest.mock import patch, MagicMock
from opsys_ps_controller.tdk_zup_controller import TdkZupController


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

    @ patch.object(TdkZupController, 'init_connection')
    def test_init_connection(self, ps_mock: MagicMock):
        ps_conn = TdkZupController()
        ps_conn.init_connection()
        ps_mock.assert_called_once_with()

    @ patch.object(TdkZupController, 'is_connected')
    def test_is_connected(self, ps_mock: MagicMock):
        ps_conn = TdkZupController()
        port = 'COM3'
        ps_conn.is_connected(port=port)
        ps_mock.assert_called_once_with(port='COM3')
        
    @ patch.object(TdkZupController, 'disconnect')
    def test_disconnect(self, ps_mock: MagicMock):
        ps_conn = TdkZupController()
        ps_conn.disconnect()
        ps_mock.assert_called_once_with()

    @ patch.object(TdkZupController, 'ps_on')
    def test_ps_on(self, ps_mock: MagicMock):
        ps_conn = TdkZupController()
        ps_conn.ps_on()
        ps_mock.assert_called_once_with()

    @ patch.object(TdkZupController, 'ps_off')
    def test_ps_off(self, ps_mock: MagicMock):
        ps_conn = TdkZupController()
        ps_conn.ps_off()
        ps_mock.assert_called_once_with()

    @ patch.object(TdkZupController, 'ps_reset')
    def test_ps_reset(self, ps_mock: MagicMock):
        ps_conn = TdkZupController()
        delay = 20
        ps_conn.ps_reset(reset_delay=delay)
        ps_mock.assert_called_once_with(reset_delay=20)

    @ patch.object(TdkZupController, 'get_current')
    def test_get_current(self, ps_mock: MagicMock):
        ps_conn = TdkZupController()
        ps_conn.get_current()
        ps_mock.assert_called_once_with()

    @ patch.object(TdkZupController, 'set_current')
    def test_set_current(self, ps_mock: MagicMock):
        ps_conn = TdkZupController()
        current = 2
        ps_conn.set_current(current=current)
        ps_mock.assert_called_once_with(current=2)

    @ patch.object(TdkZupController, 'get_voltage')
    def test_get_voltage(self, ps_mock: MagicMock):
        ps_conn = TdkZupController()
        ps_conn.get_voltage()
        ps_mock.assert_called_once_with()

    @ patch.object(TdkZupController, 'set_voltage')
    def test_set_voltage(self, ps_mock: MagicMock):
        ps_conn = TdkZupController()
        voltage = 12
        ps_conn.set_voltage(voltage=voltage)
        ps_mock.assert_called_once_with(voltage=12)

    @ patch.object(TdkZupController, 'is_remote')
    def test_is_remote(self, ps_mock: MagicMock):
        ps_conn = TdkZupController()
        ps_conn.is_remote()
        ps_mock.assert_called_once_with()

    @ patch.object(TdkZupController, 'set_mode')
    def test_set_mode(self, ps_mock: MagicMock):
        ps_conn = TdkZupController()
        remote_enable = True
        ps_conn.set_mode(is_remote=remote_enable)
        ps_mock.assert_called_once_with(is_remote=True)

    @ patch.object(TdkZupController, 'set_ps_address')
    def test_set_ps_address(self, ps_mock: MagicMock):
        ps_conn = TdkZupController()
        address = 1
        ps_conn.set_ps_address(address=address)
        ps_mock.assert_called_once_with(address=1)

    @ patch.object(TdkZupController, 'read_buffer')
    def test_read_buffer(self, ps_mock: MagicMock):
        ps_conn = TdkZupController()
        header = b"AA"
        ps_conn.read_buffer(remove_header=header)
        ps_mock.assert_called_once_with(remove_header=b"AA")

    @ patch.object(TdkZupController, 'init_buffer')
    def test_init_buffer(self, ps_mock: MagicMock):
        ps_conn = TdkZupController()
        ps_conn.init_buffer()
        ps_mock.assert_called_once_with()


if __name__ == '__main__':
    unittest.main()
