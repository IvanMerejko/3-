from tkinter import *
import constant as con

label_height = 15


def create_assortment_menu(assortment_id, commodity_id, shop_id):
    con.create_label("assortment_id", label_height, 2, 1, 4, 1, 1, "white")
    con.create_entry(assortment_id, 2, 4)
    con.create_label("commodity_id", label_height, 2, 1, 5, 1, 1, "white")
    con.create_entry(commodity_id, 2, 5)
    con.create_label("shop_i", label_height, 2, 1, 6, 1, 1, "white")
    con.create_entry(shop_id, 2, 6)


def create_commodity_menu(commodity_id, name, price):
    con.create_label("commodity_id", label_height, 2, 1, 4, 1, 1, "white")
    con.create_entry(commodity_id, 2, 4)
    con.create_label("name", label_height, 2, 1, 5, 1, 1, "white")
    con.create_entry(name, 2, 5)
    con.create_label("price", label_height, 2, 1, 6, 1, 1, "white")
    con.create_entry(price, 2, 6)


def create_customer_menu(customer_id, name, raiting, worker_id):
    con.create_label("customer_id", label_height, 2, 1, 4, 1, 1, "white")
    con.create_entry(customer_id, 2, 4)
    con.create_label("name", label_height, 2, 1, 5, 1, 1, "white")
    con.create_entry(name, 2, 5)
    con.create_label("raiting", label_height, 2, 1, 6, 1, 1, "white")
    con.create_entry(raiting, 2, 6)
    con.create_label("worker_id", label_height, 2, 1, 7, 1, 1, "white")
    con.create_entry(worker_id, 2, 7)


def create_order_menu(customer_id, order_id, assortment_id):
    con.create_label("customer_id", label_height, 2, 1, 4, 1, 1, "white")
    con.create_entry(customer_id, 2, 4)
    con.create_label("order_id", label_height, 2, 1, 5, 1, 1, "white")
    con.create_entry(order_id, 2, 5)
    con.create_label("assortment_id", label_height, 2, 1, 6, 1, 1, "white")
    con.create_entry(assortment_id, 2, 6)


def create_shop_menu(shop_id, monthly_profit, address):
    con.create_label("shop_id", label_height, 2, 1, 4, 1, 1, "white")
    con.create_entry(shop_id, 2, 4)
    con.create_label("monthly_profit", label_height, 2, 1, 5, 1, 1, "white")
    con.create_entry(monthly_profit, 2, 5)
    con.create_label("address", label_height, 2, 1, 6, 1, 1, "white")
    con.create_entry(address, 2, 6)


def create_worker_menu(worker_id, shop_id, name, surname, position):
    con.create_label("worker_id", label_height, 2, 1, 4, 1, 1, "white")
    con.create_entry(worker_id, 2, 4)
    con.create_label("shop_id", label_height, 2, 1, 5, 1, 1, "white")
    con.create_entry(shop_id, 2, 5)
    con.create_label("name", label_height, 2, 1, 6, 1, 1, "white")
    con.create_entry(name, 2, 6)
    con.create_label("surname", label_height, 2, 1, 7, 1, 1, "white")
    con.create_entry(surname, 2, 7)
    con.create_label("position", label_height, 2, 1, 8, 1, 1, "white")
    con.create_entry(position, 2, 8)


def create_delete_menu():
    remove_unused_elements()
    delete_part_fields = {con.Assortment_str: 'assortment_id',
                          con.Commodity_str: 'commodity_id',
                          con.Order_str: 'order_id',
                          con.Worker_str: 'worker_id',
                          con.Shop_str: 'shop_id',
                          con.Customer_str: 'customer_id'}
    current_field_name = delete_part_fields[con.current_table]
    value = StringVar()
    def delete_statement():
        status, result = con.execute_query(con.delete_query.format(table=con.current_table,
                                                           field=current_field_name,
                                                            value=value.get()))
        con.text_label['text'] = status
    con.create_label(current_field_name, label_height, 2, 1, 4, 1, 1, "white")
    con.create_entry(value, 2, 4)
    con.create_button('delete', delete_statement, 1, 5)


def remove_unused_elements():
    positions = con.remove_dict_for_first_task[con.current_table]
    positions += con.delete_position_for_remove
    for row, column in positions:
        con.remove_element(row, column)


def create_assortment_insert():
    assortment_id = StringVar()
    commodity_id = StringVar()
    shop_id = StringVar()
    create_assortment_menu(assortment_id, commodity_id, shop_id)
    def insert_callback():
        status, result = con.execute_query(con.insert_queries[3].format(con.current_table, assortment_id.get(),
                                                                commodity_id.get(), shop_id.get()))
        con.text_label['text'] = status
    con.create_button('Ok', insert_callback, 1, 7)
def create_assortment_select():
    assortment_id = StringVar()
    commodity_id = StringVar()
    shop_id = StringVar()
    create_assortment_menu(assortment_id, commodity_id, shop_id)
    def callback():
        con.select_callback({(assortment_id.get(), 'assortment_id'),
                             (commodity_id.get(), 'commodity_id'),
                             (shop_id.get(), 'shop_id')})

    con.create_button('select', callback, 1, 7)
def create_assortment_update():
    print()

def create_commodity_insert():
    name = StringVar()
    commodity_id = StringVar()
    price = StringVar()
    create_commodity_menu(commodity_id, name, price)
    def insert_callback():
        status, result = con.execute_query(con.insert_queries[3].format(con.current_table, commodity_id.get(),
                                                                name.get(), price.get()))
        con.text_label['text'] = status
    con.create_button('Ok', insert_callback, 1, 7)
