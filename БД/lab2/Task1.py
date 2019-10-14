from tkinter import *
import constant as con


def create_action_menu(table_name):
    con.current_table = table_name
    con.create_button(con.frame, "Select", con.select, 1,3)


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
    con.create_button(con.frame, con.Assortment_str, assortment_table_use, 1, 2)
    con.create_button(con.frame, con.Commodity_str, commodity_table_use, 2, 2)
    con.create_button(con.frame, con.Customer_str, customer_table_use, 3, 2)
    con.create_button(con.frame, con.Order_str, order_table_use, 4, 2)
    con.create_button(con.frame, con.Shop_str, shop_table_use, 5, 2)
    con.create_button(con.frame, con.Worker_str, worker_table_use, 6, 2)
