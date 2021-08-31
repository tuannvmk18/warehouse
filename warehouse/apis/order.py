import json
import traceback

from flask_restx import Namespace, Resource, fields
from warehouse.services import order as order_service
from warehouse.services import product as product_service
from warehouse.services import supplier as supplier_service

api = Namespace('order', description='order api')


@api.route('/')
class OderRouterWithoutParam(Resource):
    def get(self):
        try:
            list_o = order_service.get_all()
            r = []
            for result in list_o:
                try:
                    # result = order_service.get_by_id(o[0].id)
                    response = json.loads(result[0].json())
                    response['customer'] = json.loads(result[1].json())
                    response['order_total'] = 0
                    products = []
                    for p in result[2]:
                        product = json.loads(product_service.get_without_supplier(p.product_id).json())
                        if product['supplier_id'] is not None:
                            supplier = json.loads(supplier_service.get_by_id(product['supplier_id']).json())
                            product['supplier'] = supplier
                        product.pop('supplier_id', None)
                        product['quantity'] = p.quantity
                        product['total'] = product['price'] * product['quantity']
                        response['order_total'] += product['total']
                        products.append(product)
                    response.pop('customer_id', None)
                    response['list_product'] = products
                    r.append(response)
                except:
                    return {'message': 'Something error'}, 404
            return r
        except:
            return {'message': 'Something error'}, 404

    def post(self):
        products_temp = api.payload['products']
        products = []
        for i in products_temp:
            p = product_service.get_without_supplier(i['id'])
            if p is None:
                return {"message": "product not available"}
            products.append(p)
        customer_id = api.payload['customer_id']
        o = order_service.create(customer_id, products)
        ot = order_service.do_s(o.id, products_temp)
        return {"order_id": o.id}


@api.route('/<int:id>')
class OderRouterWithID(Resource):
    def get(self, id: int):
        try:
            result = order_service.get_by_id(id)
            response = json.loads(result[0].json())
            response['customer'] = json.loads(result[1].json())
            response['order_total'] = 0
            products = []
            for p in result[2]:
                product = json.loads(product_service.get_without_supplier(p.product_id).json())
                if product['supplier_id'] is not None:
                    supplier = json.loads(supplier_service.get_by_id(product['supplier_id']).json())
                    product['supplier'] = supplier
                product.pop('supplier_id', None)
                product['quantity'] = p.quantity
                product['total'] = product['price'] * product['quantity']
                response['order_total'] += product['total']
                products.append(product)
            response.pop('customer_id', None)
            response['list_product'] = products
            return response
        except:
            return {'message': 'Something error'}, 404

    def delete(self, id: int):
        try:
            if order_service.delete(id):
                return {'message': 'Success'}
            else:
                raise Exception
        except:
            return {'message': 'Error'}
