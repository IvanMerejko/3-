from tkinter import *
import psycopg2

Assortment_str = 'assortment'
Commodity_str = 'commodity'
Customer_str = 'customer'
Order_str = 'order'
Shop_str = 'shop'
Worker_str = 'worker'

clicked_color_change = {Assortment_str: (2, 1),
                        Commodity_str: (2, 2),
                        Customer_str: (2, 3),
                        Order_str: (2, 4),
                        Shop_str: (2, 5),
                        Worker_str: (2, 6)}


remove_dict_for_first_task = {Assortment_str: [(4, 1), (5, 1), (6, 1), (4, 2), (5, 2), (6, 2), (7, 1)],
                              Commodity_str: [(4, 1), (5, 1), (6, 1), (4, 2), (5, 2), (6, 2), (7, 1)],
                              Customer_str: [(4, 1), (5, 1), (6, 1), (7, 1), (4, 2), (5, 2), (6, 2), (7, 2), (8, 1)],
                              Order_str: [(4, 1), (5, 1), (6, 1), (4, 2), (5, 2), (6, 2), (7, 1)],
                              Shop_str: [(4, 1), (5, 1), (6, 1), (4, 2), (5, 2), (6, 2), (7, 1)],
                              Worker_str: [(4, 1), (5, 1), (6, 1), (7, 1), (8, 1), (4, 2), (5, 2), (6, 2), (7, 2), (8, 2), (9, 1)]}

insert_queries = {3: 'INSERT INTO \"{0}\"VALUES ({1},{2},{3})',
                  4: 'INSERT INTO \"{0}\"VALUES ({1},{2},{3},{4})',
                  5: 'INSERT INTO \"{0}\"VALUES ({1},{2},{3},{4},{5})'}

delete_query = 'Delete From \"{table}\" Where {field} = {value}'
delete_position_for_remove = [(4, 1), (4, 2), (5, 1)]
current_table = ''


def create_label(name, width, height, column_number,row_number=1, columnspan=9, rowspan=5, color="light blue"):
    label = Label(text=name, width=width, height=height, bg=color)
    label.grid(row=row_number, column=column_number, columnspan=columnspan, rowspan=rowspan,pady=1)
    return label


def create_button(name, callback, column_number, row_number=1):
    button = Button(text=name, command=callback)
    button.grid(row=row_number, column=column_number, padx=5, pady=3)
    return button


def create_entry(var_text, column_number, row_number):
    entry = Entry(textvariable=var_text)
    entry.grid(row=row_number, column=column_number, padx=1, pady=1)
    return entry

HEIGHT = 800
WIDTH = 600
window = Tk()
window.minsize(width=100, height=100)
window.geometry('{0}x{1}'.format(HEIGHT, WIDTH))
window.title("lab2")
window.grid_columnconfigure(4, minsize=100)
text_label = create_label('', 130, 20, 1, 10)
connection = psycopg2.connect(user = "postgres",
                              password = "bdfy45231",
                              port = "1111",
                              database = "test")
cursor = connection.cursor()


def select():
    print(current_table)
    cursor.execute("SELECT * FROM \"{0}\";".format(current_table))
    connection.commit()
    result = None
    text_label['text'] = ''
    for record in cursor.fetchall():
        text_label['text'] += str(record) + '\n'





def remove_element(row, column):
    for element in window.grid_slaves():
        if element.grid_info()["row"] == row and element.grid_info()["column"] == column:
            element.grid_forget()
            return


def change_color(pos):
    row, column = pos[0], pos[1]
    for element in window.grid_slaves():
        if element.grid_info()["row"] == row and element.grid_info()["column"] == column:
            element.config(bg="light blue")
        else:
            element.config(bg="white")


def execute_query(query):
    try:
        cursor.execute(query)
        connection.commit()
        return 'Ok'
    except Exception as err:
        connection.commit()
        return err

