

class View(object):

    @staticmethod
    def tables_menu():
        print("Select Table")
        print("1 - Assortment")
        print("2 - Commodity")
        print("3 - Customer")
        print("4 - Order")
        print("5 - Shop")
        print("6 - Worker")

    @staticmethod
    def action_menu():
        print("1 - Select")
        print("2 - Insert")
        print("3 - Delete")
        print("4 - Update")

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
