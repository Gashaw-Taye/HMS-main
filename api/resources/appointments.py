import re
from xmlrpc.client import DateTime
from flask_restful import Resource,reqparse, marshal, fields
from resources.errors import AppointmentsNotFoundError, PersonNotFoundError
from common.db import *

appointments_fields = {
	'id':fields.Integer,
	'appointed_by':fields.Integer,
	'patient_id':fields.Integer,
	'appt_date':fields.String,
	'description':fields.String,
	'status':fields.Integer,
	'created_at':fields.Integer,
	'updated_at':fields.Integer,
}

def appointments_request_parser():
	input_parser = reqparse.RequestParser()
	input_parser.add_argument('appointed_by', type=int, required=False, location='json')
	input_parser.add_argument('patient_id', type=int, required=False, location='json')
	input_parser.add_argument('appt_date', type=str, required=True, location='json')
	input_parser.add_argument('description', type=str, required=False, location='json')
	input_parser.add_argument('status', type=int, required=False, location='json')
	input_parser.add_argument('created_at', type=int, required=False, location='json')
	input_parser.add_argument('updated_at', type=int, required=False, location='json')
	return input_parser

def appointments_args_parser(args):
	appointments_updates = {}
	for k, v in args.items():
		appointments_updates[k] = v
	return appointments_updates

class Appointments(Resource):
	def __init__(self):
		self.reqparse = appointments_request_parser()
		super(Appointments, self).__init__()

	# @requires_auth
	def get(self, id, aid):
		connect_cursor = get_connect_cursor()
		sql = f'select * from appointments where id = {aid} and patient_id = {id}'
		appointments  = select_sql(connect_cursor[1], sql)
		close_connect_cursor(connect_cursor)
		if  appointments is None:
			raise  AppointmentsNotFoundError()
		return {' appointments': marshal( appointments, appointments_fields)}

	def put(self, id, aid):
		try:
			connect_cursor = get_connect_cursor()
			sql = f'select * from appointments where id = {aid} and patient_id={id}'
			appointments = select_sql(connect_cursor[1], sql)
			if not appointments:
				raise AppointmentsNotFoundError()
			args = self.reqparse.parse_args()
			appointments_insert = appointments_args_parser(args)
			
			pre_sql = ""
			for k, v in appointments_insert.items():
				if v not in ["", None]:
					if isinstance(v, int):
						pre_sql += f"{k}={v}, "
					else:
						pre_sql += f"{k}='{v}', "
			sql = f"UPDATE appointments SET {pre_sql}updated_at = unix_timestamp() WHERE id={aid}"
			r = update_sql(connect_cursor[1], sql)
			close_connect_cursor(connect_cursor)
			if r:
				return {'status':'SUCCESS'}, 200
			else:
				return {"status":"ERROR"}, 404
		except Exception as e:
			return {"status":"ERROR", "msg": f"{e}"},500

	# @requires_auth
	def delete(self, id, aid):
		try:
			connect_cursor = get_connect_cursor()
			sql = f'select * from appointments where id = {aid} and patient_id={id} and status > 0'
			appointments = select_sql(connect_cursor[1], sql)
			if not appointments:
				raise AppointmentsNotFoundError()
			sql = f'update appointmentsset status = 0, updated_at = unix_timestamp() where id = {aid}'
			r = update_sql(connect_cursor[1], sql)
			close_connect_cursor(connect_cursor)
			if r:
				return {'status':'SUCCESS'}, 200
			else:
				return {"status":"ERROR"}, 404
		except Exception as e:
			return {"status":"ERROR", "msg": f"{e}"},500

class AppointmentsList(Resource):
	def __init__(self):
		self.reqparse = appointments_request_parser()
		super(AppointmentsList, self).__init__()

	# @requires_auth
	def get(self, id):
		connect_cursor = get_connect_cursor()
		sql = 'select * from appointments'
		appointmentss = select_sql(connect_cursor[1], sql)
		close_connect_cursor(connect_cursor)
		if  appointmentss is None:
			raise  AppointmentsNotFoundError()
		all_appointmentss = [marshal(appointments, appointments_fields) for appointments in appointmentss]
		active_appointmentss  = [appointments_dict for appointments_dict in all_appointmentss if appointments_dict['status'] != False]
		return {' appointments': marshal( active_appointmentss, appointments_fields)}

	def post(self, id):
		try:
			args = self.reqparse.parse_args()
			appointments_insert = appointments_args_parser(args)
			connect_cursor = get_connect_cursor()
			sql = f'SELECT * FROM persons WHERE id={id} and status > 0'
			appointments_insert['patient_id'] = id
			persons = select_sql(connect_cursor[1], sql)
			if persons is None:
				raise PersonNotFoundError()
			keys = ""
			values = ""
			for k, v in appointments_insert.items():
				if v not in ["", None]:
					if isinstance(v, int):
						keys += f"{k}, "
						values += f"{v}, "
					else:
						keys += f"{k}, "
						values += f"'{v}', "
			sql = f'INSERT INTO appointments({keys}created_at, updated_at) VALUES ({values}unix_timestamp(), unix_timestamp())'
			r = insert_sql(connect_cursor[1], sql)
			close_connect_cursor(connect_cursor)
			if r:
				return {'status':'SUCCESS', "data":appointments_insert}, 200
			else:
				return {"status":"ERROR"}, 404
		except Exception as e:
			return {"status":"ERROR", "msg": f"{e}"},500

