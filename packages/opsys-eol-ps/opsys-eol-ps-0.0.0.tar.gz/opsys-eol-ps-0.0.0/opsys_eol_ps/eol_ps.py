# API for reading power supply parameters via MODBUS-RTU.
import minimalmodbus

# GLOBAL VARIABLES


#################
# MODBUS METHODS
#################
class EolPs():
    def __init__(self, com_num):
        self.PS_UNIT_ID = 1
        self.MODBUS_CONN = None
        # self.init_modbus_conn(com_num)

    def init_modbus_conn(self, com_num):
        try:
            self.MODBUS_CONN = minimalmodbus.Instrument("COM" + str(com_num), self.PS_UNIT_ID)
            self.MODBUS_CONN.serial.parity = 'E'
        except:
            raise

    def read_reg(self, reg_adr, func_code):
        try:
            return self.MODBUS_CONN.read_register(registeraddress = reg_adr, number_of_decimals = 0, functioncode = func_code, signed = False)
        except:
            raise

    def read_input_reg(self, reg_adr):
        input_func_code = 4
        try:
            return self.read_reg(reg_adr, input_func_code)
        except:
            raise

    def read_holding_reg(self, reg_adr):
        holding_func_code = 3
        try:
            return self.read_reg(reg_adr, holding_func_code)
        except:
            raise

    def write_holding_reg(self, reg_adr, value):
        try:
            self.MODBUS_CONN.write_register(registeraddress = reg_adr, value = value, number_of_decimals = 0, functioncode = 6, signed = False)
        except:
            raise

    #####################
    # PS SPECIFIC METHODS
    #####################

    def get_output_state(self, ):
        return self.read_holding_reg(5) != 0

    def set_output_state(self, mode):
        value = 0
        if(mode):
            value = 1
        self.write_holding_reg(5, value)


    def get_volt_limit(self, ):
        value = self.read_holding_reg(103)
        return self.convert_dtoa_volts(value)

    def set_volt_limit(self, volts):
        value = 12
        if (volts <= value):
            value = volts
        self.write_holding_reg(103, self.convert_atod_volts(value))

    def get_volt_monitor(self, ):
        value = self.read_input_reg(1)
        return self.convert_dtoa_volts(value)


    def get_current_limit(self, ):
        value = self.read_holding_reg(104)
        return self.convert_dtoa_current(value)

    def set_current_limit(self, current):
        self.write_holding_reg(104, self.convert_atod_current(current))

    def get_current_monitor(self, ):
        value = self.read_input_reg(2)
        return self.convert_dtoa_current(value)


    def get_upper_volt_lim(self, ):
        value = self.read_holding_reg(105)
        return self.convert_dtoa_volts(value)

    def set_upper_volt_lim(self, volts):
        self.write_holding_reg(105, self.convert_atod_volts(volts))


    # Alarm history is reset when turning output ON
    def is_alarm_active(self, ):
        return self.read_input_reg(0) != 0


    #################
    # UTILITY METHODS
    #################

    # Input is 0-1024 scale, output is 0-24V
    def convert_dtoa_volts(self, d_volts):
        return round((d_volts*24)/1024,2)

    # Input is 0-24V scale, output is 0-1024
    def convert_atod_volts(self, a_volts):
        return round((a_volts*1024)/24,2)


    # Input is 0-1024 scale, output is 0-12A
    def convert_dtoa_current(self, d_amp):
        return round((d_amp*25)/1024,2)

    # Input is 0-12A scale, output is 0-1024
    def convert_atod_current(self, a_amp):
        return round((a_amp*1024)/25,2)
