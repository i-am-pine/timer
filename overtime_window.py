'''window to show overtime after the timer is closed'''
from threading import Thread
import customtkinter as tk

class overtime_window(tk.CTk):
    '''Window whith a string text with overtime and buttons Copy (to copy that string) and Close'''
    def __init__(self, message="you've overworked"):
        super().__init__()
        tk.set_appearance_mode('System')
        tk.set_default_color_theme('dark-blue')

        self.attributes('-alpha',0.8)

        frame=tk.CTkFrame(self, bg_color='transparent',fg_color='transparent')
        frame.pack(padx=20, pady=15, fill='both', expand=True)

        label=tk.CTkLabel(frame, text=message.upper() ,font=('', 24, 'bold') , )
        label.pack(pady=10)

        buttonsFrame=tk.CTkFrame(frame, bg_color='transparent',fg_color='transparent')
        buttonsFrame.pack()

        buttonCopy=tk.CTkButton(buttonsFrame, text='Copy', width=70, height=10, 
                                command=lambda:[self.clipboard_clear(), self.clipboard_append(message)])
        buttonOK=tk.CTkButton(buttonsFrame, text='Close', width=70, height=10, command=self.destroy)
        buttonCopy.grid(column=0, row=0, padx=5)
        buttonOK.grid(column=1, row=0, padx=5)

        self.geometry(f'+{int((self.winfo_screenwidth()-self.winfo_width())/2)}'\
                      f'+{int((self.winfo_screenheight()-self.winfo_height())/2)}')
        
        self.overrideredirect(True)
        self.attributes('-topmost', True)

class overtime_thread(Thread):
    '''thread to start this window'''
    def __init__(self, message = "you've overworked"):
        super().__init__()
        self.message=message

    def run(self):
        window=overtime_window(self.message)
        window.mainloop()

'''for test purposes'''
if __name__=='__main__':
    # overtime_window().mainloop()
    overtime_thread().start()