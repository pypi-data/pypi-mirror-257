from abc import ABC, abstractmethod


class CartAbstract(ABC):
    @abstractmethod
    def setup_cart_motor(self, laser_com: int, ps_com: int):
        pass
    
    @abstractmethod
    def move_to_start(self):
        pass
    
    @abstractmethod
    def move_to_end(self):
        pass
    
    @abstractmethod
    def move_cart_motor(self, dest: int):
        pass
    
    @abstractmethod
    def get_distance(self):
        pass
    
    @abstractmethod
    def stop_cart(self):
        pass
    