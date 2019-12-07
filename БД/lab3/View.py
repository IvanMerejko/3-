

class View(object):

    @staticmethod
    def tables_menu():
        print("Select table")
        print("1 - Assortment")
        print("2 - Commodity")
        print("3 - Customer")
        print("4 - Order")
        print("5 - Shop")
        print("6 - Worker")

    @staticmethod
    def action_menu():
        print("Select action")
        print("1 - Select")
        print("2 - Insert")
        print("3 - Delete")
        print("4 - Update")
        print("5 - Select from all tables")
        print("6 - Generate random data")
        print("7 - Special select by word")

    @staticmethod
    def print_assortment(parameters):
        print("assortment_id | commodity_id | shop_id")
        try:
            result = parameters.split('\n')
            for column in result:
                column = column[1:len(column) - 1]
                assortment_id, commodity_id, shop_id = column.split(", ")
                print("\t\t", assortment_id, "\t  |\t\t", commodity_id, "\t\t |\t", shop_id)
        except:
            print("")

    @staticmethod
    def print_commodity(parameters):
        print("commodity_id | name | price")
        try:
            result = parameters.split('\n')
            for column in result:
                column = column[1:len(column) - 1]
                commodity_id, name, price = column.split(", ")
                print("\t\t", commodity_id, "\t  |\t\t", name, "\t\t |\t", price)
        except:
            print("")

    @staticmethod
    def print_customer(parameters):
        print("customer_id | raiting | worker_id | name")
        try:
            result = parameters.split('\n')
            for column in result:
                column = column[1:len(column) - 1]
                customer_id, raiting, worker_id, name = column.split(", ")
                print("\t\t", customer_id, "\t  |\t\t", raiting, "\t\t |\t", worker_id, "\t  |\t\t", name)
        except:
            print("")

    @staticmethod
    def print_order(parameters):
        print("order_id | customer_id | assortment_id")
        try:
            result = parameters.split('\n')
            for column in result:
                column = column[1:len(column) - 1]
                order_id, customer_id, assortment_id = column.split(", ")
                print("\t\t", order_id, "\t  |\t\t", customer_id, "\t\t |\t", assortment_id)
        except:
            print("")

    @staticmethod
    def print_shop(parameters):
        print("shop_id | monthly_profit | address")
        try:
            result = parameters.split('\n')
            for column in result:
                column = column[1:len(column) - 1]
                shop_id, monthly_profit, address = column.split(", ")
                print("\t\t", shop_id, "\t  |\t\t", monthly_profit, "\t\t |\t", address)
        except:
            print("")

    @staticmethod
    def print_worker(parameters):
        print("worker_id | shop_id | name | surname | position")
        try:
            result = parameters.split('\n')
            for column in result:
                column = column[1:len(column) - 1]
                worker_id, shop_id, name, surname, position = column.split(", ")
                print("\t\t", worker_id, "\t  |\t\t", shop_id, "\t\t |\t", name, "\t\t |\t", surname, "\t\t |\t",position)
        except:
            print("")