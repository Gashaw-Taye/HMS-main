import re
from flask_restful import Resource,reqparse, marshal, fields
from resources.errors import PatientsNotFoundError, PersonsNotFoundError
from resources.shared import patients_fields
from common.db import *
from flask import request

def patients_request_parser():
	input_parser = reqparse.RequestParser()
	input_parser.add_argument('patient_id', type=int, required=False, location='json')
	input_parser.add_argument('consulted_by', type=int, required=False, location='json')
	input_parser.add_argument('pre_examination', type=str, required=False, location='json')
	input_parser.add_argument('examinations', type=str, required=False, location='json')
	input_parser.add_argument('status', type=int, required=False, location='json')
	input_parser.add_argument('created_at', type=int, required=False, location='json')
	input_parser.add_argument('updated_at', type=int, required=False, location='json')
	return input_parser

def patients_args_parser(args):
	patients_updates = {}
	for k, v in args.items():
		patients_updates[k] = v
	return patients_updates

class Patients(Resource):
	def __init__(self):
		self.reqparse = patients_request_parser()
		super(Patients, self).__init__()

	# @requires_auth
	def get(self, id, pid):
		connect_cursor = get_connect_cursor()
		sql = f'select * from patients where id = {pid}'
		patients  = select_sql(connect_cursor[1], sql)
		close_connect_cursor(connect_cursor)
		if  patients is None:
			raise  PatientsNotFoundError()
		return {'patients': marshal( patients, patients_fields)}

	def put(self, id, pid):
		try:
			connect_cursor = get_connect_cursor()
			sql = f'select * from patients JOIN persons ON patients.patient_id = persons.id WHERE persons.id = {id} and patients.id = {pid}'
			patients = select_sql(connect_cursor[1], sql)
			if not patients:
				raise PatientsNotFoundError()
			args = self.reqparse.parse_args()
			patients_insert = patients_args_parser(args)

			pre_sql = ""
			for k, v in patients_insert.items():
				if v not in ["", None]:
					if isinstance(v, int):
						pre_sql += f"{k}={v}, "
					else:
						pre_sql += f"{k}='{v}', "
			sql = f"UPDATE patients SET {pre_sql}updated_at = unix_timestamp() WHERE id={pid}"
			r = update_sql(connect_cursor[1], sql)
			close_connect_cursor(connect_cursor)
			if r:
				return {'status':'SUCCESS'}, 200
			else:
				return {"status":"ERROR"}, 404
		except Exception as e:
			return {"status":"ERROR", "msg": f"{e}"}, 500

	# @requires_auth
	def delete(self, id, pid):
		try:
			connect_cursor = get_connect_cursor()
			sql = f'select * from patients JOIN persons ON patients.patient_id = persons.id WHERE persons.id = {id} and patients.id = {pid}'
			patients = select_sql(connect_cursor[1], sql)
			if not patients:
				raise PatientsNotFoundError()
			sql = f'update patientsset status = 0, updated_at = unix_timestamp() where id = {pid}'
			r = update_sql(connect_cursor[1], sql)
			close_connect_cursor(connect_cursor)
			if r:
				return {'status':'SUCCESS'}, 200
			else:
				return {"status":"ERROR"}, 404
		except Exception as e:
			return {"status":"ERROR", "msg": f"{e}"}, 500

class PatientsList(Resource):
	def __init__(self):
		self.reqparse = patients_request_parser()
		super(PatientsList, self).__init__()

	# @requires_auth
	def get(self, id):
		query = ""
		args = request.args
		if args:
			query += " WHERE "
			for key, val in args.items():
				if key == 'status':
					query += 'persons.'+str(key)+" = "+str(val) + " and "
				else:
					query += str(key)+" = "+str(val) + " and "

			query = query[:-4]
		connect_cursor = get_connect_cursor()
		sql = 'select patients.*, concat(persons.first_name, persons.last_name) as doctor_name FROM patients \
			LEFT JOIN persons ON persons.id = patient_id'+query
		patients = select_sql(connect_cursor[1], sql)
		if  patients is None:
			raise  PatientsNotFoundError()
		patient_details = {}
		for patient in patients:
			id = patient['patient_id']
			# get person
			sql = 'select * from persons where id = %s'
			c1 = format_number(id)
			person  = select_sql(connect_cursor[1], sql % c1)
			if not person:
				raise PersonsNotFoundError()
			if id not in patient_details:
				patient_details[id] = person[0]
			if 'patient_history' not in patient_details[id]:
				patient_details[id]['patient_history'] = []
			patient_details[id]['patient_history'].append(patient)

			# get prescriptions
			sql = "SELECT prescriptions.*, concat(persons.first_name, ' ', persons.last_name) as doctor_name, \
				concat(p2.first_name, ' ' , p2.last_name) as pharmacist_name FROM persons INNER JOIN prescriptions \
					on persons.id = prescriptions.provided_by INNER JOIN persons p2 on p2.id = prescriptions.approved_pharmacist WHERE person_id=%s"
		
			# sql = 'select * from prescriptions where person_id = %s'
			c1 = format_number(id)
			prescriptions  = select_sql(connect_cursor[1], sql % c1)
			if prescriptions:
				patient_details[id]['prescriptions'] = prescriptions

			# get patient_room
			sql = 'select * from patient_room where person_id = %s'
			c1 = format_number(id)
			patient_rooms  = select_sql(connect_cursor[1], sql % c1)
			if patient_rooms:
				patient_details[id]['bed_room'] = patient_rooms
		close_connect_cursor(connect_cursor)
		return {'patients': patient_details}

	def post(self, id):
		try:
			args = self.reqparse.parse_args()
			patients_insert = patients_args_parser(args)
			patients_insert['pre_examination'] = str(patients_insert['pre_examination'])
			patients_insert['examinations'] = str(patients_insert['examinations'])
			connect_cursor = get_connect_cursor()
			sql = f'select * from persons where id = {id}'
			person  = select_sql(connect_cursor[1], sql)
			if not person:
				raise PersonsNotFoundError()

			keys = "patient_id, "
			values = f"{id}, "
			for k, v in patients_insert.items():
				if v not in ["", None]:
					if isinstance(v, int):
						keys += f"{k}, "
						values += f"{v}, "
					else:
						keys += f"{k}, "
						values += f"'{v}', "
			sql = f'INSERT INTO patients ({keys}created_at, updated_at) VALUES ({values}unix_timestamp(), unix_timestamp())'
			r = insert_sql(connect_cursor[1], sql)
			close_connect_cursor(connect_cursor)
			if r:
				return {'status':'SUCCESS', "data":patients_insert}, 200
			else:
				return {"status":"ERROR"}, 404
		except Exception as e:
			return {"status":"ERROR", "msg": f"{e}"}, 500




