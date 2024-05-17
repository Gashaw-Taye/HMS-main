import re
from flask_restful import Resource,reqparse, marshal, fields
from resources.errors import RolesNotFoundError
from flask import request
from common.db import *
from resources.shared import roles_fields

def roles_request_parser():
	input_parser = reqparse.RequestParser()
	input_parser.add_argument('org_id', type=int, required=False, location='json')
	input_parser.add_argument('name', type=str, required=False, location='json')
	input_parser.add_argument('description', type=str, required=False, location='json')
	input_parser.add_argument('status', type=int, required=False, location='json')
	input_parser.add_argument('created_at', type=int, required=False, location='json')
	input_parser.add_argument('updated_at', type=int, required=False, location='json')
	return input_parser

def roles_args_parser(args):
	roles_updates = {}
	for k, v in args.items():
		roles_updates[k] = v
	return roles_updates

class Roles(Resource):
	def __init__(self):
		self.reqparse = roles_request_parser()
		super(Roles, self).__init__()

	# @requires_auth
	def get(self, id):
		connect_cursor = get_connect_cursor()
		sql = 'SELECT * FROM roles where id = %s'
		c1 = format_number(id)
		roles  = select_sql(connect_cursor[1], sql % c1)
		close_connect_cursor(connect_cursor)
		if  roles is None:
			raise  RolesNotFoundError()
		return {'roles': marshal( roles, roles_fields)}

	def put(self, id):
		try:
			connect_cursor = get_connect_cursor()
			sql = 'SELECT * FROM roles where id = %s'
			c1 = format_number(id)
			roles = select_sql(connect_cursor[1], sql % c1)
			if not roles:
				raise RolesNotFoundError()
			args = self.reqparse.parse_args()
			roles_insert = roles_args_parser(args)

			pre_sql = ""
			for k, v in roles_insert.items():
				if v not in ["", None]:
					if isinstance(v, int):
						pre_sql += f"{k}={v}, "
					else:
						pre_sql += f"{k}='{v}', "
			sql = f"UPDATE roles SET {pre_sql}updated_at = unix_timestamp() WHERE id={id}"
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
			sql = f'SELECT * FROM roles where id = {id}'
			roles = select_sql(connect_cursor[1], sql)
			if not roles:
				raise RolesNotFoundError()
			sql = f'update roles set status = 0, updated_at = unix_timestamp() where id = {id}'
			r = update_sql(connect_cursor[1], sql)
			close_connect_cursor(connect_cursor)
			if r:
				return {'status':'SUCCESS'}, 200
			else:
				return {"status":"ERROR"}, 404
		except Exception as e:
			return {"status":"ERROR", "msg": f"{e}"}, 500

class RolesList(Resource):
	def __init__(self):
		self.reqparse = roles_request_parser()
		super(RolesList, self).__init__()

	# @requires_auth
	def get(self):
		connect_cursor = get_connect_cursor()
		sql = 'SELECT * FROM roles'
		roless = select_sql(connect_cursor[1], sql)
		close_connect_cursor(connect_cursor)
		if  roless is None:
			raise  RolesNotFoundError()
		all_roless = [marshal(roles, roles_fields) for roles in roless]
		active_roless  = [roles_dict for roles_dict in all_roless if roles_dict['status'] != False]
		return {'roles': marshal( active_roless, roles_fields)}

	def post(self):
		try:
			args = self.reqparse.parse_args()
			roles_insert = roles_args_parser(args)
			connect_cursor = get_connect_cursor()
			keys = ""
			values = ""
			for k, v in roles_insert.items():
				if v not in ["", None]:
					if isinstance(v, int):
						keys += f"{k}, "
						values += f"{v}, "
					else:
						keys += f"{k}, "
						values += f"'{v}', "
			sql = f'INSERT INTO roles ({keys}created_at, updated_at) VALUES ({values}unix_timestamp(), unix_timestamp())'
			r = insert_sql(connect_cursor[1], sql)
			close_connect_cursor(connect_cursor)
			if r:
				return {'status':'SUCCESS', "data":roles_insert}, 200
			else:
				return {"status":"ERROR"}, 404
		except Exception as e:
			return {"status":"ERROR", "msg": f"{e}"}, 500
