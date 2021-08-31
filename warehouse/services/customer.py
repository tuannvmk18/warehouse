from sqlmodel import Session, select
from warehouse import engine
from warehouse.models import Customer
from warehouse.ultis import update_attr


def get_all():
    with Session(engine) as session:
        statement = select(Customer)
        results = session.exec(statement)
        return results.fetchall()


def get_by_id():
    with Session(engine) as session:
        statement = select(Customer)
        result = session.exec(statement)
        return result.one_or_none()


def create(customer: Customer):
    with Session(engine) as session:
        session.add(customer)
        session.commit()
        session.refresh(customer)
        return customer


def delete(customer_id: int):
    with Session(engine) as session:
        statement = select(Customer).where(Customer.id == customer_id)
        customer = session.exec(statement).one_or_none()
        if customer is not None:
            session.delete(customer)
            session.commit()
            return True
        return False


def update(customer_id: int, customer_update):
    with Session(engine) as session:
        statement = select(Customer).where(Customer.id == customer_id)
        old_customer = session.exec(statement)
        update_attr(old_customer, customer_update)
        session.add(old_customer)
        session.commit()
        session.refresh(old_customer)
        return old_customer
