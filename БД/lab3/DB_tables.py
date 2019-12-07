from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Shop(Base):
    __tablename__ = 'shop'
    shop_id = Column(Integer, primary_key=True)
    monthly_profit = Column(Integer)
    address = Column(String)

    # def __repr__(self):
    #     return f'List: {self.name}'
    def get_item(self):
        return "{0},{1},{2}".format(self.shop_id,
                                    self.monthly_profit,
                                    self.address)

    def get_column(self, column_name):
        if column_name == "shop_id":
            return self.shop_id
        elif column_name == 'address':
            return self.address
        elif column_name == 'monthly_profit':
            return self.monthly_profit

    @staticmethod
    def create(self):
        return Shop()

class Worker(Base):
    __tablename__ = 'worker'
    worker_id = Column(Integer, primary_key=True)
    shop_id = Column(Integer, ForeignKey('shop.shop_id'))
    name = Column(String)
    surname = Column(String)
    position = Column(String)
    shop = relationship(Shop, backref="shops")

    def get_item(self):
        return "{0},{1},{2},{3},{4}".format(self.worker_id,
                                            self.shop_id,
                                            self.name,
                                            self.surname,
                                            self.position)

    def get_column(self, column_name):
        if column_name == "worker_id":
            return self.worker_id
        elif column_name == 'name':
            return self.name
        elif column_name == 'surname':
            return self.surname
        elif column_name == 'position':
            return self.position

    @staticmethod
    def create(self):
        return Worker()


class Commodity(Base):
    __tablename__ = 'commodity'
    commodity_id = Column(Integer, primary_key=True)
    name = Column(String)
    price = Column(Integer)

    def get_item(self):
        return "{0},{1},{2}".format(self.commodity_id,
                                    self.name,
                                    self.price)

    def get_column(self, column_name):
        if column_name == "commodity_id":
            return self.commodity_id
        elif column_name == 'name':
            return self.name
        elif column_name == 'price':
            return self.price

    @staticmethod
    def create(self):
        return Commodity()


class Customer(Base):
    __tablename__ = 'customer'
    customer_id = Column(Integer, primary_key=True)
    name = Column(String)
    raiting = Column(Integer)
    worker_id = Column(Integer, ForeignKey('worker.worker_id'))
    worker = relationship(Worker, backref="workers")
    def get_item(self):
        return "{0},{1},{2}, {3}".format(self.customer_id,
                                         self.name,
                                         self.raiting,
                                         self.worker_id)

    def get_column(self, column_name):
        if column_name == "customer_id":
            return self.customer_id
        elif column_name == 'name':
            return self.name
        elif column_name == 'raiting':
            return self.raiting
        elif column_name == 'worker_id':
            return self.worker_id

    @staticmethod
    def create(self):
        return Customer()


class Assortment(Base):
    __tablename__ = 'assortment'
    assortment_id = Column(Integer, primary_key=True)
    commodity_id = Column(Integer, ForeignKey('commodity.commodity_id'))
    shop_id = Column(Integer, ForeignKey('shop.shop_id'))
    shop = relationship(Shop, backref="shops_a")
    commodity = relationship(Commodity, backref="commodities")

    def get_item(self):
        return "{0},{1},{2}".format(self.assortment_id,
                                    self.commodity_id,
                                    self.shop_id)

    def get_column(self, column_name):
        if column_name == "assortment_id":
            return self.assortment_id
        elif column_name == 'shop_id':
            return self.shop_id
        elif column_name == 'commodity_id':
            return self.commodity_id

    @staticmethod
    def create():
        return Assortment()


class Order(Base):
    __tablename__ = 'order'
    order_id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey('customer.customer_id'))
    assortment_id = Column(Integer, ForeignKey('assortment.assortment_id'))
    customer = relationship(Customer, backref="customers")
    assortment = relationship(Assortment, backref="assortments")

    def get_item(self):
        return "{0},{1},{2}".format(self.order_id,
                                    self.customer_id,
                                    self.assortment_id)

    def get_column(self, column_name):
        if column_name == "order_id":
            return self.order_id
        elif column_name == 'customer_id':
            return self.customer_id
        elif column_name == 'assortment_id':
            return self.assortment_id

    @staticmethod
    def create(self):
        return Order()


def get_column_object(table_object, name):
    return table_object.get_column(table_object, name)
