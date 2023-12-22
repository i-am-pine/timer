'''functions wich help not to get too cozy'''
from os.path import join as path_join
from sys import executable as actual_python
from threading import Thread, Event
import json
from time import sleep
import subprocess
import pyautogui
from parameters import DISTURBANCE_INTERVAL
# from time_over_window import time_over_thread
# from image_window import image_window_thread

class disturbing_actions:
    '''class with actions which remind to leave the computer'''
    def __init__(self) -> None:
        pass

    @staticmethod
    def print(message):
        '''prints message'''
        print(message)

    @staticmethod
    def show_window(**kwargs):
        '''shows window with message using subprocess 
        because tkinter windows outside main thread fight with each other'''
        # time_over_thread(**kwargs).start()
        params=''
        if 'message' in kwargs: params+=' -m "'+kwargs['message']+'"'
        if 'message_color' in kwargs: params+=' -c "'+kwargs['message_color']+'"'
        if 'fg_color' in kwargs: params+=' -f "'+kwargs['fg_color']+'"'
        Thread(target=subprocess.call, args=[actual_python+' time_over_window.py'+params]).start()

    @staticmethod
    def open_notepad(**kwargs):
        '''opens notepad and writes text in it'''
        thead=Thread(target=disturbing_actions.open_notepad_thread, kwargs=kwargs,)
        thead.start()

    @staticmethod
    def open_notepad_thread(message='the quick brown fox jumps over the lazy dog'):
        Thread(target=subprocess.call, args=['notepad']).start()
        sleep(0.1)
        pyautogui.write(message)
        sleep(0.3)
        pyautogui.click(pyautogui.locateCenterOnScreen(path_join('.','img','notepad.jpg'), confidence=0.8))

    @staticmethod
    def show_image_window():
        '''shows image with lion'''
        Thread(target=subprocess.call, args=[actual_python+' image_window.py']).start()


class disturbance_thread(Thread):
    '''executes actions described in disturbing_actions.json in cicle'''
    def __init__(self, json_file='disturbing_actions.json'):
        super().__init__()
        self.actions=[]
        self._stop_event=Event()
        self.json_file=json_file

    def read_json(self):
        '''read json with disturbing actions'''
        with open(self.json_file, encoding='utf-8') as file:
            self.actions = json.load(file)

    def run(self) -> None:
        '''executes actions from json file'''
        self.read_json()
        while self.not_stopped():
            for action in self.actions:
                if self.not_stopped():
                    getattr(disturbing_actions, action['action'])(**action['params'])
                    sleep(DISTURBANCE_INTERVAL)
                else:
                    return

    def not_stopped(self):
        '''check if process is stopped'''
        return not self._stop_event.is_set()

    def stop(self):
        '''that is how we stop it'''
        self._stop_event.set()
        # self.not_stopped=False


#for tests
if __name__=='__main__':
    print(actual_python)
    try:
        disturbance=disturbance_thread()
        disturbance.start()
        sleep(100)
        disturbance.stop()
    except KeyboardInterrupt:
        disturbance.stop()
