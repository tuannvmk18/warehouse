from sqlmodel import Session, select
from warehouse import engine
from warehouse.models import Product, Supplier
from warehouse.ultis import update_attr


def get_all():
    with Session(engine) as session:
        statement = select(Product, Supplier).join(Supplier, isouter=True)
        results = session.exec(statement)
        return results.fetchall()


def get_by_id(product_id: int):
    with Session(engine) as session:
        statement = select(Product, Supplier).join(Supplier, isouter=True).where(Product.id == product_id)
        product = session.exec(statement).one_or_none()
        return product


def create(product: Product):
    with Session(engine) as session:
        session.add(product)
        session.commit()
        session.refresh(product)
        return product


def delete(product_id: int):
    with Session(engine) as session:
        statement = select(Product).where(Product.id == product_id)
        product = session.exec(statement).one_or_none()
        if product is not None:
            session.delete(product)
            session.commit()
            return True
        return False


def update(product_id: int, payload: Product):
    with Session(engine) as session:
        statement = select(Product).where(Product.id == product_id)
        product = session.exec(statement).one_or_none()
        if product is not None:
            update_attr(product, payload)
            session.add(product)
            session.commit()
            session.refresh(product)
            return product
        return None


def get_without_supplier(product_id: int):
    with Session(engine) as session:
        statement = select(Product).where(Product.id == product_id)
        product = session.exec(statement).one_or_none()
        return product
