'''window with lion image and moving text'''
from threading import Thread
from os.path import join as path_join
import customtkinter as tk
from PIL import Image, ImageTk

class image_window(tk.CTk):
    '''window with lion image and moving text wich closes it'''
    def __init__(self):
        super().__init__()
        # self.parent=parent
        tk.set_appearance_mode('System')
        tk.set_default_color_theme('dark-blue')

        self.overrideredirect(True)
        self.attributes('-topmost', True)

        self.image=Image.open(path_join('.','img','lion.jpg'))
        self.image_tk=ImageTk.PhotoImage(self.image)
        self.maxwidth, self.maxheight=self.image.size

        self.canvas=tk.CTkCanvas(self, bd=0, highlightthickness=0, relief='ridge')
        self.canvas.create_image(self.winfo_width()/2,self.winfo_height()/2,image=self.image_tk, anchor='center')

        self.canvas.pack(fill="both", expand=True)
        stop=self.canvas.create_text(100, 100, anchor='c', text='STOP IT', fill='#ffaf00', font=('',36,'bold'), justify='center')
        self.canvas.tag_bind(stop, '<Button-1>', self.image_click)

        self.geometry(f'+{int((self.winfo_screenwidth()-self.winfo_width())/2)}'\
                      f'+{int((self.winfo_screenheight()-self.winfo_height())/2)}')

        self.grow=True
        self.text_move_up=True
        self.step=0
        self.after(10, self.resize)

    def image_click(self, _):
        '''closes window by clicking on STOP IT text'''
        self.canvas.delete('all')
        self.image.close()
        self.destroy()

    def resize(self):
        '''resizes window and moves "STOP IT" text'''
        self.step+=1
        if self.grow:
            if (width:=self.winfo_width()+1)>=self.maxwidth: width=self.maxwidth
            if (heigth:=self.winfo_height()+1)>=self.maxheight: heigth=self.maxheight
            if width==self.maxwidth and heigth==self.maxheight: self.grow=False
        else:
            if (width:=self.winfo_width()-1)<=200: width=200
            if (heigth:=self.winfo_height()-1)<=200: heigth=200
            if width==200 and heigth==200: self.grow=True

        if self.text_move_up:
            if (text_y:=int(heigth/2-self.step))<=100:
                text_y=100
                self.step=0
                self.text_move_up=False
        else:
            if (text_y:=int(heigth/2+self.step))>=heigth-100:
                text_y=100
                self.step=0
                self.text_move_up=True

        self.geometry(f'{width}x{heigth}')
        self.geometry(f'+{int((self.winfo_screenwidth()-width)/2)}'\
                        f'+{int((self.winfo_screenheight()-heigth)/2)}')
        self.canvas.delete('all')
        self.canvas.create_image(width/2,heigth/2,image=self.image_tk, anchor='center')
        stop=self.canvas.create_text(width/2,text_y, anchor='c', text='STOP IT', fill='#ffaf00', font=('',36,'bold'), justify='center')
        self.canvas.tag_bind(stop, '<Button-1>', self.image_click)

        self.after(10, self.resize)


class image_window_thread(Thread):
    def __init__(self):
        super().__init__()

    def run(self):
        # p=tk.CTk()
        window=image_window()
        window.mainloop()


if __name__=='__main__':
    image_window_thread().start()
