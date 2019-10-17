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

insert_query = 'INSERT INTO \"{table}\"VALUES {values}'

delete_query = 'Delete From \"{table}\" Where {field} = {value}'
select_query = 'Select {fields} from \"{table}\"'
update_query = 'Update \"{table}\" Set {fields} Where {primary_key}'
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


def create_filters_in_query(query, fields):
    filters = []
    for field, field_name in fields:
        if len(str(field)) > 0:
            filters.append(' {0} = {1} '.format(field_name, field))
    filters_count = len(filters)
    if filters_count > 0:
        query += ' WHERE'
        query += filters[0]
        for i in range(1, filters_count):
            if len(filters[i]) > 0:
                query += ' AND '
                query += filters[i]
    return query


def select_callback(fields_value):
    query = select_query
    fields = '*'
    query = create_filters_in_query(query, fields_value)
    status, result = execute_query(query.format(fields=fields, table=current_table))
    text_label['text'] = str(status) + '\n' + str(result)

def update_callback(primary_key, new_fields):
    primary_key_value, primary_key_name = primary_key
    if len(str(primary_key_value)) == 0:
        text_label["text"] = 'Please set value to primary key ({name})'.format(name=primary_key_name)
        return
    primary_key_part = "{name} = {value}".format(name=primary_key_name, value=primary_key_value)
    fields_part = ''
    for field_value, field_name in new_fields:
        if len(str(field_value)) != 0:
            fields_part += " {name} = {value} ".format(name=field_name, value=field_value)
    if len(fields_part) == 0:
        text_label["text"] = 'Please set new value minimum for one field'.format(name=primary_key_name)
        return
    status, result = execute_query(update_query.format(table=current_table,
                                                       fields=fields_part,
                                                       primary_key=primary_key_part), False)
    text_label['text'] = str(status) + '\n' + str(result)


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


def execute_query(query, is_need_to_fetch=True):
    try:
        cursor.execute(query)
        if not is_need_to_fetch:
            return 'Ok', ''
        result = ''
        for record in cursor.fetchall():
            result += str(record) + '\n'
        connection.commit()
        return 'Ok', result
    except Exception as err:
        connection.commit()
        return err, ''

