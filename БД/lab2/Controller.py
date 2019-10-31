from tkinter import *
import psycopg2


class Controller:
    Assortment_str = 'assortment'
    Commodity_str = 'commodity'
    Customer_str = 'customer'
    Order_str = 'order'
    Shop_str = 'shop'
    Worker_str = 'worker'
    Empty_str = ''

    tables_number = {1: Assortment_str,
                     2: Commodity_str,
                     3: Customer_str,
                     4: Order_str,
                     5: Shop_str,
                     6: Worker_str}

    tables_columns = {Assortment_str: ["assortment_id", "commodity_id", "order_id"],
                      Commodity_str: ["commodity_id", "name", "price"],
                      Customer_str: ["customer_id", "name", "raiting", "worker_id"],
                      Order_str: ["customer_id", "order_id", "assortment_id"],
                      Shop_str: ["shop_id", "monthly_profit", "address"],
                      Worker_str: ["worker_id", "shop_id", "name", "surname", "position"]}


    current_table = None
    action = None

    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.start()

    def print_table(self, parameters):
        tables_print_function = {self.Assortment_str: self.view.print_assortment,
                                 self.Commodity_str:  self.view.print_commodity,
                                 self.Customer_str:   self.view.print_customer}
        tables_print_function[self.current_table](parameters)

    def print_columns_titles(self):
        columns = self.tables_columns[self.current_table]
        size = len(columns)
        for i in range(0, size):
            print("{number} for {column}".format(number=i, column=columns[i]))

    def start(self):
        while True:
            self.view.tables_menu()
            try:
                table = int(input())
                self.current_table = self.tables_number[table]
                self.view.action_menu()
                action_numbers = {1: self.select_action,
                                  2: self.insert_action}
                self.action = int(input())
                action_numbers[self.action]()
            except Exception as e:
                print("Please write correct value ", e)
                continue

    def is_correct_parameters(self, parameters):
        current_used_fields = []
        size = len(self.tables_columns[self.current_table])
        for parameter in parameters:
            field_number = int(parameter[0])
            if int(field_number) not in range(-1, size) and len(parameter) != 3:
                return False
            else:
                for field in current_used_fields:
                    if field_number == field:
                        return False
                current_used_fields.append(field_number)
        return True

    def insert_action(self):
        print("Please write value  which you want to insert into table {table}. "
              "( format must be 1=value 2=value etc )".format(table=self.current_table))
        self.print_columns_titles()
        insert_parameters = []
        while True:
            string = input()
            result = string.split()
            is_error_data = False
            try:
                if self.is_correct_parameters(result):
                    for column in result:
                        insert_parameters.append([self.tables_columns[self.current_table][int(column[0])], column[2]])
                else:
                    is_error_data = True
                    print("Incorrect value")
            except:
                is_error_data = True
                print("Incorrect value")
            if not is_error_data:
                break
        status, resutl = self.model.insert_callback(self.current_table, )

    def select_action(self):
        print("Please write value by which you want to select from table {table}. "
              "( format must be 1=value 2=value etc )"
              "\nPress Enter for select without parameters".format(table=self.current_table))
        self.print_columns_titles()
        select_parametrs = []
        while True:
            string = input()
            result = string.split()
            is_error_data = False
            try:
                if self.is_correct_parameters(result):
                    for column in result:
                        select_parametrs.append([self.tables_columns[self.current_table][int(column[0])], column[2]])
                else:
                    is_error_data = True
                    print("Incorrect value")
            except:
                is_error_data = True
                print("Incorrect value")
            if not is_error_data:
                break
        status, result = self.model.select_callback(self.current_table, select_parametrs)
        if status == "Ok":
            self.print_table(result)