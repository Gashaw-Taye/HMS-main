import re
from flask_restful import Resource,reqparse, marshal, fields
from resources.errors import Bed_roomsNotFoundError
from flask import request
from datetime import datetime
import copy
import shortuuid
import os
from common.db import *

bed_rooms_fields = {
	'id':fields.Integer,
	'room_id':fields.Integer,
	'bed_name':fields.String,
	'description':fields.String,
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
def bed_rooms_request_parser():
	input_parser = reqparse.RequestParser()
	input_parser.add_argument('room_id', type=int, required=True, location='json')
	input_parser.add_argument('bed_name', type=str, required=True, location='json')
	input_parser.add_argument('description', type=str, required=False, location='json')
	input_parser.add_argument('status', type=int, required=False, location='json')
	input_parser.add_argument('created_at', type=int, required=False, location='json')
	input_parser.add_argument('updated_at', type=int, required=False, location='json')
	return input_parser

def bed_rooms_args_parser(args):
	bed_rooms_updates = {}
	for k, v in args.items():
		bed_rooms_updates[k] = v
	return bed_rooms_updates

class Bed_rooms(Resource):
	def __init__(self):
		self.reqparse = bed_rooms_request_parser()
		super(Bed_rooms, self).__init__()

	# @requires_auth
	def get(self, id):
		connect_cursor = get_connect_cursor()
		sql = 'select * from bed_rooms where id = %s'
		c1 = format_number(id)
		bed_rooms  = select_sql(connect_cursor[1], sql % c1)
		close_connect_cursor(connect_cursor)
		if  bed_rooms is None:
			raise  Bed_roomsNotFoundError()
		return {'bed_rooms': marshal( bed_rooms, bed_rooms_fields)}

	def put(self, id):
		try:
			connect_cursor = get_connect_cursor()
			sql = 'select * from bed_rooms where id = %s'
			c1 = format_number(id)
			bed_rooms = select_sql(connect_cursor[1], sql % c1)
			if not bed_rooms:
				raise Bed_roomsNotFoundError()
			args = self.reqparse.parse_args()
			bed_rooms_insert = bed_rooms_args_parser(args)
			pre_sql = ""
			for k, v in bed_rooms_insert.items():
				if v not in ["", None]:
					if isinstance(v, int):
						pre_sql += f"{k}={v}, "
					else:
						pre_sql += f"{k}='{v}', "
			sql = f"UPDATE bed_rooms SET {pre_sql}updated_at = unix_timestamp() WHERE id={id}"
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
			sql = 'select * from bed_rooms where id = %s'
			c1 = format_number(id)
			bed_rooms = select_sql(connect_cursor[1], sql % c1)
			if not bed_rooms:
				raise Bed_roomsNotFoundError()
			sql = 'update bed_rooms set status = %s, updated_at = unix_timestamp() where id = %s'
			c1 = False
			c2 = format_number(id)
			r = update_sql(connect_cursor[1], sql % (c1, c2))
			close_connect_cursor(connect_cursor)
			return {'Deleted':'success'}
		except Exception as e:
			return {"status":"ERROR", "msg": f"{e}"},500

class Bed_roomsList(Resource):
	def __init__(self):
		self.reqparse = bed_rooms_request_parser()
		super(Bed_roomsList, self).__init__()

	# @requires_auth
	def get(self):
		connect_cursor = get_connect_cursor()
		sql = 'select * from bed_rooms'
		bed_roomss = select_sql(connect_cursor[1], sql)
		close_connect_cursor(connect_cursor)
		if  bed_roomss is None:
			raise  Bed_roomsNotFoundError()
		all_bed_roomss = [marshal(bed_rooms, bed_rooms_fields) for bed_rooms in bed_roomss]
		active_bed_roomss  = [bed_rooms_dict for bed_rooms_dict in all_bed_roomss if bed_rooms_dict['status'] != False]
		return {'bed_rooms': marshal( active_bed_roomss, bed_rooms_fields)}

	def post(self):
		try:
			args = self.reqparse.parse_args()
			bed_rooms_insert = bed_rooms_args_parser(args)
			connect_cursor = get_connect_cursor()

			keys = ""
			values = ""
			for k, v in bed_rooms_insert.items():
				if v not in ["", None]:
					if isinstance(v, int):
						keys += f"{k}, "
						values += f"{v}, "
					else:
						keys += f"{k}, "
						values += f"'{v}', "
			sql = f'INSERT INTO bed_rooms({keys}created_at, updated_at) VALUES ({values}unix_timestamp(), unix_timestamp())'
			r = insert_sql(connect_cursor[1], sql)
			close_connect_cursor(connect_cursor)
			if r:
				return {'status':'SUCCESS', "data":bed_rooms_insert}, 200
			else:
				return {"status":"ERROR"}, 404
		except Exception as e:
			return {"status":"ERROR", "msg": f"{e}"},500
