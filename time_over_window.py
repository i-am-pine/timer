'''basic window with message and 3 buttons'''
import customtkinter as tk
import pyautogui
from threading import Thread
from time import sleep
import gc
import click

class time_over_window(tk.CTk):
    '''window with text message and three buttons'''
    def __init__(self, message = 'time is over', message_color='#FF6631', fg_color='#4E4E4E', **kwargs):
        super().__init__(fg_color, **kwargs)
        tk.set_appearance_mode('System')
        tk.set_default_color_theme('dark-blue')

        width, height = pyautogui.size()
        self.geometry(f'+{int((width-530)/2)}+{int((height-120)/2)}')

        self.overrideredirect(True)
        self.attributes('-topmost', True)

        frame=tk.CTkFrame(self, bg_color='transparent',fg_color='transparent')
        frame.pack(padx=20, pady=15, fill='both', expand=True)

        self.label=tk.CTkLabel(frame, text=message.upper(), font=('', 48, 'bold'), text_color=message_color)
        self.label.grid(column=0, row=0, columnspan=3, pady=5)

        button1=tk.CTkButton(frame, text='Ok', width=150, height=10, command=self.destroy) 
        button2=tk.CTkButton(frame, text='Yes', width=150, height=10, command=self.destroy)
        button3=tk.CTkButton(frame, text='I am a workaholic', width=150, height=10, command=self.destroy)

        button1.grid(column=0, row=1, sticky='w', pady=5)
        button2.grid(column=1, row=1, padx=20)
        button3.grid(column=2, row=1, sticky='e')


class time_over_thread(Thread):
    '''thread to start this window, to avoid tkinter windows to fight with each other'''
    def __init__(self, message = 'time is over', message_color='#FF6631', fg_color='#4E4E4E',):
        super().__init__()
        self.message=message
        self.fg_color=fg_color
        self.message_color=message_color

    def run(self):
        window=time_over_window(self.message, self.message_color, self.fg_color)
        window.mainloop()

@click.command()
@click.option('--message', '-m',  type=click.STRING, help='message for window')
@click.option('--message-color', '-c', type=click.STRING, help='color of letters')
@click.option('--fg-color', '-f',type=click.STRING, help='color of window')
def process_args(**kwargs):
    # kwargs_for_window=dict(filter(lambda value: value[1] is not None, kwargs.items()))
    time_over_window(**{key: value for key, value in kwargs.items() if value is not None}).mainloop()
    
if __name__ =='__main__':
    # time_over_thread().start()
    process_args()
