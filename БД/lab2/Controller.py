
import random, string


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

    tables_columns = {Assortment_str: ["assortment_id", "commodity_id", "shop_id"],
                      Commodity_str: ["commodity_id", "name", "price"],
                      Customer_str: ["customer_id", "name", "raiting", "worker_id"],
                      Order_str: ["order_id", "customer_id", "assortment_id"],
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
                                 self.Customer_str:   self.view.print_customer,
                                 self.Order_str: self.view.print_order,
                                 self.Shop_str: self.view.print_shop,
                                 self.Worker_str: self.view.print_worker}
        tables_print_function[self.current_table](parameters)

    def print_columns_titles(self, is_need_primary_key):
        columns = self.tables_columns[self.current_table]
        start_i = (0 if is_need_primary_key else 1)
        size = len(columns)
        for i in range(start_i, size):
            print("{number} for {column}".format(number=i, column=columns[i]))

    def start(self):
        while True:
            self.view.tables_menu()
            try:
                table = int(input())
                self.current_table = self.tables_number[table]
                self.view.action_menu()
                action_numbers = {1: self.select_action,
                                  2: self.insert_action,
                                  3: self.delete_action,
                                  4: self.update_action,
                                  5: self.big_tables_select,
                                  6: self.generate_random_values}
                self.action = int(input())
                action_numbers[self.action]()
            except Exception as e:
                print("Please write correct value ", e)
                continue

    def big_tables_select(self):
        print("Set values between which you want to select data(format int1 int2)")
        while True:
            try:
                values = input()
                values = values.split(' ')
                status, result = self.model.select_from_all_tables(int(values[0]), int(values[1]))
                print(status, result)
                break

            except:
                print('Incorrect format')

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

    def delete_action(self):
        print("Please write values by which you want to delete from table {table}. "
              "( format must be 1=value|2=value etc )".format(table=self.current_table))
        self.print_columns_titles(True)
        delete_parameters = []
        while True:
            string = input()
            result = string.split('|')
            is_error_data = False
            try:
                if self.is_correct_parameters(result):
                    for column in result:
                        insert_list = column.split('=')
                        delete_parameters.append([self.tables_columns[self.current_table][int(insert_list[0])],
                                                 insert_list[1]])
                else:
                    is_error_data = True
                    print("Incorrect value")
                status, result_db = self.model.delete_callback(self.current_table,
                                                               delete_parameters)
                print(status)
                if status == 'Ok':
                    break
            except:
                is_error_data = True
                print("Incorrect value")
            if not is_error_data:
                break

    def insert_action(self):
        print("Please write value which you want to insert into table {table}. "
              "( format must be 1=value|2=value etc ). Input order must be followed".format(table=self.current_table))
        self.print_columns_titles(False)
        insert_parameters = []
        while True:
            string = input()
            result = string.split('|')
            is_error_data = False
            try:
                if self.is_correct_parameters(result):
                    for column in result:
                        insert_list = column.split('=')
                        insert_parameters.append(insert_list[1])
                else:
                    is_error_data = True
                    print("Incorrect value")
                status, result_db = self.model.insert_callback(self.current_table,
                                                               insert_parameters,
                                                               self.tables_columns[self.current_table])
                print(status)
                if status == 'Ok':
                    break
            except:
                is_error_data = True
                print("Incorrect value")
            if not is_error_data:
                break

    def select_action(self):
        print("Please write value by which you want to select from table {table}. "
              "( format must be 1=value 2=value etc )"
              "\nPress Enter for select without parameters".format(table=self.current_table))
        self.print_columns_titles(True)
        select_parameters = []
        while True:
            string = input()
            result = string.split()
            is_error_data = False
            try:
                if self.is_correct_parameters(result):
                    for column in result:
                        insert_list = column.split('=')
                        select_parameters.append([self.tables_columns[self.current_table][int(insert_list[0])],
                                                 insert_list[1]])
                else:
                    is_error_data = True
                    print("Incorrect value")
            except:
                is_error_data = True
                print("Incorrect value")
            if not is_error_data:
                break
        status, result = self.model.select_callback(self.current_table, select_parameters)
        if status == "Ok":
            self.print_table(result)

    def update_action(self):
        print("Please write value which you want to update in table {table}. "
              "( format must be 1=value|2=value etc ) "
              "\nFirst parameter must be primary key( number 0 )".format(table=self.current_table))
        self.print_columns_titles(True)
        update_parameters = []
        while True:
            string = input()
            result = string.split('|')
            is_error_data = False
            try:
                if self.is_correct_parameters(result):
                    for column in result:
                        insert_list = column.split('=')
                        update_parameters.append([self.tables_columns[self.current_table][int(insert_list[0])],
                                                  insert_list[1]])
                else:
                    is_error_data = True
                    print("Incorrect value")
                status, result_db = self.model.update_callback(self.current_table,
                                                               update_parameters[0],
                                                               update_parameters[1::])
                print(status)
                if status == 'Ok':
                    break
            except:
                is_error_data = True
                print("Incorrect value")
            if not is_error_data:
                break

    def generate_random_values(self):
        def random_word(length):
           letters = string.ascii_lowercase
           return ''.join(random.choice(letters) for i in range(length))
        def random_int(min, max):
            return random.randint(min, max)
        def random_order():
            return [random_int(1, 1000), random_int(1, 1000)]
        def random_worker():
            return [random_int(1, 1000), random_word(25), random_word(25), random_word(25)]
        def random_shop():
            return [random_int(1000, 10000), random_word(25)]
        def random_commodity():
            return [random_word(25), random_int(1000, 10000)]
        def random_customer():
            return [random_word(25), random_int(1, 1000), random_int(1, 100)]
        def random_assortment():
            return [random_int(1, 1000), random_int(1, 1000)]

        random_data_generator = {self.Assortment_str: random_assortment,
                                 self.Worker_str: random_worker,
                                 self.Shop_str: random_shop,
                                 self.Order_str: random_order,
                                 self.Commodity_str: random_commodity,
                                 self.Customer_str: random_customer}
        for i in range(1, 100):
            self.model.insert_callback(self.current_table,
                                       random_data_generator[self.current_table](),
                                       self.tables_columns[self.current_table])
