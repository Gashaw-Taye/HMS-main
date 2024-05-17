import re
from flask_restful import Resource,reqparse, marshal, fields
from werkzeug.security import generate_password_hash,check_password_hash
from resources.errors import UsersNotFoundError, EmployeesNotFoundError, UserAlreadyFoundError, UserNameFoundError
from common.util import *
from common.db import *
import jwt
import datetime

from flask_restful import Resource, reqparse
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token
)
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import JWTManager

users_fields = {
	'id':fields.Integer,
	'username':fields.String,
	'password':fields.String,
	'public_id':fields.Integer,
	'token':fields.String,
	'first_login':fields.String,
	'last_login':fields.String,
	'status':fields.Integer,
	'created_at':fields.Integer,
	'updated_at':fields.Integer,
	}

def users_request_parser():
	input_parser = reqparse.RequestParser()
	input_parser.add_argument('id', type=int, required=False, location='json')
	input_parser.add_argument('username', type=str, required=True, location='json')
	input_parser.add_argument('password', type=str, required=True, location='json')
	input_parser.add_argument('public_id', type=int, required=False, location='json')
	input_parser.add_argument('token', type=str, required=False, location='json')
	input_parser.add_argument('first_login', type=str, required=False, location='json')
	input_parser.add_argument('last_login', type=str, required=False, location='json')
	input_parser.add_argument('status', type=int, required=False, location='json')
	input_parser.add_argument('created_at', type=int, required=False, location='json')
	input_parser.add_argument('updated_at', type=int, required=False, location='json')
	return input_parser

def users_args_parser(args):
	users_updates = {}
	for k, v in args.items():
		users_updates[k] = v
	users_updates['password'] = generate_password_hash(args['password'], method='sha256')
	return users_updates

class Users(Resource):
	def __init__(self):
		self.reqparse = users_request_parser()
		super(Users, self).__init__()

	# @requires_auth
	def get(self, id):
		connect_cursor = get_connect_cursor()
		sql = 'select * from users where id = %s'
		c1 = format_number(id)
		users  = select_sql(connect_cursor[1], sql % c1)
		close_connect_cursor(connect_cursor)
		if  users is None:
			raise  UsersNotFoundError()
		return {'users': marshal( users, users_fields)}

	def put(self, id):
		connect_cursor = get_connect_cursor()
		sql = f'SELECT users.*, employees.id FROM users, employees WHERE users.id = {id} and employees.id = {id}'
		users = select_sql(connect_cursor[1], sql)
		if not users:
			raise UsersNotFoundError()
		args = self.reqparse.parse_args()
		users_insert = users_args_parser(args)

		pre_sql = ""
		for k, v in users_insert.items():
			if v not in ["", None]:
				if isinstance(v, int):
					pre_sql += f"{k}={v}, "
				else:
					pre_sql += f"{k}='{v}', "
		sql = f"UPDATE users SET {pre_sql}updated_at = unix_timestamp() WHERE id={id}"
		r = update_sql(connect_cursor[1], sql)
		close_connect_cursor(connect_cursor)
		if r:
			return {'status':'SUCCESS'}, 200
		else:
			return {"status":"ERROR"}, 404

	# @requires_auth
	def delete(self, id):
		connect_cursor = get_connect_cursor()
		sql = f'SELECT users.*, employees.id FROM users, employees WHERE users.id = {id} and employees.id = {id}'
		users = select_sql(connect_cursor[1], sql)
		if not users:
			close_connect_cursor(connect_cursor)
			raise UsersNotFoundError()
		sql = f'update usersset status = 0, updated_at = unix_timestamp() where id = {id}'
		r = update_sql(connect_cursor[1], sql)
		close_connect_cursor(connect_cursor)
		if r:
			return {'status':'SUCCESS'}, 200
		else:
			return {"status":"ERROR"}, 404

	def post(self, id):
		args = self.reqparse.parse_args()
		users_insert = users_args_parser(args)

		# check employee exist
		connect_cursor = get_connect_cursor()
		sql = f'SELECT * from employees WHERE id = {id}'
		employees = select_sql(connect_cursor[1], sql)
		if not employees:
			close_connect_cursor(connect_cursor)
			raise EmployeesNotFoundError()

		# check user already exist in users table
		sql = f'SELECT * from users WHERE id = {id}'
		users = select_sql(connect_cursor[1], sql)
		if users:
			close_connect_cursor(connect_cursor)
			raise UserAlreadyFoundError()
		
		# check username is not taken
		username = users_insert['username']
		sql = f"SELECT * from users WHERE username = '{username}'"
		user_name = select_sql(connect_cursor[1], sql)
		if user_name:
			close_connect_cursor(connect_cursor)
			raise UserNameFoundError()
			
		keys = "id, "
		values = f"{id}, "
		for k, v in users_insert.items():
			if v not in ["", None]:
				if isinstance(v, int):
					keys += f"{k}, "
					values += f"{v}, "
				else:
					keys += f"{k}, "
					values += f"'{v}', "
		sql = f'INSERT INTO users ({keys}created_at, updated_at) VALUES ({values} unix_timestamp(), unix_timestamp())'
		r = insert_sql(connect_cursor[1], sql)
		close_connect_cursor(connect_cursor)
		if r:
			return {'status':'SUCCESS', "data":users_insert}, 201
		else:
			return {"status":"ERROR"}, 404

