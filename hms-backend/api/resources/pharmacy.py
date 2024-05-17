import re
from flask_restful import Resource,reqparse, marshal, fields
from resources.errors import PharmacyNotFoundError
from common.db import *
pharmacy_fields = {
	'id':fields.Integer,
	'name':fields.String,
	'org_id':fields.Integer,
	'properties':fields.String,
	'order_price':fields.Float,
	'sell_price':fields.Float,
	'amount':fields.Float,
	'expire_date':fields.String,
	'status':fields.Integer,
	'created_at':fields.Integer,
	'updated_at':fields.Integer,

	}
def pharmacy_request_parser():
	input_parser = reqparse.RequestParser()
	input_parser.add_argument('name', type=str, required=True, location='json')
	input_parser.add_argument('org_id', type=int, required=False, location='json')
	input_parser.add_argument('properties', type=str, required=False, location='json')
	input_parser.add_argument('order_price', type=float, required=False, location='json')
	input_parser.add_argument('sell_price', type=float, required=False, location='json')
	input_parser.add_argument('amount', type=float, required=False, location='json')
	input_parser.add_argument('expire_date', type=str, required=False, location='json')
	input_parser.add_argument('status', type=int, required=False, location='json')
	input_parser.add_argument('created_at', type=int, required=False, location='json')
	input_parser.add_argument('updated_at', type=int, required=False, location='json')
	return input_parser

def pharmacy_args_parser(args):
	pharmacy_updates = {}
	for k, v in args.items():
		pharmacy_updates[k] = v
	return pharmacy_updates

class Pharmacy(Resource):
	def __init__(self):
		self.reqparse = pharmacy_request_parser()
		super(Pharmacy, self).__init__()

	# @requires_auth
	def get(self, id):
		connect_cursor = get_connect_cursor()
		sql = f'select * from pharmacy where id = {id}'
		pharmacy  = select_sql(connect_cursor[1], sql)
		close_connect_cursor(connect_cursor)
		if  pharmacy is None:
			raise  PharmacyNotFoundError()
		return {'pharmacy': marshal( pharmacy, pharmacy_fields)}

	def put(self, id):
		try:
			connect_cursor = get_connect_cursor()
			sql = f'select * from pharmacy where id = {id}'
			pharmacy = select_sql(connect_cursor[1], sql)
			if not pharmacy:
				raise PharmacyNotFoundError()
			args = self.reqparse.parse_args()
			pharmacy_insert = pharmacy_args_parser(args)

			pre_sql = ""
			for k, v in pharmacy_insert.items():
				if v not in ["", None]:
					if isinstance(v, int):
						pre_sql += f"{k}={v}, "
					else:
						pre_sql += f"{k}='{v}', "
			sql = f"UPDATE pharmacy SET {pre_sql}updated_at = unix_timestamp() WHERE id={id}"
			r = update_sql(connect_cursor[1], sql)
			close_connect_cursor(connect_cursor)
			if r:
				return {'status':'SUCCESS'}, 200
			else:
				return {"status":"ERROR"}, 404
		except Exception as e:
			return {"status":"ERROR", "msg": f"{e}"}, 500

	# @requires_auth
	def delete(self, id):
		try:
			connect_cursor = get_connect_cursor()
			sql = f'select * from pharmacy where id = {id}'
			pharmacy = select_sql(connect_cursor[1], sql)
			if not pharmacy:
				raise PharmacyNotFoundError()
			sql = f'update pharmacyset status = 0, updated_at = unix_timestamp() where id = {id}'
			r = update_sql(connect_cursor[1], sql)
			close_connect_cursor(connect_cursor)
			if r:
				return {'status':'SUCCESS'}, 200
			else:
				return {"status":"ERROR"}, 404
		except Exception as e:
			return {"status":"ERROR", "msg": f"{e}"},500

class PharmacyList(Resource):
	def __init__(self):
		self.reqparse = pharmacy_request_parser()
		super(PharmacyList, self).__init__()

	# @requires_auth
	def get(self):
		connect_cursor = get_connect_cursor()
		sql = 'select * from pharmacy'
		pharmacys = select_sql(connect_cursor[1], sql)
		close_connect_cursor(connect_cursor)
		if  pharmacys is None:
			raise  PharmacyNotFoundError()
		all_pharmacys = [marshal(pharmacy, pharmacy_fields) for pharmacy in pharmacys]
		active_pharmacys  = [pharmacy_dict for pharmacy_dict in all_pharmacys if pharmacy_dict['status'] != False]
		return {'pharmacy': marshal( active_pharmacys, pharmacy_fields)}

	def post(self):
		try:
			args = self.reqparse.parse_args()
			pharmacy_insert = pharmacy_args_parser(args)
			connect_cursor = get_connect_cursor()

			keys = ""
			values = ""
			for k, v in pharmacy_insert.items():
				if v not in ["", None]:
					if isinstance(v, int):
						keys += f"{k}, "
						values += f"{v}, "
					else:
						keys += f"{k}, "
						values += f"'{v}', "
			sql = f'INSERT INTO pharmacy({keys}created_at, updated_at) VALUES ({values}unix_timestamp(), unix_timestamp())'
			r = insert_sql(connect_cursor[1], sql)
			close_connect_cursor(connect_cursor)
			if r:
				return {'status':'SUCCESS', "data":pharmacy_insert}, 200
			else:
				return {"status":"ERROR"}, 404
		except Exception as e:
			return {"status":"ERROR", "msg": f"{e}"},500


## This api added by Mule on 2022-08-27
class PharmacyListPetient(Resource):
	def __init__(self):
		self.reqparse = pharmacy_request_parser()
		super(PharmacyListPetient, self).__init__()

	# @requires_auth
	def get(self, name):
		connect_cursor = get_connect_cursor()
		sql = f'select * from pharmacy where name like "%{name}%"'
		
		pharmacys = select_sql(connect_cursor[1], sql)
		
		close_connect_cursor(connect_cursor)
		if  pharmacys is None:
			raise  PharmacyNotFoundError()
		all_pharmacys = [marshal(pharmacy, pharmacy_fields) for pharmacy in pharmacys]
		active_pharmacys  = [pharmacy_dict for pharmacy_dict in all_pharmacys if pharmacy_dict['status'] != False]
		return {'pharmacy_order': marshal( active_pharmacys, pharmacy_fields)}

	
