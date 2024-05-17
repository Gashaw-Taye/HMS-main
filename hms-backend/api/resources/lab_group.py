import re
from flask_restful import Resource,reqparse, marshal, fields
from resources.errors import Lab_groupNotFoundError
from flask import request
from datetime import datetime
import copy
import shortuuid
import os
from common.db import *

lab_group_fields = {
	'id':fields.Integer,
	'org_id':fields.Integer,
	'name':fields.String,
	'created_at':fields.Integer,
	'status':fields.Integer,
	'updated_at':fields.Integer,
}

def lab_group_request_parser():
	input_parser = reqparse.RequestParser()
	input_parser.add_argument('org_id', type=int, required=False, location='json')
	input_parser.add_argument('name', type=str, required=False, location='json')
	input_parser.add_argument('created_at', type=int, required=False, location='json')
	input_parser.add_argument('status', type=int, required=False, location='json')
	input_parser.add_argument('updated_at', type=int, required=False, location='json')
	return input_parser

def lab_group_args_parser(args):
	lab_group_updates = {}
	for k, v in args.items():
		lab_group_updates[k] = v
	return lab_group_updates

class Lab_group(Resource):
	def __init__(self):
		self.reqparse = lab_group_request_parser()
		super(Lab_group, self).__init__()

	# @requires_auth
	def get(self, id):
		connect_cursor = get_connect_cursor()
		lab_groups = {}
		sql = 'select * from lab_group where id = %s'
		c1 = format_number(id)
		lab_group  = select_sql(connect_cursor[1], sql % c1)
		
		if  lab_group is None:
			raise  Lab_groupNotFoundError()
		lab_groups = lab_group[0]
		sql = f'select labs.* from labs JOIN lab_group on labs.lab_group_id = lab_group.id and labs.status=1 and lab_group.id = {id}'
		labs  = select_sql(connect_cursor[1], sql)
		if labs:
			lab_groups['labs'] = labs
		close_connect_cursor(connect_cursor)
		return {"lab_groups":lab_groups}
		# return {'lab_group': marshal( lab_group, lab_group_fields)}

	def put(self, id):
		try:
			connect_cursor = get_connect_cursor()
			sql = 'select * from lab_group where id = %s'
			c1 = format_number(id)
			lab_group = select_sql(connect_cursor[1], sql % c1)
			if not lab_group:
				raise Lab_groupNotFoundError()
			args = self.reqparse.parse_args()
			lab_group_insert = lab_group_args_parser(args)

			pre_sql = ""
			for k, v in lab_group_insert.items():
				if v not in ["", None]:
					if isinstance(v, int):
						pre_sql += f"{k}={v}, "
					else:
						pre_sql += f"{k}='{v}', "
			sql = f"UPDATE lab_group SET {pre_sql}updated_at = unix_timestamp() WHERE id={id}"
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
			sql = 'select * from lab_group where id = %s'
			c1 = format_number(id)
			lab_group = select_sql(connect_cursor[1], sql % c1)
			if not lab_group:
				raise Lab_groupNotFoundError()
			sql = 'update lab_group set status = %s, updated_at = unix_timestamp() where id = %s'
			c1 = False
			c2 = format_number(id)
			r = update_sql(connect_cursor[1], sql % (c1, c2))
			close_connect_cursor(connect_cursor)
			return {'Deleted':'success'}
		except Exception as e:
			return {"status":"ERROR", "msg": f"{e}"},500

class Lab_groupList(Resource):
	def __init__(self):
		self.reqparse = lab_group_request_parser()
		super(Lab_groupList, self).__init__()

	# @requires_auth
	def get(self):
		connect_cursor = get_connect_cursor()
		sql = 'select * from lab_group'
		lab_groups = select_sql(connect_cursor[1], sql)
		if  lab_groups is None:
			raise  Lab_groupNotFoundError()
		all_lab_groups = [marshal(lab_group, lab_group_fields) for lab_group in lab_groups]
		active_lab_groups  = [lab_group_dict for lab_group_dict in all_lab_groups if lab_group_dict['status'] != False]
		lab_groups = []
		if active_lab_groups:
			for i, active_lab_group in enumerate(active_lab_groups):
				id = active_lab_group['id']
				sql = f'select labs.* from labs JOIN lab_group on labs.lab_group_id = lab_group.id and labs.status=1 and lab_group.id = {id}'
				labs  = select_sql(connect_cursor[1], sql)
				if labs:
					active_lab_group['labs'] = labs
				lab_groups.append(active_lab_group)
		close_connect_cursor(connect_cursor)
		return {'lab_groups':lab_groups}
		# return {'lab_group': marshal( lab_groups, lab_group_fields)}

	def post(self):
		try:
			args = self.reqparse.parse_args()
			lab_group_insert = lab_group_args_parser(args)
			connect_cursor = get_connect_cursor()
			keys = ""
			values = ""
			for k, v in lab_group_insert.items():
				if v not in ["", None]:
					if isinstance(v, int):
						keys += f"{k}, "
						values += f"{v}, "
					else:
						keys += f"{k}, "
						values += f"'{v}', "
			sql = f'INSERT INTO lab_group({keys}created_at, updated_at) VALUES ({values}unix_timestamp(), unix_timestamp())'
			r = insert_sql(connect_cursor[1], sql)
			close_connect_cursor(connect_cursor)
			if r:
				return {'status':'SUCCESS', "data":lab_group_insert}, 200
			else:
				return {"status":"ERROR"}, 404
		except Exception as e:
			return {"status":"ERROR", "msg": f"{e}"},500

