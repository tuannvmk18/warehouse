from flask import Flask
from flask_restx import Api
from sqlmodel import create_engine, SQLModel
from . import models

api = Api()

postgresql_url = f"postgresql://minhtuan:11111111@localhost:5432/mydb"
engine = create_engine(postgresql_url, echo=True)


def create_app() -> Flask:
    app = Flask(__name__)

    api.init_app(app)

    from .apis.product import api as product_ns
    from .apis.supplier import api as supplier_ns
    from .apis.order import api as order_ns

    api.add_namespace(product_ns)
    api.add_namespace(supplier_ns)
    api.add_namespace(order_ns)

    SQLModel.metadata.create_all(engine)
    return app
