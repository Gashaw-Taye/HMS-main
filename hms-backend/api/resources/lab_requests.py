import profile
import re
from flask_restful import Resource,reqparse, marshal, fields
from resources.errors import Lab_requestsNotFoundError, PersonNotFoundError
from resources.shared import lab_requests_fields
from common.db import *

def lab_requests_request_parser():
	input_parser = reqparse.RequestParser()
	input_parser.add_argument('requested_by', type=int, required=False, location='json')
	input_parser.add_argument('lab_expert', type=int, required=False, location='json')
	input_parser.add_argument('lab_id', type=int, required=False, location='json')
	input_parser.add_argument('lab_result', type=str, required=False, location='json')
	input_parser.add_argument('lab_result_attachment', type=str, required=False, location='json')
	input_parser.add_argument('status', type=int, required=False, location='json')
	input_parser.add_argument('created_at', type=int, required=False, location='json')
	input_parser.add_argument('updated_at', type=int, required=False, location='json')
	return input_parser

def lab_requests_args_parser(args):
	lab_requests_updates = {}
	for k, v in args.items():
		lab_requests_updates[k] = v
	return lab_requests_updates

class Lab_requests(Resource):
	def __init__(self):
		self.reqparse = lab_requests_request_parser()
		super(Lab_requests, self).__init__()

	# @requires_auth
	def get(self, id, lid):
		connect_cursor = get_connect_cursor()
		sql = f'select * from lab_requests where id = {lid} and patient_id={id}'
		lab_requests  = select_sql(connect_cursor[1], sql)
		close_connect_cursor(connect_cursor)
		if  lab_requests is None:
			raise  Lab_requestsNotFoundError()
		return {'lab_requests': marshal( lab_requests, lab_requests_fields)}

	def put(self, id, lid):
		try:
			connect_cursor = get_connect_cursor()
			sql = f'select * from lab_requests where id = {lid} and patient_id = {id}'
			lab_requests = select_sql(connect_cursor[1], sql)
			if not lab_requests:
				raise Lab_requestsNotFoundError()
			args = self.reqparse.parse_args()
			lab_requests_insert = lab_requests_args_parser(args)
			
			pre_sql = ""
			for k, v in lab_requests_insert.items():
				if v not in ["", None]:
					if isinstance(v, int):
						pre_sql += f"{k}={v}, "
					else:
						pre_sql += f"{k}='{v}', "
			sql = f"UPDATE lab_requests SET {pre_sql}updated_at = unix_timestamp() WHERE id={lid}"
			r = update_sql(connect_cursor[1], sql)
			close_connect_cursor(connect_cursor)
			if r:
				return {'status':'SUCCESS'}, 200
			else:
				return {"status":"ERROR"}, 404
		except Exception as e:
			return {"status":"ERROR", "msg": f"{e}"},500

	# @requires_auth
	def delete(self, id, lid):
		try:
			connect_cursor = get_connect_cursor()
			sql = f'select * from lab_requests where id = {lid} and patient_id={id} and status > 0'
			lab_requests = select_sql(connect_cursor[1], sql)
			if not lab_requests:
				raise Lab_requestsNotFoundError()
			sql = f'update lab_requestsset status = 0, updated_at = unix_timestamp() where id = {lid} and patient_id={id}'
			r = update_sql(connect_cursor[1], sql)
			close_connect_cursor(connect_cursor)
			if r:
				return {'status':'SUCCESS'}
			else:
				return {"status":"ERROR"}
		except Exception as e:
			return {"status":"ERROR", "msg": f"{e}"},500

class Lab_requestsList(Resource):
	def __init__(self):
		self.reqparse = lab_requests_request_parser()
		super(Lab_requestsList, self).__init__()

	# @requires_auth
	def get(self, id):
		connect_cursor = get_connect_cursor()
		sql = f'select * from lab_requests WHERE patient_id={id}'
		lab_requestss = select_sql(connect_cursor[1], sql)
		close_connect_cursor(connect_cursor)
		if  lab_requestss is None:
			raise PersonNotFoundError()
		all_lab_requestss = [marshal(lab_requests, lab_requests_fields) for lab_requests in lab_requestss]
		active_lab_requestss  = [lab_requests_dict for lab_requests_dict in all_lab_requestss if lab_requests_dict['status'] != False]
		return {'lab_requests': marshal( active_lab_requestss, lab_requests_fields)}

	def post(self, id):
		try:
			args = self.reqparse.parse_args()
			lab_requests_insert = lab_requests_args_parser(args)
			connect_cursor = get_connect_cursor()
			sql = f'select * from persons WHERE id={id}'
			lab_requestss = select_sql(connect_cursor[1], sql)
			if not lab_requestss:
				close_connect_cursor(connect_cursor)
				raise PersonNotFoundError()
			keys = "patient_id, "
			values = f"{id}, "
			for k, v in lab_requests_insert.items():
				if v not in ["", None]:
					if isinstance(v, int):
						keys += f"{k}, "
						values += f"{v}, "
					else:
						keys += f"{k}, "
						values += f"'{v}', "
			sql = f'INSERT INTO lab_requests({keys}created_at, updated_at) VALUES ({values}unix_timestamp(), unix_timestamp())'
			r = insert_sql(connect_cursor[1], sql)
			close_connect_cursor(connect_cursor)
			if r:
				return {'status':'SUCCESS', "data":lab_requests_insert}, 200
			else:
				return {"status":"ERROR"}, 404
		except Exception as e:
			return {"status":"ERROR", "msg": f"{e}"},500