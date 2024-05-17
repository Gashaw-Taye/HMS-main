from ast import arg
import re
from flask_restful import Resource,reqparse, marshal, fields
from resources.errors import EmployeesNotFoundError, PersonsNotFoundError
from common.db import *

employees_fields = {
	'id':fields.Integer,
	'org_id':fields.Integer,
	'first_name':fields.String,
	'last_name':fields.String,
	'grand_father':fields.String,
	'gender':fields.String,
	'date_of_birth':fields.String,
	'email':fields.String,
	'person_type':fields.String,
	'prefix':fields.String,
	'profile_image':fields.String,
	'status':fields.Integer,
	'created_at':fields.Integer,
	'updated_at':fields.Integer,

}

def employees_request_parser():
	input_parser = reqparse.RequestParser()
	input_parser.add_argument('org_id', type=int, required=False, location='json')
	input_parser.add_argument('first_name', type=str, required=False, location='json')
	input_parser.add_argument('last_name', type=str, required=False, location='json')
	input_parser.add_argument('grand_father', type=str, required=False, location='json')
	input_parser.add_argument('gender', type=str, required=False, location='json')
	input_parser.add_argument('date_of_birth', type=str, required=False, location='json')
	input_parser.add_argument('email', type=str, required=False, location='json')
	input_parser.add_argument('person_type', type=str, required=False, location='json')
	input_parser.add_argument('prefix', type=str, required=False, location='json')
	input_parser.add_argument('profile_image', type=str, required=False, location='json')
	input_parser.add_argument('status', type=int, required=False, location='json')
	input_parser.add_argument('created_at', type=int, required=False, location='json')
	input_parser.add_argument('updated_at', type=int, required=False, location='json')
	return input_parser

def employees_args_parser(args):
	employees_updates = {}
	for k, v in args.items():
		employees_updates[k] = v
	return employees_updates

class Employees(Resource):
	def __init__(self):
		self.reqparse = employees_request_parser()
		super(Employees, self).__init__()

	# @requires_auth
	def get(self, id):
		connect_cursor = get_connect_cursor()
		sql = f'SELECT * FROM employees WHERE id = {id}'
		employees  = select_sql(connect_cursor[1], sql)

		if  employees is None:
			# close_connect_cursor(connect_cursor)
			raise  EmployeesNotFoundError()
		employee = employees[0]
		employee['users'] = []
		
		sql = f'SELECT * FROM users WHERE id = {id}'
		users  = select_sql(connect_cursor[1], sql)
		if users:
			employee['users'] = users

		# Get roles
		employee['roles'] = []
		sql = f'SELECT roles.name FROM roles JOIN role_users ON role_users.role_id = roles.id and role_users.user_id ={id}'
		roles  = select_sql(connect_cursor[1], sql)
		if roles:
			employee['roles'] = roles
		return {'employees': employee}

	def put(self, id):
		try:
			connect_cursor = get_connect_cursor()
			sql = f'select * from employees where id = {id}'
			employees = select_sql(connect_cursor[1], sql)
			if not employees:
				raise EmployeesNotFoundError()
			args = self.reqparse.parse_args()
			employees_insert = employees_args_parser(args)

			pre_sql = ""
			for k, v in employees_insert.items():
				if v not in ["", None]:
					if isinstance(v, int):
						pre_sql += f"{k}={v}, "
					else:
						pre_sql += f"{k}='{v}', "
			sql = f"UPDATE employees SET {pre_sql}updated_at = unix_timestamp() WHERE id={id}"
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
			sql = f'select * from employees where id = {id}'
			c1 = format_number(id)
			employees = select_sql(connect_cursor[1], sql)
			if not employees:
				raise EmployeesNotFoundError()
			sql = f'update employeesset status = 0, updated_at = unix_timestamp() where id = {id}'
			r = update_sql(connect_cursor[1], sql)
			close_connect_cursor(connect_cursor)
			if r:
				return {'status':'SUCCESS'}, 200
			else:
				return {"status":"ERROR"}, 404
		except Exception as e:
			return {"status":"ERROR", "msg": f"{e}"},500

class EmployeesList(Resource):
	def __init__(self):
		self.reqparse = employees_request_parser()
		super(EmployeesList, self).__init__()

	# @requires_auth
	def get(self):
		connect_cursor = get_connect_cursor()
		sql = 'select * from employees'
		employeess = select_sql(connect_cursor[1], sql)
		close_connect_cursor(connect_cursor)
		if  employeess is None:
			raise  EmployeesNotFoundError()
		all_employeess = [marshal(employees, employees_fields) for employees in employeess]
		active_employeess  = [employees_dict for employees_dict in all_employeess if employees_dict['status'] != False]
		return {'employees': marshal( active_employeess, employees_fields)}

	def post(self):
		try:
			args = self.reqparse.parse_args()
			employees_insert = employees_args_parser(args)
			connect_cursor = get_connect_cursor()
			keys = ""
			values = ""
			for k, v in employees_insert.items():
				if v not in ["", None]:
					if isinstance(v, int):
						keys += f"{k}, "
						values += f"{v}, "
					else:
						keys += f"{k}, "
						values += f"'{v}', "
			sql = f'INSERT INTO employees({keys}created_at, updated_at) VALUES ({values}unix_timestamp(), unix_timestamp())'
			r = insert_sql(connect_cursor[1], sql)
			close_connect_cursor(connect_cursor)
			if r:
				return {'status':'SUCCESS', "data":employees_insert}, 200
			else:
				return {"status":"ERROR"}, 404
		except Exception as e:
			return {"status":"ERROR", "msg": f"{e}"},500

class EmployeDetails(Resource):
	def __init__(self) -> None:
		super().__init__()

	def get(self, id):
		connect_cursor = get_connect_cursor()
		# get persons
		persons = {}
		sql = f'select * from employees where id = {id}'
		person  = select_sql(connect_cursor[1], sql)
		if not person:
			raise PersonsNotFoundError()
		persons = person[0]

		# Get roles
		sql = f'SELECT roles.id, roles.name, roles.org_id, roles.description, role_users.status FROM roles JOIN role_users on role_users.user_id = roles.id and role_users.status=1 and user_id = {id} WHERE roles.status = 1'
		roles  = select_sql(connect_cursor[1], sql)
		if roles:
			persons['roles'] = roles
		close_connect_cursor(connect_cursor)
		if  persons is None:
			raise  PersonsNotFoundError()
		return {'employee': persons}