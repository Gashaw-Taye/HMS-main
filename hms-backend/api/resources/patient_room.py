import re
from flask_restful import Resource,reqparse, marshal
from resources.errors import Patient_roomNotFoundError
from resources.shared import patient_room_fields
from flask import request
from datetime import datetime
from common.db import *

def patient_room_request_parser():
	input_parser = reqparse.RequestParser()
	input_parser.add_argument('person_id', type=int, required=False, location='json')
	input_parser.add_argument('room_id', type=int, required=False, location='json')
	input_parser.add_argument('enterance_date', type=int, required=False, location='json')
	input_parser.add_argument('leave_date', type=int, required=False, location='json')
	input_parser.add_argument('status', type=int, required=False, location='json')
	input_parser.add_argument('created_at', type=int, required=False, location='json')
	input_parser.add_argument('updated_at', type=int, required=False, location='json')
	return input_parser

def patient_room_args_parser(args):
	patient_room_updates = {}
	for k, v in args.items():
		patient_room_updates[k] = v
	return patient_room_updates

class Patient_room(Resource):
	def __init__(self):
		self.reqparse = patient_room_request_parser()
		super(Patient_room, self).__init__()

	# @requires_auth
	def get(self, id, rid):
		connect_cursor = get_connect_cursor()
		sql = f'select * from patient_room where person_id={id} and id = {rid}'
		patient_room  = select_sql(connect_cursor[1], sql)
		close_connect_cursor(connect_cursor)
		if  patient_room is None:
			raise  Patient_roomNotFoundError()
		return {'patient_room': marshal( patient_room, patient_room_fields)}

	def put(self, id, rid):
		try:
			connect_cursor = get_connect_cursor()
			sql = f'select * from patient_room where person_id={id} and id = {rid}'
			patient_room = select_sql(connect_cursor[1], sql)
			if not patient_room:
				raise Patient_roomNotFoundError()
			args = self.reqparse.parse_args()
			patient_room_insert = patient_room_args_parser(args)

			pre_sql = ""
			for k, v in patient_room_insert.items():
				if v not in ["", None]:
					if isinstance(v, int):
						pre_sql += f"{k}={v}, "
					else:
						pre_sql += f"{k}='{v}', "
			sql = f"UPDATE patient_room SET {pre_sql}updated_at = unix_timestamp() WHERE id={id}"
			r = update_sql(connect_cursor[1], sql)
			close_connect_cursor(connect_cursor)
			if r:
				return {'status':'SUCCESS'}, 200
			else:
				return {"status":"ERROR"}, 404
		except Exception as e:
			return {"status":"ERROR", "msg": f"{e}"}, 500

	# @requires_auth
	def delete(self, id, rid):
		try:
			connect_cursor = get_connect_cursor()
			sql = f'select * from patient_room where person_id={id} and id = {rid}'
			c1 = format_number(id)
			patient_room = select_sql(connect_cursor[1], sql % c1)
			if not patient_room:
				raise Patient_roomNotFoundError()
			sql = 'UPDATE patient_room SET status = 0, updated_at = unix_timestamp() WHERE person_id={id} and id = {rid}'
			r = update_sql(connect_cursor[1], sql)
			if r:
				return {'status':'SUCCESS'}, 200
			else:
				return {"status":"ERROR"}, 404
		except Exception as e:
			return {"status":"ERROR", "msg": f"{e}"}, 500

class Patient_roomList(Resource):
	def __init__(self):
		self.reqparse = patient_room_request_parser()
		super(Patient_roomList, self).__init__()

	# @requires_auth
	def get(self, id):
		connect_cursor = get_connect_cursor()
		sql = f'select * from patient_room WHERE person_id={id}'
		patient_rooms = select_sql(connect_cursor[1], sql)
		close_connect_cursor(connect_cursor)
		if  patient_rooms is None:
			raise  Patient_roomNotFoundError()
		all_patient_rooms = [marshal(patient_room, patient_room_fields) for patient_room in patient_rooms]
		active_patient_rooms  = [patient_room_dict for patient_room_dict in all_patient_rooms if patient_room_dict['status'] != False]
		return {' patient_room': marshal( active_patient_rooms, patient_room_fields)}

	def post(self, id):
		try:
			args = self.reqparse.parse_args()
			patient_room_insert = patient_room_args_parser(args)
			connect_cursor = get_connect_cursor()

			keys = "person_id"
			values = f"{id}"
			for k, v in patient_room_insert.items():
				if v not in ["", None]:
					if isinstance(v, int):
						keys += f"{k}, "
						values += f"{v}, "
					else:
						keys += f"{k}, "
						values += f"'{v}', "
			sql = f'INSERT INTO patient_room ({keys}created_at, updated_at) VALUES ({values}unix_timestamp(), unix_timestamp())'
			r = insert_sql(connect_cursor[1], sql)
			close_connect_cursor(connect_cursor)
			if r:
				return {'status':'SUCCESS', "data":patient_room_insert}, 200
			else:
				return {"status":"ERROR"}, 404
		except Exception as e:
			return {"status":"ERROR", "msg": f"{e}"}, 500

