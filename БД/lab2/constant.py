from tkinter import *
import psycopg2
Assortment_str = "assortment"
Commodity_str = "commodity"
Customer_str = "customer"
Order_str = "order"
Shop_str = "shop"
Worker_str = "worker"

current_table = ""


WIDTH = 600
HEIGHT = 500
window = Tk()
window.minsize(width=100, height=100)
window.geometry('600x500')
window.title("lab2")
window.grid_columnconfigure(4, minsize=100)
text_label = Label(width=100, height=5, bg="light blue")
text_label.grid(row=10, column=1, columnspan=9, rowspan=5)
connection = psycopg2.connect(user = "postgres",
                              password = "bdfy45231",
                              port = "1111",
                              database = "test")
cursor = connection.cursor()


def select():
    print(current_table)
    cursor.execute("SELECT * FROM \"{0}\";".format(current_table))
    records = cursor.fetchall()
    text_label['text'] = records
    # for record in records:
    #     text_label['text'] += record



def create_button(name, callback, column_number, row_number=1):
    print(name, row_number, column_number)
    button = Button(text=name, command=callback)
    button.grid(row=row_number, column=column_number, padx=5, pady=3)