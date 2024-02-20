import serial
from time import sleep
from configs import PowerSupplyConfigurations


class PsParams:
    volt_cmd = b'\x01\x04\x00\x01\x00\x01\x60\x0A'
    curr_cmd = b'\x01\x04\x00\x02\x00\x01\x90\x0A'
    buffer_size = 8
    sleep_time = 0.1
    
    def __init__(self):
        self.serial_conn = None

    def init_com(self, com_port):
        """
        Initialize COM port session with PS

        Args:
            com_port (int): COM port number
        """
        try:
            self.serial_conn = serial.Serial('COM' + str(com_port), 
                                    PowerSupplyConfigurations.BAUDRATE, 
                                    parity=serial.PARITY_EVEN, 
                                    timeout=PowerSupplyConfigurations.COM_TIMEOUT
                                    )
            
            sleep(self.sleep_time)
            
            self.serial_conn.flushInput()
            self.serial_conn.flushOutput()
            
        except Exception as e:
            print(f'Initializing PS COM error: {e}')
            raise

    def close_com(self):
        """
        Close com port session with PS
        """    
        try:
            if self.serial_conn is not None:
                self.serial_conn.close()
                self.serial_conn = None
                
        except Exception as e:
            print(f'PS disconnect error: {e}')
            raise

    def read_volt(self):
        """
        Read voltage from power supply

        Returns:
            float: PS voltage in Volts
        """        
        try:
            if self.serial_conn is None:
                raise ConnectionError('Must initialize COM port before reading!')
            
            
            self.serial_conn.write(self.volt_cmd)
            sleep(self.sleep_time)
            reply = self.serial_conn.read(self.buffer_size)
            a_val = int.from_bytes(reply[3:5],'big')  # analog value 0-1024. 1024==48V
            
            return round((a_val * 48) / 1024, 2)
        
        except Exception as e:
            print(f'PS voltage read error: {e}')
            raise

    def read_current(self):
        """
        Read current from power supply

        Returns:
            float: PS current in Ampers
        """        
        try:
            if self.serial_conn is None:
                raise ConnectionError('Must initialize COM port before reading!')
            
            self.serial_conn.write(self.curr_cmd)
            sleep(self.sleep_time)
            reply = self.serial_conn.read(self.buffer_size)
            a_val = int.from_bytes(reply[3:5], 'big') # analog value 0-1024. 1024==12.5A
            
            return round((a_val * 12.5) / 1024, 2)
        
        except Exception as e:
            print(f'PS current read error: {e}')
            raise