def create_commodity_select():
    name = StringVar()
    commodity_id = StringVar()
    price = StringVar()
    create_commodity_menu(commodity_id, name, price)
    def callback():
        con.select_callback({(commodity_id.get(), 'commodity_id'),
                             (name.get(), 'name'),
                             (price.get(), 'price')})

    con.create_button('select', callback, 1, 7)


def create_customer_insert():
    customer_id = StringVar()
    name = StringVar()
    raiting = StringVar()
    worker_id = StringVar()
    create_customer_menu(customer_id, name, raiting, worker_id)
    def insert_callback():
        status, result = con.execute_query(con.insert_queries[4].format(con.current_table, customer_id.get(),
                                                                raiting.get(), worker_id.get(), name.get()))
        con.text_label['text'] = status
    con.create_button('Ok', insert_callback, 1, 8)
def create_customer_select():
    customer_id = StringVar()
    name = StringVar()
    raiting = StringVar()
    worker_id = StringVar()
    create_customer_menu(customer_id, name, raiting, worker_id)
    def callback():
        con.select_callback({(customer_id.get(), 'customer_id'),
                             (name.get(), 'name'),
                             (raiting.get(), 'raiting'),
                             (worker_id.get(), 'worker_id')})

    con.create_button('select', callback, 1, 8)


def create_order_insert():
    customer_id = StringVar()
    order_id = StringVar()
    assortment_id = StringVar()
    create_order_menu(customer_id, order_id, assortment_id)
    def insert_callback():
        status, result = con.execute_query(con.insert_queries[3].format(con.current_table, order_id.get(),
                                                                        customer_id.get(), assortment_id.get()))
        con.text_label['text'] = status
    con.create_button('Ok', insert_callback, 1, 7)
def create_order_select():
    customer_id = StringVar()
    order_id = StringVar()
    assortment_id = StringVar()
    create_order_menu(customer_id, order_id, assortment_id)
    def callback():
        con.select_callback({(customer_id.get(), 'customer_id'),
                             (order_id.get(), 'order_id'),
                             (assortment_id.get(), 'assortment_id')})

    con.create_button('select', callback, 1, 7)


def create_shop_insert():
    shop_id = StringVar()
    monthly_profit = StringVar()
    address = StringVar()
    create_shop_menu(shop_id, monthly_profit, address)
    def insert_callback():
        status, result = con.execute_query(con.insert_queries[3].format(con.current_table, shop_id.get(),
                                                                monthly_profit.get(), address.get()))
        con.text_label['text'] = status
    con.create_button('Ok', insert_callback, 1, 7)
def create_shop_select():
    shop_id = StringVar()
    monthly_profit = StringVar()
    address = StringVar()
    create_shop_menu(shop_id, monthly_profit, address)
    def callback():
        con.select_callback({(shop_id.get(), 'shop_id'),
                             (monthly_profit.get(), 'monthly_profit'),
                             (address.get(), 'address')})

    con.create_button('select', callback, 1, 7)


def create_worker_insert():
    worker_id = StringVar()
    shop_id = StringVar()
    name = StringVar()
    surname = StringVar()
    position = StringVar()
    create_worker_menu(worker_id, shop_id, name, surname, position)
    def insert_callback():
        status, result = con.execute_query(con.insert_queries[3].format(con.current_table, worker_id.get(), shop_id.get(),
                                                                name.get(), surname.get(), position.get()))
        con.text_label['text'] = status
    con.create_button('Ok', insert_callback, 1, 9)
def create_worker_select():
    worker_id = StringVar()
    shop_id = StringVar()
    name = StringVar()
    surname = StringVar()
    position = StringVar()
    create_worker_menu(worker_id, shop_id, name, surname, position)
    def callback():
        con.select_callback({(worker_id.get(), 'worker_id'),
                             (shop_id.get(), 'shop_id'),
                             (name.get(), 'name'),
                             (surname.get(), 'surname'),
                             (position.get(), 'position')})

    con.create_button('select', callback, 1, 9)

insert_creators = {con.Assortment_str: create_assortment_insert,
                   con.Commodity_str: create_commodity_insert,
                   con.Customer_str: create_customer_insert,
                   con.Order_str: create_order_insert,
                   con.Shop_str: create_shop_insert,
                   con.Worker_str: create_worker_insert}

select_creators = {con.Assortment_str: create_assortment_select,
                   con.Commodity_str: create_commodity_select,
                   con.Customer_str: create_customer_select,
                   con.Order_str: create_order_select,
                   con.Shop_str: create_shop_select,
                   con.Worker_str: create_worker_select}

def create_action_menu(table_name):
    if len(con.current_table) != 0:
        remove_unused_elements()
    con.current_table = table_name
    con.change_color(con.clicked_color_change[con.current_table])
    con.create_button("Select", select_creators[con.current_table], 1, 3)
    con.create_button("Insert", insert_creators[con.current_table], 2, 3)
    con.create_button("Delete", create_delete_menu, 3, 3)
    con.create_button("Update", create_assortment_update, 4, 3)


def assortment_table_use():
    create_action_menu(con.Assortment_str)


def commodity_table_use():

    create_action_menu(con.Commodity_str)


def customer_table_use():
    create_action_menu(con.Customer_str)


def order_table_use():
    create_action_menu(con.Order_str)


def shop_table_use():
    create_action_menu(con.Shop_str)


def worker_table_use():
    create_action_menu(con.Worker_str)


def create_menu_for_task1():
    con.create_button(con.Assortment_str, assortment_table_use, 1, 2)
    con.create_button(con.Commodity_str, commodity_table_use, 2, 2)
    con.create_button(con.Customer_str, customer_table_use, 3, 2)
    con.create_button(con.Order_str, order_table_use, 4, 2)
    con.create_button(con.Shop_str, shop_table_use, 5, 2)
    con.create_button(con.Worker_str, worker_table_use, 6, 2)
