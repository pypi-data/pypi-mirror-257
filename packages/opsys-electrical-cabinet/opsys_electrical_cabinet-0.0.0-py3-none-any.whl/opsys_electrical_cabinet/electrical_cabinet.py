# PLC MODBUS Control API
from pyModbusTCP.client import ModbusClient

class ElectricalCabinet():
    
    def __init__(self, ip_address):
        self.TCP_CONN = None

        # self.init_tcp_conn(ip_address)


    # Open TCP session with PLC
    def init_tcp_conn(self, ip_address):
        try:
            self.TCP_CONN = ModbusClient(host=ip_address, auto_open=True, auto_close=True)
        except:
            print(self.TCP_CONN)
            print("Error initializing MODBUS TCP connection to PLC")
            raise

    def read_holding_reg(self, reg_adr, reg_num):
        try:
            response = self.TCP_CONN.read_holding_registers(reg_adr, reg_num)
            return response
        except:
            print(self.TCP_CONN)
            print("Error reading register from PLC")
            raise

    # values - list of values, starting register from reg_adr
    def write_holding_reg(self, reg_adr, values):

        for val in values:
            if(val):
                val = 1
            else:
                val = 0
        try:
            response = self.TCP_CONN.write_multiple_registers(reg_adr, values)
            return response
        except:
            print(self.TCP_CONN)
            print("Error writing to register on PLC")
            raise

    # PLC SPECIFIC METHODS
    def get_gimbal_interlock_state(self):
        return self.read_holding_reg(11,1)[0]

    def set_gimbal_interlock_state(self, value):
        self.write_holding_reg(11,[value])


    def get_trx_cover_state(self):
        return self.read_holding_reg(3,1)[0]


    def get_laser_state(self):
        return self.read_holding_reg(12,1)[0]

    def set_laser_state(self, value):
        self.write_holding_reg(12,[value])

    # light_num value from [0,1,2]
    def get_light_state(self, light_num):
        adr = 0
        if (light_num in [0,1,2]):
            adr = light_num
        return self.read_holding_reg(24 + adr,1)[0]

    def set_light_state(self, light_num, value):
        adr = 0
        if (light_num in [0,1,2]):
            adr = light_num
        return self.write_holding_reg(24 + adr,[value])


    def get_gimbal_power_state(self):
        return self.read_holding_reg(8,1)[0]

    def set_gimbal_power_state(self, value):
        self.write_holding_reg(8,[value]) 


    def get_leds_power_state(self):
        return self.read_holding_reg(10,1)[0]

    def set_leds_power_state(self, value):
        self.write_holding_reg(10,[value]) 


    def get_spare_power_state(self):
        return self.read_holding_reg(9,1)[0]

    def set_spare_power_state(self, value):
        self.write_holding_reg(9,[value]) 


    def get_hw_tx_state(self):
        return self.read_holding_reg(30,1)[0]

    def set_hw_tx_state(self, value):
        self.write_holding_reg(30,[value]) 


    def get_door_interlock_state(self):
        return self.read_holding_reg(5,1)[0]




