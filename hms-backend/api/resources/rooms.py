import re
from flask_restful import Resource,reqparse, marshal, fields
from resources.errors import RoomsNotFoundError
from flask import request
from datetime import datetime
import copy
import shortuuid
import os
from common.db import *

rooms_fields = {
	'id':fields.Integer,
	'bld_id':fields.Integer,
	'room_name':fields.String,
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
def rooms_request_parser():
	input_parser = reqparse.RequestParser()
	input_parser.add_argument('bld_id', type=int, required=False, location='json')
	input_parser.add_argument('room_name', type=str, required=False, location='json')
	input_parser.add_argument('description', type=str, required=False, location='json')
	input_parser.add_argument('status', type=int, required=False, location='json')
	input_parser.add_argument('created_at', type=int, required=False, location='json')
	input_parser.add_argument('updated_at', type=int, required=False, location='json')
	return input_parser

def rooms_args_parser(args):
	rooms_updates = {}
	for k, v in args.items():
		rooms_updates[k] = v
	return rooms_updates

class Rooms(Resource):
	def __init__(self):
		self.reqparse = rooms_request_parser()
		super(Rooms, self).__init__()

	# @requires_auth
	def get(self, id):
		connect_cursor = get_connect_cursor()
		sql = f'select * from rooms where id = {id}'
		rooms  = select_sql(connect_cursor[1], sql)
		close_connect_cursor(connect_cursor)
		if  rooms is None:
			raise  RoomsNotFoundError()
		return {'rooms': marshal( rooms, rooms_fields)}

	def put(self, id):
		try:
			connect_cursor = get_connect_cursor()
			sql = f'select * from rooms where id = {id}'
			rooms = select_sql(connect_cursor[1], sql)
			if not rooms:
				raise RoomsNotFoundError()
			args = self.reqparse.parse_args()
			rooms_insert = rooms_args_parser(args)
			pre_sql = ""
			for k, v in rooms_insert.items():
				if v not in ["", None]:
					if isinstance(v, int):
						pre_sql += f"{k}={v}, "
					else:
						pre_sql += f"{k}='{v}', "
			sql = f"UPDATE rooms SET {pre_sql}updated_at = unix_timestamp() WHERE id={id}"
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
			sql = f'select * from rooms where id = {id}'
			rooms = select_sql(connect_cursor[1], sql)
			if not rooms:
				raise RoomsNotFoundError()
			sql = f'update rooms set status = 0, updated_at = unix_timestamp() where id = {id}'
			r = update_sql(connect_cursor[1], sql)
			close_connect_cursor(connect_cursor)
			if r:
				return {'status':'SUCCESS'}, 200
			else:
				return {"status":"ERROR"}, 404
		except Exception as e:
			return {"status":"ERROR", "msg": f"{e}"}, 500

class RoomsList(Resource):
	def __init__(self):
		self.reqparse = rooms_request_parser()
		super(RoomsList, self).__init__()

	# @requires_auth
	def get(self):
		connect_cursor = get_connect_cursor()
		sql = 'select * from rooms'
		roomss = select_sql(connect_cursor[1], sql)
		close_connect_cursor(connect_cursor)
		if  roomss is None:
			raise  RoomsNotFoundError()
		all_roomss = [marshal(rooms, rooms_fields) for rooms in roomss]
		active_roomss  = [rooms_dict for rooms_dict in all_roomss if rooms_dict['status'] != False]
		return {'rooms': marshal( active_roomss, rooms_fields)}

	def post(self):
		try:
			args = self.reqparse.parse_args()
			rooms_insert = rooms_args_parser(args)
			connect_cursor = get_connect_cursor()
			keys = ""
			values = ""
			for k, v in rooms_insert.items():
				if v not in ["", None]:
					if isinstance(v, int):
						keys += f"{k}, "
						values += f"{v}, "
					else:
						keys += f"{k}, "
						values += f"'{v}', "
			sql = f'INSERT INTO rooms ({keys}created_at, updated_at) VALUES ({values}unix_timestamp(), unix_timestamp())'
			r = insert_sql(connect_cursor[1], sql)
			close_connect_cursor(connect_cursor)
			if r:
				return {'status':'SUCCESS', "data":rooms_insert}, 200
			else:
				return {"status":"ERROR"}, 404
		except Exception as e:
			return {"status":"ERROR", "msg": f"{e}"}, 500

