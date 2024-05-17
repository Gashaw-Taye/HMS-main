import re
from flask_restful import Resource,reqparse, marshal, fields
from resources.errors import LabsNotFoundError
from flask import request
from datetime import datetime
import copy
import shortuuid
import os
from common.db import *

labs_fields = {
	'id':fields.Integer,
	'lab_group_id':fields.Integer,
	'name':fields.String,
	'description':fields.String,
	'status':fields.Integer,
	'created_at':fields.Integer,
	'updated_at':fields.Integer,

	}

def labs_request_parser():
	input_parser = reqparse.RequestParser()
	# input_parser.add_argument('id', type=int, required=False, location='json')
	input_parser.add_argument('lab_group_id', type=int, required=False, location='json')
	input_parser.add_argument('name', type=str, required=False, location='json')
	input_parser.add_argument('description', type=str, required=False, location='json')
	input_parser.add_argument('status', type=int, required=False, location='json')
	input_parser.add_argument('created_at', type=int, required=False, location='json')
	input_parser.add_argument('updated_at', type=int, required=False, location='json')
	return input_parser

def labs_args_parser(args):
	labs_updates = {}
	for k, v in args.items():
		labs_updates[k] = v
	return labs_updates

class Labs(Resource):
	def __init__(self):
		self.reqparse = labs_request_parser()
		super(Labs, self).__init__()

	# @requires_auth
	def get(self, id):
		connect_cursor = get_connect_cursor()
		sql = 'select * from labs where id = %s'
		c1 = format_number(id)
		labs  = select_sql(connect_cursor[1], sql % c1)
		close_connect_cursor(connect_cursor)
		if  labs is None:
			raise  LabsNotFoundError()
		return {'labs': marshal( labs, labs_fields)}

	def put(self, id):
		try:
			connect_cursor = get_connect_cursor()
			sql = f'select * from labs where id = {id}'
			labs = select_sql(connect_cursor[1], sql)
			if not labs:
				raise LabsNotFoundError()
			args = self.reqparse.parse_args()
			labs_insert = labs_args_parser(args)
			pre_sql = ""
			for k, v in labs_insert.items():
				if v not in ["", None]:
					if isinstance(v, int):
						pre_sql += f"{k}={v}, "
					else:
						pre_sql += f"{k}='{v}', "
			sql = f"UPDATE labs SET {pre_sql}updated_at = unix_timestamp() WHERE id={id}"
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
			sql = f'select * from labs where id = {id}'
			labs = select_sql(connect_cursor[1], sql)
			if not labs:
				raise LabsNotFoundError()
			sql = f'update labsset status = 0, updated_at = unix_timestamp() where id = {id}'
			r = update_sql(connect_cursor[1], sql)
			close_connect_cursor(connect_cursor)
			if r:
				return {'status':'SUCCESS'}, 200
			else:
				return {"status":"ERROR"}, 404
		except Exception as e:
			return {"status":"ERROR", "msg": f"{e}"},500

class LabsList(Resource):
	def __init__(self):
		self.reqparse = labs_request_parser()
		super(LabsList, self).__init__()

	# @requires_auth
	def get(self):
		connect_cursor = get_connect_cursor()
		sql = 'select * from labs'
		labss = select_sql(connect_cursor[1], sql)
		close_connect_cursor(connect_cursor)
		if  labss is None:
			raise  LabsNotFoundError()
		all_labss = [marshal(labs, labs_fields) for labs in labss]
		active_labss  = [labs_dict for labs_dict in all_labss if labs_dict['status'] != False]
		return {'labs': marshal( active_labss, labs_fields)}

	def post(self):
		try:
			args = self.reqparse.parse_args()
			labs_insert = labs_args_parser(args)
			connect_cursor = get_connect_cursor()

			keys = ""
			values = ""
			for k, v in labs_insert.items():
				if v not in ["", None]:
					if isinstance(v, int):
						keys += f"{k}, "
						values += f"{v}, "
					else:
						keys += f"{k}, "
						values += f"'{v}', "
			sql = f'INSERT INTO labs({keys}created_at, updated_at) VALUES ({values}unix_timestamp(), unix_timestamp())'
			r = insert_sql(connect_cursor[1], sql)
			close_connect_cursor(connect_cursor)
			if r:
				return {'status':'SUCCESS', "data":labs_insert}, 200
			else:
				return {"status":"ERROR"}, 404
		except Exception as e:
			return {"status":"ERROR", "msg": f"{e}"},500

