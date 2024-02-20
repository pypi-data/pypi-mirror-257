import serial
from time import sleep
from configs import LaserConfigurations


class LaserDistance:
    read_cmd = b'\xAA\x00\x00\x20\x00\x01\x00\x00\x21'
    sleep_time = 0.1
    buffer_size = 13
    
    def __init__(self):
        self.serial_conn = None
    
    def init_com(self, com_port):
        """
        Initialize COM port session with laser

        Args:
            com_port (int): COM port number
        """
        try:            
            self.serial_conn = serial.Serial('COM' + str(com_port), 
                                    LaserConfigurations.BAUDRATE, 
                                    timeout=LaserConfigurations.COM_TIMEOUT
                                    )
            self.serial_conn.rts = True
            
            sleep(self.sleep_time)
            self.serial_conn.rts = False
            sleep(3)
            
            self.serial_conn.flushInput()
            self.serial_conn.flushOutput()
            
        except Exception as e:
            print(f'Initializing laser COM error: {e}')
            raise

    def close_com(self):
        """
        Close COM port session with laser
        """
        try:            
            if self.serial_conn is not None:
                self.serial_conn.close()
                self.serial_conn = None
                
        except Exception as e:
            print(f'Laser disconnect error: {e}')
            raise

    def read_dist(self):
        """
        Read distance from laser

        Returns:
            float: distance round value in meters
        """
        try:            
            if self.serial_conn is None:
                raise ConnectionError('Must initialize COM port before reading!')
            
            self.serial_conn.write(self.read_cmd)
            reply = self.serial_conn.read(self.buffer_size)
            dist = int.from_bytes(reply[6:10], 'big')  # returns value in mm
            
            return round(dist / 1000, 3)
        
        except Exception as e:
            print(f'Distance read error: {e}')
            raise
