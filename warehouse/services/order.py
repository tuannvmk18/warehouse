from datetime import datetime

from sqlmodel import Session, select
from typing import List

from warehouse import engine
from warehouse.models import Order, Product, Customer, OrderDetail
from warehouse.ultis import update_attr


def get_all():
    with Session(engine) as session:
        statement = select(Order, Customer).join(Customer)
        results = session.exec(statement)
        r = []
        for o in results.fetchall():
            statement = select(OrderDetail).where(OrderDetail.order_id == o[0].id)
            order_details = session.exec(statement).fetchall()
            r.append([o[0], o[1], order_details])
        print(r)
        return r


def get_by_id(order_id: int):
    with Session(engine) as session:
        statement = select(Order, Customer).join(Customer).where(Order.id == order_id)
        order = session.exec(statement).one_or_none()
        statement = select(OrderDetail).where(OrderDetail.order_id == order_id)
        order_details = session.exec(statement).fetchall()
        result = [order[0], order[1], order_details]
        return result


def create(customer_id: int, products: List[Product]):
    order = Order()
    order.products = products
    order.customer_id = customer_id
    order.order_date = datetime.now()
    print(order)
    with Session(engine) as session:
        session.add(order)
        session.commit()
        session.refresh(order)
        return order


def do_s(order_id: int, payload):
    with Session(engine) as session:
        for i in payload:
            statement = select(OrderDetail).where(
                OrderDetail.product_id == i['id']).where(OrderDetail.order_id == order_id)
            order = session.exec(statement).one_or_none()
            if order is not None:
                order.quantity = i['quantity']
            session.add(order)
            session.commit()


def delete(order_id):
    with Session(engine) as session:
        statement = select(Order).where(Order.id == order_id)
        order = session.exec(statement).one_or_none()
        session.delete(order)
        session.commit()


def get_by_customer_id(customer_id):
    with Session(engine) as session:
        statement = select(Order).where(Order.customer_id == customer_id)
        results = session.exec(statement).fetchall()
        return results
