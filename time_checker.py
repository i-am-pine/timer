'''module to check idle time to stop timer if computer is inactive '''
from time import time, sleep
from threading import Thread, Event
from pynput import mouse, keyboard
from parameters import IDLE_TIME

class UserInactiveExeption(Exception):
    pass

class time_checker(Thread):
    '''controls if user is active, stops when it is inactive during IDLE_TIME from parameters.py'''
    def __init__(self):
        super().__init__()
        self.prev_time=None
        self.keyboard_listener=None
        self.mouse_listener=None
        self._stop_event=Event()

    def run(self):
        self.prev_time = [time()]
        # self.not_stopped=True

        self.keyboard_listener = keyboard.Listener(on_press=self.update_time)
        self.mouse_listener = mouse.Listener(on_click=self.update_time, 
                                             on_scroll=self.update_time,
                                             on_move=self.update_time)
        with self.keyboard_listener, self.mouse_listener:
            try:
                while self.not_stopped():
                    sleep(0.1)
                    self.check_time()
            except UserInactiveExeption:
                return False

    def update_time(self, *args):
        self.prev_time[0]=time()

    def check_time(self):
        if time()-self.prev_time[0]>IDLE_TIME:
            self.keyboard_listener.stop()
            self.mouse_listener.stop()
            raise UserInactiveExeption
    
    def not_stopped(self):
        return not self._stop_event.is_set()
        
    def stop(self):
        self._stop_event.set()
