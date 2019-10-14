from tkinter import *
from constant import *
from Task1 import create_menu_for_task1




def create_window():
    create_button(frame, "Task1", create_menu_for_task1, 1)
    window.mainloop()

if __name__=="__main__":
    create_window()