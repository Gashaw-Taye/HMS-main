import re
from flask_restful import Resource,reqparse, marshal, fields
from resources.errors import BuildingsNotFoundError
from flask import request
from datetime import datetime
import copy
import shortuuid
import os
from common.db import *

buildings_fields = {
	'id':fields.Integer,
	'org_id':fields.Integer,
	'name':fields.String,
	'description':fields.String,
	'status':fields.Integer,
	'created_at':fields.Integer,
	'updated_at':fields.Integer,

}

def buildings_request_parser():
	input_parser = reqparse.RequestParser()
	input_parser.add_argument('org_id', type=int, required=False, location='json')
	input_parser.add_argument('name', type=str, required=False, location='json')
	input_parser.add_argument('description', type=str, required=False, location='json')
	input_parser.add_argument('status', type=int, required=False, location='json')
	input_parser.add_argument('created_at', type=int, required=False, location='json')
	input_parser.add_argument('updated_at', type=int, required=False, location='json')
	return input_parser

def buildings_args_parser(args):
	buildings_updates = {}
	for k, v in args.items():
		buildings_updates[k] = v
	return buildings_updates

class Buildings(Resource):
	def __init__(self):
		self.reqparse = buildings_request_parser()
		super(Buildings, self).__init__()

	# @requires_auth
	def get(self, id):
		connect_cursor = get_connect_cursor()
		sql = f'select * from buildings where id = {id}'
		buildings  = select_sql(connect_cursor[1], sql)
		close_connect_cursor(connect_cursor)
		if  buildings is None:
			raise  BuildingsNotFoundError()
		return {'buildings': marshal( buildings, buildings_fields)}

	def put(self, id):
		try:
			connect_cursor = get_connect_cursor()
			sql = f'select * from buildings where id = {id}'
			buildings = select_sql(connect_cursor[1], sql)
			if not buildings:
				raise BuildingsNotFoundError()
			args = self.reqparse.parse_args()
			buildings_insert = buildings_args_parser(args)
			pre_sql = ""
			for k, v in buildings_insert.items():
				if v not in ["", None]:
					if isinstance(v, int):
						pre_sql += f"{k}={v}, "
					else:
						pre_sql += f"{k}='{v}', "
			sql = f"UPDATE buildings SET {pre_sql}updated_at = unix_timestamp() WHERE id={id}"
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
			sql = f'select * from buildings where id = {id} and status > 0'
			# return sql
			buildings = select_sql(connect_cursor[1], sql)
			if not buildings:
				raise BuildingsNotFoundError()
			sql = f'update buildings set status = 0, updated_at = unix_timestamp() where id = {id}'
			r = update_sql(connect_cursor[1], sql)
			close_connect_cursor(connect_cursor)
			if r:
				return {'status':'SUCCESS'}, 200
			else:
				return {"status":"ERROR"}, 404
		except Exception as e:
			return {"status":"ERROR", "msg": f"{e}"}, 500

class BuildingsList(Resource):
	def __init__(self):
		self.reqparse = buildings_request_parser()
		super(BuildingsList, self).__init__()

	# @requires_auth
	def get(self):
		connect_cursor = get_connect_cursor()
		sql = 'select * from buildings'
		buildingss = select_sql(connect_cursor[1], sql)
		close_connect_cursor(connect_cursor)
		if  buildingss is None:
			raise  BuildingsNotFoundError()
		all_buildingss = [marshal(buildings, buildings_fields) for buildings in buildingss]
		active_buildingss  = [buildings_dict for buildings_dict in all_buildingss if buildings_dict['status'] != False]
		return {'buildings': marshal( active_buildingss, buildings_fields)}

	def post(self):
		try:
			args = self.reqparse.parse_args()
			buildings_insert = buildings_args_parser(args)
			connect_cursor = get_connect_cursor()

			keys = ""
			values = ""
			for k, v in buildings_insert.items():
				if v not in ["", None]:
					if isinstance(v, int):
						keys += f"{k}, "
						values += f"{v}, "
					else:
						keys += f"{k}, "
						values += f"'{v}', "
			sql = f'INSERT INTO buildings({keys}created_at, updated_at) VALUES ({values}unix_timestamp(), unix_timestamp())'
			r = insert_sql(connect_cursor[1], sql)
			close_connect_cursor(connect_cursor)
			if r:
				return {'status':'SUCCESS', "data":buildings_insert}, 200
			else:
				return {"status":"ERROR"}, 404
		except Exception as e:
			return {"status":"ERROR", "msg": f"{e}"},500