# class UsersList(Resource):
# 	def __init__(self):
# 		self.reqparse = users_request_parser()
# 		super(UsersList, self).__init__()

# 	# @requires_auth
# 	def get(self):
# 		connect_cursor = get_connect_cursor()
# 		sql = 'select * from users'
# 		userss = select_sql(connect_cursor[1], sql)
# 		close_connect_cursor(connect_cursor)
# 		if  userss is None:
# 			raise  UsersNotFoundError()
# 		all_userss = [marshal(users, users_fields) for users in userss]
# 		active_userss  = [users_dict for users_dict in all_userss if users_dict['status'] != False]
# 		return {'users': marshal( active_userss, users_fields)}

# 	def post(self):
# 		args = self.reqparse.parse_args()
# 		users_insert = users_args_parser(args)
# 		connect_cursor = get_connect_cursor()

# 		keys = ""
# 		values = ""
# 		for k, v in users_insert.items():
# 			if v not in ["", None]:
# 				if isinstance(v, int):
# 					keys += f"{k}, "
# 					values += f"{v}, "
# 				else:
# 					keys += f"{k}, "
# 					values += f"'{v}', "
# 		sql = f'INSERT INTO users ({keys}created_at, updated_at) VALUES ({values}unix_timestamp(), unix_timestamp())'
# 		r = insert_sql(connect_cursor[1], sql)
# 		close_connect_cursor(connect_cursor)
# 		if r:
# 			return {'status':'SUCCESS', "data":users_insert}, 200
# 		else:
# 			return {"status":"ERROR"}, 404

class UserLogin(Resource):

	parser = reqparse.RequestParser()
	parser.add_argument('username', type=str, required=True, help="Username field cannot be blank.")
	parser.add_argument('password', type=str, required=True,  help="Password field cannot be blank.")

	def get_roles(self, user_id):
		connect_cursor = get_connect_cursor()
		sql = 'select roles.name from user_roles, roles where user_roles.user_id = %s and user_roles.role_id=roles.id'
		c1 = user_id
		users  = select_sql(connect_cursor[1], sql % c1)
		close_connect_cursor(connect_cursor)
	def __init__(self) -> None:
		super().__init__()

	def post(self):
		try:
			data = self.parser.parse_args()
			# return data
			connect_cursor = get_connect_cursor()
			sql = 'select id, username, password from users where username = %s'
			c1 = format_str(data['username'])
			users  = select_sql(connect_cursor[1], sql % c1)
			close_connect_cursor(connect_cursor)

			if  users and len(users)==1:
				user = users[0]
				if check_password_hash(user['password'], data['password']):
					# if safe_str_cmp(user['password'], data['password']):
					username = user['username']
					id = user['id']
					# Get role name
					connect_cursor = get_connect_cursor()
					sql = f'SELECT roles.name FROM role_users, roles WHERE role_users.user_id = {id} and role_users.role_id=roles.id'
					role_name  = select_sql(connect_cursor[1], sql)
					role = ""
					if role_name and len(role_name)==1:
						role = role_name[0]['name']
					sql = f'SELECT * FROM employees WHERE id = {id}'
					c1 = format_number(id)
					persons  = select_sql(connect_cursor[1], sql)
					person = {}
					if persons:
						person = persons[0]
					access_token = create_access_token(identity=username, additional_claims={"role":role, "info":person})
					refresh_token = create_refresh_token(username, additional_claims={"role":role, "info":person})
					sql = f"UPDATE users set token='{access_token}' WHERE id={id}"
					login_update = update_sql(connect_cursor[1], sql)
					close_connect_cursor(connect_cursor)
					return {
						'access_token': access_token,
						'refresh_token': refresh_token
					}, 200
				else:
					return {"status": "ERROR", "info":"Make sure username and password is correct"}
			else:
				raise UsersNotFoundError()
		except Exception as e:
			return {"status":"ERROR", "info":str(e)}, 404
				

		

