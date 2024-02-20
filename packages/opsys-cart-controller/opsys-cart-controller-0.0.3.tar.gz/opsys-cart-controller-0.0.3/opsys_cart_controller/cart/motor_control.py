import requests
from configs import MotorConfigurations


def init_com():
    """
    Initialize communication session with motor
    """
    try:
        req_format = "init?com={:d}"
        req = req_format.format(MotorConfigurations.COM)
        # get response from server
        _ = requests.get(MotorConfigurations.TARGET_URL + req)
        
    except Exception as e:
        print(f'Initializing motor COM error: {e}')
        raise


def close_com():
    """
    Close communication session with motor
    """
    try:
        req_format = "close?com={:d}"
        req = req_format.format(MotorConfigurations.COM)
        # get response from server
        _ = requests.get(MotorConfigurations.TARGET_URL + req)
        
    except Exception as e:
        print(f'Motor disconnect error: {e}')
        raise


def rel_pos(pos, velocity=80, accel=20000, decel=20000):
    """
    Move motor by relative position in meters

    Args:
        pos (int): current cart position in meters
        velocity (int, optional): cart velocity. Defaults to 80.
        accel (int, optional): cart acceleration. Defaults to 20000.
        decel (int, optional): cart deceleration. Defaults to 20000.
    """
    try:
        req_format = "rel_pos?com={:d}&pos={:d}&velocity={:d}&accel={:d}&deccel={:d}"
        
        req = req_format.format(
            MotorConfigurations.COM,
            int(pos * MotorConfigurations.STEPS_TO_METER),
            velocity,
            accel,
            decel
        )
        
        _ = requests.get(MotorConfigurations.TARGET_URL + req)
        
    except Exception as e:
        print(f'Relative cart move error: {e}')
        raise
    
    
def abs_pos(laser_conn, pos, velocity=80, accel=20000, decel=20000):
    """
    Move motor to absolute position in meters

    Args:
        laser_com (LaserDistance): laser serial connection instance
        pos (int): current cart position in meters
        velocity (int, optional): cart velocity. Defaults to 80.
        accel (int, optional): cart acceleration. Defaults to 20000.
        decel (int, optional): cart deceleration. Defaults to 20000.
    """
    try:   
        current_pos = laser_conn.read_dist()
        target_pos = pos - current_pos
        rel_pos(target_pos, velocity, accel, decel)
        
    except Exception as e:
        print(f'Absolute cart move error: {e}')
        raise


def e_stop():
    """
    Send motor EMERGENCY STOP command
    """
    try:
        req_format = "estop?com={:d}"
        req = req_format.format(MotorConfigurations.COM)
        # get response from server
        _ = requests.get(MotorConfigurations.TARGET_URL + req)
        
    except Exception as e:
        print(f'Cart emergency stop error: {e}')
        raise


def move_status():
    """
    Read motor movement status

    Returns:
        str: "move" if moving, else "stop"
    """
    try:
        req_format = "move_status?com={:d}"
        req = req_format.format(MotorConfigurations.COM)
        # get response from server
        response = requests.get(MotorConfigurations.TARGET_URL + req)
        
        return response.text
    
    except Exception as e:
        print(f'Cart movement status read error: {e}')
        raise
