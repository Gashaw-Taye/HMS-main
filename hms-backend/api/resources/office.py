import re
from flask_restful import Resource,reqparse, marshal, fields
from resources.errors import OfficeNotFoundError
from common.db import *

office_fields = {
	'id':fields.Integer,
	'off_name':fields.String,
	'main_branch':fields.Integer,
	'off_description':fields.String,
	'status':fields.Integer,
	'created_at':fields.Integer,
	'updated_at':fields.Integer,
}

def office_request_parser():
	input_parser = reqparse.RequestParser()
	input_parser.add_argument('off_name', type=str, required=False, location='json')
	input_parser.add_argument('main_branch', type=int, required=False, location='json')
	input_parser.add_argument('off_description', type=str, required=False, location='json')
	input_parser.add_argument('status', type=int, required=False, location='json')
	input_parser.add_argument('created_at', type=int, required=False, location='json')
	input_parser.add_argument('updated_at', type=int, required=False, location='json')
	return input_parser

def office_args_parser(args):
	office_updates = {}
	for k, v in args.items():
		office_updates[k] = v
	return office_updates

class Office(Resource):
	def __init__(self):
		self.reqparse = office_request_parser()
		super(Office, self).__init__()

	# @requires_auth
	def get(self, id):
		connect_cursor = get_connect_cursor()
		sql = f'select * from office where id = {id}'
		office  = select_sql(connect_cursor[1], sql)
		close_connect_cursor(connect_cursor)
		if  office is None:
			raise  OfficeNotFoundError()
		return {'office': marshal( office, office_fields)}

	def put(self, id):
		try:
			connect_cursor = get_connect_cursor()
			sql = f'select * from office where id = {id}'
			office = select_sql(connect_cursor[1], sql)
			if not office:
				raise OfficeNotFoundError()
			args = self.reqparse.parse_args()
			office_insert = office_args_parser(args)
			pre_sql = ""
			for k, v in office_insert.items():
				if v not in ["", None]:
					if isinstance(v, int):
						pre_sql += f"{k}={v}, "
					else:
						pre_sql += f"{k}='{v}', "
			sql = f"UPDATE office SET {pre_sql}updated_at = unix_timestamp() WHERE id={id}"
			r = update_sql(connect_cursor[1], sql)
			close_connect_cursor(connect_cursor)
			if r:
				return {'status':'SUCCESS'}, 200
			else:
				return {"status":"ERROR"}, 404
		except Exception as e:
			return {"status":"ERROR", "msg": f"{e}"},500

	# @requires_auth
	def delete(self, id):
		try:
			connect_cursor = get_connect_cursor()
			sql = f'select * from office where id = {id}'
			c1 = format_number(id)
			office = select_sql(connect_cursor[1], sql)
			if not office:
				raise OfficeNotFoundError()
			sql = f'update office set status = 0, updated_at = unix_timestamp() where id = {id}'
			r = update_sql(connect_cursor[1], sql)
			close_connect_cursor(connect_cursor)
			if r:
				return {'status':'SUCCESS'}, 200
			else:
				return {"status":"ERROR"}, 404
		except Exception as e:
			return {"status":"ERROR", "msg": f"{e}"}, 500

class OfficeList(Resource):
	def __init__(self):
		self.reqparse = office_request_parser()
		super(OfficeList, self).__init__()

	# @requires_auth
	def get(self):
		connect_cursor = get_connect_cursor()
		sql = 'select * from office'
		offices = select_sql(connect_cursor[1], sql)
		close_connect_cursor(connect_cursor)
		if  offices is None:
			raise  OfficeNotFoundError()
		all_offices = [marshal(office, office_fields) for office in offices]
		active_offices  = [office_dict for office_dict in all_offices if office_dict['status'] != False]
		return {'office': marshal( active_offices, office_fields)}

	def post(self):
		try:
			args = self.reqparse.parse_args()
			office_insert = office_args_parser(args)
			connect_cursor = get_connect_cursor()
			keys = ""
			values = ""
			for k, v in office_insert.items():
				if v not in ["", None]:
					if isinstance(v, int):
						keys += f"{k}, "
						values += f"{v}, "
					else:
						keys += f"{k}, "
						values += f"'{v}', "
			sql = f'INSERT INTO office({keys}created_at, updated_at) VALUES ({values}unix_timestamp(), unix_timestamp())'
			r = insert_sql(connect_cursor[1], sql)
			close_connect_cursor(connect_cursor)
			if r:
				return {'status':'SUCCESS', "data":office_insert}, 200
			else:
				return {"status":"ERROR"}, 404
		except Exception as e:
			return {"status":"ERROR", "msg": f"{e}"}, 500

