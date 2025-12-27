from sqlalchemy import Column, Date, String, Integer, ForeignKey, Numeric
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Customer(Base):
    __tablename__ = 'customers'
    cd_customer = Column(String(256), primary_key=True)
    nm_customer = Column(String(135))
    st_email = Column(String(135))
    st_phone = Column(String(135))
    sg_state = Column(String(2))
    dt_birth = Column(Date)


class Sale(Base):
    __tablename__ = 'sales'
    cd_sale = Column(Integer, primary_key=True)
    cd_customer = Column(String(256), ForeignKey('customers.cd_customer'))
    dt_purchase_date = Column(Date)
    product_name = Column(String(135))
    num_items = Column(Integer)
    price = Column(Numeric(18, 2))
    shipping_cost = Column(Numeric(18, 2))
    total_value = Column(Numeric(18, 2))