from sqlmodel import Session, select
from warehouse import engine
from warehouse.models import Supplier
from warehouse.ultis import update_attr


def get_all():
    with Session(engine) as session:
        statement = select(Supplier)
        results = session.exec(statement)
        return results.fetchall()


def get_by_id(supplier_id: int):
    with Session(engine) as session:
        statement = select(Supplier).where(Supplier.id == supplier_id)
        supplier = session.exec(statement).one_or_none()
        return supplier


def create(supplier: Supplier):
    with Session(engine) as session:
        session.add(supplier)
        session.commit()
        session.refresh(supplier)
        return supplier


def delete(supplier_id: Supplier):
    with Session(engine) as session:
        statement = select(Supplier).where(Supplier.id == supplier_id)
        supplier = session.exec(statement).one_or_none()
        if supplier is not None:
            session.delete(supplier)
            session.commit()
            return True
        return False


def update(supplier_id: int, payload: Supplier):
    with Session(engine) as session:
        statement = select(Supplier).where(Supplier.id == supplier_id)
        supplier = session.exec(statement).one_or_none()
        if supplier_id is not None:
            update_attr(supplier, payload)
            print(supplier)
            session.add(supplier)
            session.commit()
            session.refresh(supplier)
            return supplier
        return None
