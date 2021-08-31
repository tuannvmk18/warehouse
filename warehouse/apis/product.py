import json
import traceback

from flask_restx import Namespace, Resource, fields
from warehouse.services import product as product_service
from warehouse.models import Product
from warehouse.ultis import update_attr

api = Namespace('product', description='product api')

product_schema = api.model('Product', {
    'id': fields.Integer,
    'name': fields.String,
    'price': fields.Float,
    'description': fields.String,
    'supplier_id': fields.Integer
})

product_update_schema = api.model('Product Update', {
    'name': fields.String,
    'price': fields.Float,
    'description': fields.String,
    'supplier_id': fields.Integer
})

product_create_schema = api.model('Product Update', {
    'name': fields.String,
    'price': fields.Float,
    'description': fields.String,
    'supplier_id': fields.Integer
})


@api.route("/")
class ProductRouterWithNoParam(Resource):
    def get(self):
        try:
            results = product_service.get_all()
            response = {"data": []}
            for product, supplier in results:
                supplier_json = None
                product_json = json.loads(product.json())
                if supplier is not None:
                    supplier_json = json.loads(supplier.json())
                product_json.pop("supplier_id", None)
                product_json["supplier"] = supplier_json
                response["data"].append(product_json)
            return response
        except:
            return {'message': 'Something error'}, 404

    @api.doc(body=product_create_schema)
    def post(self):
        try:
            payload = api.payload
            p = Product()
            update_attr(p, payload)
            product = product_service.create(p)
            if product is not None:
                return json.loads(product.json())
        except Exception:
            traceback.print_exc()
            return {'message': 'Something error'}, 404


@api.route("/<int:id>")
class ProductRouterWithID(Resource):
    def get(self, id: int):
        try:
            response = {}
            result = product_service.get_by_id(id)
            response["data"] = json.loads(result[0].json())
            response["data"]["supplier"] = json.loads(result[1].json())

            response["data"].pop("supplier_id", None)
            return response
        except:
            return {'message': 'Something error'}, 404

    @api.doc(body=product_update_schema)
    def put(self, id: int):
        response = product_service.update(id, api.payload)
        if response is None:
            return {'message': 'Something error'}, 404
        return json.loads(response.json())

    def delete(self, id: int):
        try:
            if product_service.delete(id):
                return {'message': 'Success'}
            else:
                raise Exception
        except:
            return {'message': 'Error'}
