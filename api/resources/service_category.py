import re
from flask_restful import Resource,reqparse, marshal, fields
from resources.errors import Service_categoryNotFoundError
from flask import request
from common.db import *

service_category_fields = {
	'office_id':fields.Integer,
	'cat_name':fields.String,
	'cat_description':fields.String,
	'status':fields.Integer,
	'created_at':fields.Integer,
	'updated_at':fields.Integer,

	}

def service_category_request_parser():
	input_parser = reqparse.RequestParser()
	input_parser.add_argument('office_id', type=int, required=False, location='json')
	input_parser.add_argument('cat_name', type=str, required=False, location='json')
	input_parser.add_argument('cat_description', type=str, required=False, location='json')
	input_parser.add_argument('status', type=int, required=False, location='json')
	input_parser.add_argument('created_at', type=int, required=False, location='json')
	input_parser.add_argument('updated_at', type=int, required=False, location='json')
	return input_parser

def service_category_args_parser(args):
	service_category_updates = {}
	for k, v in args.items():
		service_category_updates[k] = v
	return service_category_updates

class Service_category(Resource):
	def __init__(self):
		self.reqparse = service_category_request_parser()
		super(Service_category, self).__init__()

	# @requires_auth
	def get(self, id):
		connect_cursor = get_connect_cursor()
		sql = f'select * from service_category where id = {id}'
		service_category  = select_sql(connect_cursor[1], sql)
		close_connect_cursor(connect_cursor)
		if  service_category is None:
			raise  Service_categoryNotFoundError()
		return {'service_category': marshal( service_category, service_category_fields)}

	def put(self, id):
		try:
			connect_cursor = get_connect_cursor()
			sql = f'select * from service_category where id = {id}'
			service_category = select_sql(connect_cursor[1], sql)
			if not service_category:
				raise Service_categoryNotFoundError()
			args = self.reqparse.parse_args()
			service_category_insert = service_category_args_parser(args)

			pre_sql = ""
			for k, v in service_category_insert.items():
				if v not in ["", None]:
					if isinstance(v, int):
						pre_sql += f"{k}={v}, "
					else:
						pre_sql += f"{k}='{v}', "
			sql = f"UPDATE service_category SET {pre_sql}updated_at = unix_timestamp() WHERE id={id}"
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
			sql = f'select * from service_category where id = {id}'
			service_category = select_sql(connect_cursor[1], sql)
			if not service_category:
				raise Service_categoryNotFoundError()
			sql = f'update service_category set status = 0, updated_at = unix_timestamp() where id = {id}'
			r = update_sql(connect_cursor[1], sql)
			close_connect_cursor(connect_cursor)
			if r:
				return {'status':'SUCCESS'}, 200
			else:
				return {"status":"ERROR"}, 404
		except Exception as e:
			return {"status":"ERROR", "msg": f"{e}"}, 500

class Service_categoryList(Resource):
	def __init__(self):
		self.reqparse = service_category_request_parser()
		super(Service_categoryList, self).__init__()

	# @requires_auth
	def get(self):
		connect_cursor = get_connect_cursor()
		sql = 'select * from service_category'
		service_categorys = select_sql(connect_cursor[1], sql)
		close_connect_cursor(connect_cursor)
		if  service_categorys is None:
			raise  Service_categoryNotFoundError()
		all_service_categorys = [marshal(service_category, service_category_fields) for service_category in service_categorys]
		active_service_categorys  = [service_category_dict for service_category_dict in all_service_categorys if service_category_dict['status'] != False]
		return {'service_category': marshal( active_service_categorys, service_category_fields)}

	def post(self):
		try:
			args = self.reqparse.parse_args()
			service_category_insert = service_category_args_parser(args)
			connect_cursor = get_connect_cursor()

			keys = ""
			values = ""
			for k, v in service_category_insert.items():
				if v not in ["", None]:
					if isinstance(v, int):
						keys += f"{k}, "
						values += f"{v}, "
					else:
						keys += f"{k}, "
						values += f"'{v}', "
			sql = f'INSERT INTO service_category ({keys}created_at, updated_at) VALUES ({values}unix_timestamp(), unix_timestamp())'
			r = insert_sql(connect_cursor[1], sql)
			close_connect_cursor(connect_cursor)
			if r:
				return {'status':'SUCCESS', "data":service_category_insert}, 200
			else:
				return {"status":"ERROR"}, 404
		except Exception as e:
			return {"status":"ERROR", "msg": f"{e}"}, 500

