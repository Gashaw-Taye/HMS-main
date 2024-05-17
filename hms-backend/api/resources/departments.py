import re
from flask_restful import Resource,reqparse, marshal, fields
from resources.errors import DepartmentsNotFoundError
from common.db import *

departments_fields = {
	'id':fields.Integer,
	'report_to':fields.Integer,
	'org_id':fields.Integer,
	'name':fields.String,
	'status':fields.Integer,
	'created_at':fields.Integer,
	'updated_at':fields.Integer,

	}

string_regex = '^[A-Za-z]\w'
num_regex = '^[0-9]'
def string_validator(value):
    if re.search(string_regex, value):
        return value
    else:
        raise ValueError("Name value is not valid")


def find_match(contact, key, value): 
    return [(index,details) for (index, details) in enumerate(contact) if key in details and details[key] == value]

        # parser
def departments_request_parser():
	input_parser = reqparse.RequestParser()
	input_parser.add_argument('report_to', type=int, required=False, location='json')
	input_parser.add_argument('org_id', type=int, required=False, location='json')
	input_parser.add_argument('name', type=str, required=False, location='json')
	input_parser.add_argument('status', type=int, required=False, location='json')
	input_parser.add_argument('created_at', type=int, required=False, location='json')
	input_parser.add_argument('updated_at', type=int, required=False, location='json')
	return input_parser

def departments_args_parser(args):
	departments_updates = {}
	for k, v in args.items():
		departments_updates[k] = v
	return departments_updates

class Departments(Resource):
	def __init__(self):
		self.reqparse = departments_request_parser()
		super(Departments, self).__init__()

	# @requires_auth
	def get(self, id):
		connect_cursor = get_connect_cursor()
		sql = f'select * from departments where id = {id}'
		departments  = select_sql(connect_cursor[1], sql)
		close_connect_cursor(connect_cursor)
		if  departments is None:
			raise  DepartmentsNotFoundError()
		return {'departments': marshal( departments, departments_fields)}

	def put(self, id):
		try:
			connect_cursor = get_connect_cursor()
			sql = f'select * from departments where id = {id}'
			c1 = format_number(id)
			departments = select_sql(connect_cursor[1], sql)
			if not departments:
				raise DepartmentsNotFoundError()
			args = self.reqparse.parse_args()
			departments_insert = departments_args_parser(args)
			pre_sql = ""
			for k, v in departments_insert.items():
				if v not in ["", None]:
					if isinstance(v, int):
						pre_sql += f"{k}={v}, "
					else:
						pre_sql += f"{k}='{v}', "
			sql = f"UPDATE departments SET {pre_sql}updated_at = unix_timestamp() WHERE id={id}"
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
			sql = f'select * from departments where id = {id}'
			departments = select_sql(connect_cursor[1], sql)
			if not departments:
				raise DepartmentsNotFoundError()
			sql = f'update departments set status = 0, updated_at = unix_timestamp() where id = {id}'
			r = update_sql(connect_cursor[1], sql)
			close_connect_cursor(connect_cursor)
			if r:
				return {'status':'SUCCESS'}, 200
			else:
				return {"status":"ERROR"}, 404
		except Exception as e:
			return {"status":"ERROR", "msg": f"{e}"}, 500

class DepartmentsList(Resource):
	def __init__(self):
		self.reqparse = departments_request_parser()
		super(DepartmentsList, self).__init__()

	# @requires_auth
	def get(self):
		connect_cursor = get_connect_cursor()
		sql = 'select * from departments'
		departmentss = select_sql(connect_cursor[1], sql)
		close_connect_cursor(connect_cursor)
		if  departmentss is None:
			raise  DepartmentsNotFoundError()
		all_departmentss = [marshal(departments, departments_fields) for departments in departmentss]
		active_departmentss  = [departments_dict for departments_dict in all_departmentss if departments_dict['status'] != False]
		return {'departments': marshal( active_departmentss, departments_fields)}

	def post(self):
		try:
			args = self.reqparse.parse_args()
			departments_insert = departments_args_parser(args)
			connect_cursor = get_connect_cursor()

			keys = ""
			values = ""
			for k, v in departments_insert.items():
				if v not in ["", None]:
					if isinstance(v, int):
						keys += f"{k}, "
						values += f"{v}, "
					else:
						keys += f"{k}, "
						values += f"'{v}', "
			sql = f'INSERT INTO departments ({keys}created_at, updated_at) VALUES ({values}unix_timestamp(), unix_timestamp())'
			r = insert_sql(connect_cursor[1], sql)
			close_connect_cursor(connect_cursor)
			if r:
				return {'status':'SUCCESS', "data":departments_insert}, 200
			else:
				return {"status":"ERROR"}, 404
		except Exception as e:
			return {"status":"ERROR", "msg": f"{e}"}, 500

