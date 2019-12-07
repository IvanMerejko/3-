from tkinter import *
from constant import *
from Task1 import create_menu_for_task1
from Task2 import create_menu_for_task2
import Controller
import View
import Model

if __name__=="__main__":
    controller = Controller.Controller(Model.Model(), View.View())
