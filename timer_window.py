'''Timer window module'''

import time
from os.path import join as path_join
import customtkinter as tk
import pyautogui
from time_checker import time_checker
from parameters import MAX_TIME
from disturbance import disturbance_thread
from overtime_window import overtime_thread

tk.set_appearance_mode('System')
tk.set_default_color_theme('dark-blue')

class timer_window(tk.CTk):
    def __init__(self):
        '''Creates timer window 
        with label for time and buttons Start, Stop, Reset and Close
        '''
        super().__init__()
        self.start_time=0                       # time from when timer starts count
        self.stop_time=0                        # uses to substract time during which timer was stopped from the main count
        self.buffer=0                           # counter for time when timer didn't work
        self.time_over=False                    # true if time is more then MAX_TIME
        self.update_function=self.update_time   # function to update timer label
        self.time_checker=None                  # thread to check idle time
        self.disturbance_thread=None
        self.start_count()
        # self.start_checker()

        self.iconbitmap(path_join('.','img','icon.ico'))

        width, _ = pyautogui.size()
        self.geometry_string=f'+{width-270}+0'
        self.geometry(self.geometry_string)
        self.overrideredirect(True)
        self.attributes('-topmost', True)
        self.bind('<Map>', self.show_window)
        self.bind('<FocusOut>', self.hide_window)
        self.bind('<B1-Motion>', self.move_window)
        self.attributes('-alpha',0.8)

        frame=tk.CTkFrame(self, bg_color='transparent',fg_color='transparent')
        frame.pack(padx=20, pady=15, fill='both', expand=True)

        self.label=tk.CTkLabel(frame, text='00:00', font=('', 48, 'bold'))
        self.label.grid(column=0, row=0, columnspan=5)
        self.label.after(1000, self.update_time)

        buttonClose=tk.CTkButton(frame, text='x', width=10, height=10,
                                 command=lambda:[self.time_checker.stop(), self.destroy()])
        buttonClose.grid(column=5, row=0, sticky='ne')

        buttonStart=tk.CTkButton(frame, text='Start', width=70, height=10, command=self.start_count)
        buttonStop=tk.CTkButton(frame, text='Stop', width=70, height=10, command=self.stop_count)
        buttonReset=tk.CTkButton(frame, text='Reset', width=70, height=10, command=self.reset_count)

        buttonStart.grid(column=0, row=1, columnspan=2, sticky='w')
        buttonStop.grid(column=2, row=1, columnspan=2, padx=10)
        buttonReset.grid(column=4, row=1, columnspan=2,  sticky='e')

    def start_checker(self):
        '''Creates thread to check idle time, 
            timer stops when inactivity time > idle_time 
        '''
        if self.time_checker is not None:
            self.time_checker.stop()
        self.time_checker=time_checker()
        self.time_checker.start()
        self.check_inactivity_time()

    def check_inactivity_time(self):
        '''checks if time_checker thread is alive, 
        if not, stops count until user starts it'''
        if self.time_checker.is_alive():
            self.after(100, self.check_inactivity_time)
        else:
            self.stop_count()
            self.show_window('')

    def start_count(self):
        '''function for button Start'''
        self.start_checker()
        if self.stop_time>0:
            self.buffer+=time.time()-self.stop_time
            self.stop_time=0
        if self.start_time==0:
            self.start_time = time.time()
        self.update_function=self.update_time

    def stop_count(self):
        '''Function for button Stop'''
        self.time_checker.stop()
        self.stop_time=time.time()
        self.update_function=self.do_nothing

    def reset_count(self):
        '''Function for button Reset'''
        self.start_checker()
        if self.disturbance_thread is not None:
            self.disturbance_thread.stop()
        self.start_time=time.time()
        self.stop_time=0
        self.buffer=0
        self.update_function=self.update_time
        self.time_over=False

    def update_time(self):
        '''Updates timer label and checks if time is not over'''
        time_passed_int=time.time()-self.start_time-self.buffer
        time_passed=time.gmtime(time_passed_int)
        self.label.configure(text=time.strftime('%H:%M:%S',time_passed))
        self.title(time.strftime('%H:%M:%S',time_passed))
        self.label.after(1000, self.update_function)
        if not self.time_over and time_passed_int>MAX_TIME:
            self.time_over=True
            self.start_disturb()

    def do_nothing(self):
        '''Uses if timer is stopped to do nothing until it is started again'''
        self.label.after(1000, self.update_function)

    def show_window(self, _):
        '''shows window on screen on top right corner'''
        self.overrideredirect(True)
        self.deiconify()
        self.focus_force()
        self.geometry(self.geometry_string)

    def hide_window(self, _):
        '''When timer window is inactive it goes to task bar'''
        self.withdraw()
        self.overrideredirect(False)
        self.iconify()

    def move_window(self, event):
        '''uses to move window on the screen'''
        self.geometry(f'+{event.x_root}+{event.y_root}')

    def start_disturb(self):
        '''starts disturb you when your time is over'''
        self.disturbance_thread=disturbance_thread()
        self.disturbance_thread.start()

    def destroy(self):
        '''closes timer window'''
        if self.disturbance_thread is not None:
            self.disturbance_thread.stop()
        if self.time_checker is not None:
            self.time_checker.stop()
        super().destroy()
        if self.time_over:
            overtime_thread(self.get_overtime()).start()

    def get_overtime(self):
        '''returns string with information of overtime'''
        overtime=time.gmtime(time.time()-self.start_time-self.buffer-MAX_TIME)
        overtime_str=time.strftime('%H:%M:%S',overtime)
        return 'your overtime is: ' + overtime_str

if __name__ =='__main__':
    window=timer_window()
    window.mainloop()
