import unittest
from unittest.mock import patch, MagicMock
from opsys_electrical_cabinet.electrical_cabinet import ElectricalCabinet


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

    @ patch.object(ElectricalCabinet, 'get_door_interlock_state')
    def test_get_door_interlock_state(self, ec_mock: MagicMock):
        ec = ElectricalCabinet("192.168.0.2")
        ec.get_door_interlock_state()
        ec_mock.assert_called_once_with()

    @ patch.object(ElectricalCabinet, 'get_gimbal_interlock_state')
    def test_get_gimbal_interlock_state(self, ec_mock: MagicMock):
        ec = ElectricalCabinet("192.168.0.2")
        ec.get_gimbal_interlock_state()
        ec_mock.assert_called_once_with()

    @ patch.object(ElectricalCabinet, 'get_gimbal_power_state')
    def test_get_gimbal_power_state(self, ec_mock: MagicMock):
        ec = ElectricalCabinet("192.168.0.2")
        ec.get_gimbal_power_state()
        ec_mock.assert_called_once_with()

    @ patch.object(ElectricalCabinet, 'get_hw_tx_state')
    def test_get_hw_tx_state(self, ec_mock: MagicMock):
        ec = ElectricalCabinet("192.168.0.2")
        ec.get_hw_tx_state()
        ec_mock.assert_called_once_with()

    @ patch.object(ElectricalCabinet, 'get_laser_state')
    def test_get_laser_state(self, ec_mock: MagicMock):
        ec = ElectricalCabinet("192.168.0.2")
        ec.get_laser_state()
        ec_mock.assert_called_once_with()

    @ patch.object(ElectricalCabinet, 'get_leds_power_state')
    def test_get_leds_power_state(self, ec_mock: MagicMock):
        ec = ElectricalCabinet("192.168.0.2")
        ec.get_leds_power_state()
        ec_mock.assert_called_once_with()

    @ patch.object(ElectricalCabinet, 'get_light_state')
    def test_get_light_state(self, ec_mock: MagicMock):
        ec = ElectricalCabinet("192.168.0.2")
        ec.get_light_state()
        ec_mock.assert_called_once_with()

    @ patch.object(ElectricalCabinet, 'get_spare_power_state')
    def test_get_spare_power_state(self, ec_mock: MagicMock):
        ec = ElectricalCabinet("192.168.0.2")
        ec.get_spare_power_state()
        ec_mock.assert_called_once_with()

    @ patch.object(ElectricalCabinet, 'get_trx_cover_state')
    def test_get_trx_cover_state(self, ec_mock: MagicMock):
        ec = ElectricalCabinet("192.168.0.2")
        ec.get_trx_cover_state()
        ec_mock.assert_called_once_with()

    @ patch.object(ElectricalCabinet, 'init_tcp_conn')
    def test_init_tcp_conn(self, ec_mock: MagicMock):
        ec = ElectricalCabinet("192.168.0.2")
        ec.init_tcp_conn()
        ec_mock.assert_called_once_with()

    @ patch.object(ElectricalCabinet, 'read_holding_reg')
    def test_read_holding_reg(self, ec_mock: MagicMock):
        ec = ElectricalCabinet("192.168.0.2")
        ec.read_holding_reg()
        ec_mock.assert_called_once_with()

    @ patch.object(ElectricalCabinet, 'set_gimbal_interlock_state')
    def test_set_gimbal_interlock_state(self, ec_mock: MagicMock):
        ec = ElectricalCabinet("192.168.0.2")
        ec.set_gimbal_interlock_state()
        ec_mock.assert_called_once_with()

    @ patch.object(ElectricalCabinet, 'set_gimbal_power_state')
    def test_set_gimbal_power_state(self, ec_mock: MagicMock):
        ec = ElectricalCabinet("192.168.0.2")
        ec.set_gimbal_power_state()
        ec_mock.assert_called_once_with()

    @ patch.object(ElectricalCabinet, 'set_hw_tx_state')
    def test_set_hw_tx_state(self, ec_mock: MagicMock):
        ec = ElectricalCabinet("192.168.0.2")
        ec.set_hw_tx_state()
        ec_mock.assert_called_once_with()

    @ patch.object(ElectricalCabinet, 'set_laser_state')
    def test_set_laser_state(self, ec_mock: MagicMock):
        ec = ElectricalCabinet("192.168.0.2")
        ec.set_laser_state()
        ec_mock.assert_called_once_with()

    @ patch.object(ElectricalCabinet, 'set_leds_power_state')
    def test_set_leds_power_state(self, ec_mock: MagicMock):
        ec = ElectricalCabinet("192.168.0.2")
        ec.set_leds_power_state()
        ec_mock.assert_called_once_with()

    @ patch.object(ElectricalCabinet, 'set_light_state')
    def test_set_light_state(self, ec_mock: MagicMock):
        ec = ElectricalCabinet("192.168.0.2")
        ec.set_light_state()
        ec_mock.assert_called_once_with()

    @ patch.object(ElectricalCabinet, 'set_spare_power_state')
    def test_set_spare_power_state(self, ec_mock: MagicMock):
        ec = ElectricalCabinet("192.168.0.2")
        ec.set_spare_power_state()
        ec_mock.assert_called_once_with()

    @ patch.object(ElectricalCabinet, 'write_holding_reg')
    def test_write_holding_reg(self, ec_mock: MagicMock):
        ec = ElectricalCabinet("192.168.0.2")
        ec.write_holding_reg()
        ec_mock.assert_called_once_with()
if __name__ == '__main__':
    unittest.main()
