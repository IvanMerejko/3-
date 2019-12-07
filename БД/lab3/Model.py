from Controller import  Assortment_str, Commodity_str, Customer_str, Order_str, Shop_str, Worker_str
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from DB_tables import *

class Model:

    tables_map = {Assortment_str: Assortment,
                  Commodity_str: Commodity_str,
                  Customer_str: Customer,
                  Order_str: Order,
                  Shop_str: Shop,
                  Worker_str: Worker}

    def __init__(self):
        engine = create_engine("postgresql://postgres:bdfy45231@localhost:1111/test")
        session_class = sessionmaker(bind=engine)
        self.session = session_class()

    def insert_callback(self, current_table, values, columns_name):
        table_object = self.tables_map[current_table]
        try:
            db_object = table_object.create()
            for i in range(0, len(values)):
                setattr(db_object, columns_name[i], values[i])
            self.session.add(db_object)
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            print(e)
        return '', ''

    def select_callback(self, current_table, fields_value):
        table_object = self.tables_map[current_table]
        query = self.session.query(table_object)
        if len(fields_value) != 0:
            for field_name, fields_value in fields_value:
                query = query.filter(get_column_object(table_object, field_name)==fields_value)
        for element in query.all():
            print(element.get_item())
        return "",  ""

    def update_callback(self, current_table, primary_key, new_fields):
        try:
            table_object = self.tables_map[current_table]
            query = self.session.query(table_object)
            query = query.filter(get_column_object(table_object, primary_key[0]) == primary_key[1])
            d_ = dict()
            for column, newValue in new_fields:
                d_[column] = newValue
            print(d_)
            query.update(d_)

        except Exception as e:
            self.session.rollback()
            print(e)
        return "", ""

    def delete_callback(self, current_table, fields):
        table_object = self.tables_map[current_table]
        query = self.session.query(table_object)
        for field_name, fields_value in fields:
            query = query.filter(get_column_object(table_object, field_name) == fields_value)
        try:
            for obj in query.all():
                self.session.delete(obj)
                self.session.commit()
        except Exception as e:
            self.session.rollback()
            print(e)

        return '', ''

