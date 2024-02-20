class CartConfigurations:
    """
    Cart configurations
    """
    DEVIATION = 0.10  # Cart distance deviation
    VELOCITY = 200    # Motor velocity
    ACCEL = 300000    # Acceleration
    DECEL = 1500000   # Deceleration
    TIMEOUT = 60      # Maximal step timeout

    
class LaserConfigurations:
    """
    Laser configurations
    """
    COM = 10          # Laser COM port number
    BAUDRATE = 19200  # COM port baudrate
    COM_TIMEOUT = 1   # COM port timeout
    
    
class MotorConfigurations:
    """
    Cart motor configurations
    """
    TARGET_URL = "http://192.168.1.212:5000/"  # controlling motor by http requests
    COM = 5                                    # COM Port assigned by motor PC
    STEPS_TO_METER = 46500                     # amount of motor steps in 1 meter
    
    
class PowerSupplyConfigurations:
    """
    Power supply configurations
    """
    COM = 8            # PS COM port number
    BAUDRATE = 19200   # COM port baudrate
    COM_TIMEOUT = 0.5  # COM port timeout
