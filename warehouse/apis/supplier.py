import json
import traceback

from flask_restx import Namespace, Resource, fields

from warehouse.models import Supplier
from warehouse.services import supplier as supplier_service
from warehouse.ultis import update_attr

api = Namespace('supplier', description='supplier api')

supplier_schema = api.model('Supplier', {
    'id': fields.Integer,
    'name': fields.String,
    'address': fields.String,
    'phone': fields.String
})

supplier_create_schema = api.model('Supplier Create', {
    'name': fields.String,
    'address': fields.String,
    'phone': fields.String
})

supplier_update_schema = api.model('Supplier Update', {
    'name': fields.String,
    'address': fields.String,
    'phone': fields.String
})


@api.route("/")
class SupplerRouterWithoutParam(Resource):
    def get(self):
        try:
            results = supplier_service.get_all()
            print(results)
            response = [json.loads(obj.json()) for obj in results]
            return response
        except:
            return {'message': 'Something error'}, 404

    @api.doc(body=supplier_create_schema)
    def post(self):
        try:
            payload = api.payload
            p = Supplier()
            update_attr(p, payload)
            product = supplier_service.create(p)
            if product is not None:
                return json.loads(product.json())
        except Exception:
            traceback.print_exc()
            return {'message': 'Something error'}, 404


@api.route("/<int:id>")
class SupplierRouterWithID(Resource):
    def get(self, id: int):
        try:
            supplier = supplier_service.get_by_id(id)
            if supplier is not None:
                return json.loads(supplier.json())
            raise Exception
        except:
            return {'message': 'Something error'}, 404

    @api.doc(body=supplier_update_schema)
    def put(self, id: int):
        response = supplier_service.update(id, api.payload)
        if response is None:
            return {'message': 'Something error'}, 404
        return json.loads(response.json())

    def delete(self, id: int):
        try:
            if supplier_service.delete(id):
                return {'message': 'Success'}
            else:
                raise Exception
        except:
            return {'message': 'Error'}
