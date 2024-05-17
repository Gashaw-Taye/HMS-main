import re
from flask_restful import Resource,reqparse, marshal, fields
from resources.errors import Role_usersNotFoundError
from flask import request
from datetime import datetime
import copy
import shortuuid
import os
from common.db import *

role_users_fields = {
	'id':fields.Integer,
	'role_id':fields.Integer,
	'user_id':fields.Integer,
	'status':fields.Integer,
	'created_at':fields.Integer,
	'updated_at':fields.Integer,

	}

def role_users_request_parser():
	input_parser = reqparse.RequestParser()
	input_parser.add_argument('role_id', type=int, required=False, location='json')
	input_parser.add_argument('user_id', type=int, required=False, location='json')
	input_parser.add_argument('status', type=int, required=False, location='json')
	input_parser.add_argument('created_at', type=int, required=False, location='json')
	input_parser.add_argument('updated_at', type=int, required=False, location='json')
	return input_parser

def role_users_args_parser(args):
	role_users_updates = {}
	for k, v in args.items():
		role_users_updates[k] = v
	return role_users_updates

class Role_users(Resource):
	def __init__(self):
		self.reqparse = role_users_request_parser()
		super(Role_users, self).__init__()

	# @requires_auth
	def get(self, id):
		connect_cursor = get_connect_cursor()
		sql = 'select * from role_users where id = %s'
		c1 = format_number(id)
		role_users  = select_sql(connect_cursor[1], sql % c1)
		close_connect_cursor(connect_cursor)
		if  role_users is None:
			raise  Role_usersNotFoundError()
		return {' role_users': marshal( role_users, role_users_fields)}

	def put(self, id):
		try:
			connect_cursor = get_connect_cursor()
			sql = f'SELECT * FROM role_users WHERE id = {id}'
			role_users = select_sql(connect_cursor[1], sql)
			if not role_users:
				raise Role_usersNotFoundError()
			args = self.reqparse.parse_args()
			role_users_insert = role_users_args_parser(args)

			pre_sql = ""
			for k, v in role_users_insert.items():
				if v not in ["", None]:
					if isinstance(v, int):
						pre_sql += f"{k}={v}, "
					else:
						pre_sql += f"{k}='{v}', "
			sql = f"UPDATE role_users SET {pre_sql}updated_at = unix_timestamp() WHERE id={id}"
			r = update_sql(connect_cursor[1], sql)
			close_connect_cursor(connect_cursor)
			if r:
				return {'status':'SUCCESS'}, 200
			else:
				return {"status":"ERROR"}, 404
		except Exception as e:
			return {"status":"ERROR", "Detail":str(e)}, 500

	# @requires_auth
	def delete(self, id):
		try:
			connect_cursor = get_connect_cursor()
			sql = f'select * from role_users where id = {id} and status > 0'
			role_users = select_sql(connect_cursor[1], sql)
			if not role_users:
				raise Role_usersNotFoundError()
			sql = f'update role_usersset status = 0, updated_at = unix_timestamp() where id = {id}'
			r = update_sql(connect_cursor[1], sql)
			close_connect_cursor(connect_cursor)
			if r:
				return {'status':'SUCCESS'}, 200
			else:
				return {"status":"ERROR"}, 404
		except Exception as e:
			return {"status":"ERROR", "msg": f"{e}"}, 500

class Role_usersList(Resource):
	def __init__(self):
		self.reqparse = role_users_request_parser()
		super(Role_usersList, self).__init__()

	# @requires_auth
	def get(self):
		connect_cursor = get_connect_cursor()
		sql = 'select * from role_users'
		role_userss = select_sql(connect_cursor[1], sql)
		close_connect_cursor(connect_cursor)
		if  role_userss is None:
			raise  Role_usersNotFoundError()
		all_role_userss = [marshal(role_users, role_users_fields) for role_users in role_userss]
		active_role_userss  = [role_users_dict for role_users_dict in all_role_userss if role_users_dict['status'] != False]
		return {' role_users': marshal( active_role_userss, role_users_fields)}

	def post(self):
		try:
			args = self.reqparse.parse_args()
			role_users_insert = role_users_args_parser(args)
			connect_cursor = get_connect_cursor()

			keys = ""
			values = ""
			for k, v in role_users_insert.items():
				if v not in ["", None]:
					if isinstance(v, int):
						keys += f"{k}, "
						values += f"{v}, "
					else:
						keys += f"{k}, "
						values += f"'{v}', "
			sql = f'INSERT INTO role_users ({keys}created_at, updated_at) VALUES ({values}unix_timestamp(), unix_timestamp())'
			# return sql
			r = insert_sql(connect_cursor[1], sql)
			close_connect_cursor(connect_cursor)
			if r:
				return {'status':'SUCCESS', "data":role_users_insert}, 200
			else:
				return {"status":"ERROR"}, 404
		except Exception as e:
			return {"status":"ERROR", "Detail":str(e)}

