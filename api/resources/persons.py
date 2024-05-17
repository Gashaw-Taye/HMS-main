from flask import request
from flask_restful import Resource,reqparse, marshal
from resources.errors import PersonsNotFoundError
from resources.shared import persons_fields
from common.db import *

def persons_request_parser():
	input_parser = reqparse.RequestParser()
	input_parser.add_argument('org_id', type=int, required=False, location='json')
	input_parser.add_argument('first_name', type=str, required=False, location='json')
	input_parser.add_argument('last_name', type=str, required=False, location='json')
	input_parser.add_argument('grand_father', type=str, required=False, location='json')
	input_parser.add_argument('gender', type=str, required=False, location='json')
	input_parser.add_argument('date_of_birth', type=str, required=False, location='json')
	input_parser.add_argument('email', type=str, required=False, location='json')
	input_parser.add_argument('person_type', type=str, required=False, location='json')
	input_parser.add_argument('prefix', type=str, required=False, location='json')
	input_parser.add_argument('profile_image', type=str, required=False, location='json')
	input_parser.add_argument('status', type=int, required=False, location='json')
	input_parser.add_argument('created_at', type=int, required=False, location='json')
	input_parser.add_argument('updated_at', type=int, required=False, location='json')
	return input_parser	

def persons_args_parser(args):
	persons_updates = {}
	for k, v in args.items():
		persons_updates[k] = v
	return persons_updates

class Persons(Resource):
	def __init__(self):
		self.reqparse = persons_request_parser()
		super(Persons, self).__init__()

	# @requires_auth
	def get(self, id):
		connect_cursor = get_connect_cursor()
		sql = f'select * from persons where id = {id}'
		persons  = select_sql(connect_cursor[1], sql)
		close_connect_cursor(connect_cursor)
		if  persons is None:
			raise  PersonsNotFoundError()
		return {'person': marshal( persons, persons_fields)}

	def put(self, id):
		try:
			connect_cursor = get_connect_cursor()
			sql = f'select * from persons where id = {id}'
			persons = select_sql(connect_cursor[1], sql)
			if not persons:
				raise PersonsNotFoundError()
			args = self.reqparse.parse_args()
			persons_insert = persons_args_parser(args)

			pre_sql = ""
			for k, v in persons_insert.items():
				if v not in ["", None]:
					if isinstance(v, int):
						pre_sql += f"{k}={v}, "
					else:
						pre_sql += f"{k}='{v}', "
			sql = f"UPDATE persons SET {pre_sql}updated_at = unix_timestamp() WHERE id={id}"
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
			sql = f'select * from persons where id = {id}'
			persons = select_sql(connect_cursor[1], sql)
			if not persons:
				raise PersonsNotFoundError()
			sql = f'update persons set status = 0, updated_at = unix_timestamp() where id = {id}'
			r = update_sql(connect_cursor[1], sql)
			close_connect_cursor(connect_cursor)
			if r:
				return {'status':'SUCCESS'}, 200
			else:
				return {"status":"ERROR"}, 404
		except Exception as e:
			return {"status":"ERROR", "msg": f"{e}"}, 500

class PersonsList(Resource):
	def __init__(self):
		self.reqparse = persons_request_parser()
		super(PersonsList, self).__init__()

	# @requires_auth
	def get(self):
		query = ""
		args = request.args
		if args:
			query += " WHERE "
			for key, val in args.items():
				if key == 'status':
					if "," in val:
						val = val.split(",")
						query += 'persons.'+str(key)+" in "+str(tuple(val))+ " and "
					else:
						query += 'persons.'+str(key)+" = "+str(val) + " and "
			query = query[:-4]
		connect_cursor = get_connect_cursor()
		sql = f'select * from persons {query}'
		personss = select_sql(connect_cursor[1], sql)
		close_connect_cursor(connect_cursor)
		if  personss is None:
			raise  PersonsNotFoundError()
		all_personss = [marshal(persons, persons_fields) for persons in personss]
		active_personss  = [persons_dict for persons_dict in all_personss if persons_dict['status'] > 0]
		return {'persons': marshal( active_personss, persons_fields)}

	def post(self):
		try:
			args = self.reqparse.parse_args()
			persons_insert = persons_args_parser(args)
			connect_cursor = get_connect_cursor()
			keys = ""
			values = ""
			for k, v in persons_insert.items():
				if v not in ["", None]:
					if isinstance(v, int):
						keys += f"{k}, "
						values += f"{v}, "
					else:
						keys += f"{k}, "
						values += f"'{v}', "
			sql = f'INSERT INTO persons({keys}created_at, updated_at) VALUES ({values}unix_timestamp(), unix_timestamp())'
			r = insert_sql(connect_cursor[1], sql)
			close_connect_cursor(connect_cursor)
			if r:
				return {'status':'SUCCESS', "data":persons_insert}, 200
			else:
				return {"status":"ERROR"}, 404
		except Exception as e:
			return {"status":"ERROR", "msg": f"{e}"},500

class patientDetail(Resource):
	def __init__(self) -> None:
		super().__init__()

	def get(self, id):
		connect_cursor = get_connect_cursor()
		# get persons
		query = ""
		args = request.args
		if args:
			query += " and "
			for key, val in args.items():
				if key == 'status':
					query += 'persons.'+str(key)+" = "+str(val) + " and "
			query = query[:-4]
		connect_cursor = get_connect_cursor()
		persons = {}
		sql = f'select * from persons where id = {id}{query}'
		person  = select_sql(connect_cursor[1], sql)
		if not person:
			raise PersonsNotFoundError()
		persons = person[0]

		# get patients history
		persons['diagnosis'] = []
		sql = f"SELECT patients.*, concat(employees.first_name, ' ', employees.last_name) as doctor_name FROM patients, employees WHERE patient_id = {id} and patients.status > 0 and employees.id = patients.consulted_by"
		patients  = select_sql(connect_cursor[1], sql)
		
		if patients:
			persons['diagnosis'] = patients

		# get prescriptions
		persons['prescriptions'] = []
		sql = f"SELECT prescriptions.*, concat(employees.first_name, ' ', employees.last_name) as doctor_name FROM prescriptions, employees WHERE person_id={id} and prescriptions.status > 0 and employees.id=prescriptions.provided_by"
		prescriptions  = select_sql(connect_cursor[1], sql)
		if prescriptions:
			persons['prescriptions'] = prescriptions

		# get patient_room
		persons['bed_room'] = []
		sql = f'select * from patient_room where person_id = {id}  and status > 0'
		patient_rooms  = select_sql(connect_cursor[1], sql)
		if patient_rooms:
			persons['bed_room'] = patient_rooms

		# get pation labs
		persons['labs'] = []
		sql = f"""SELECT lab_requests.*, concat(x.first_name, ' ', x.last_name) as doctor_name, concat(y.first_name, ' ', y.last_name) as labratory_expert, labs.name as lab
		FROM lab_requests LEFT JOIN employees x on x.id = lab_requests.requested_by 
		LEFT JOIN employees y on x.id = lab_requests.lab_expert
		LEFT JOIN labs ON labs.id = lab_requests.lab_id
		WHERE patient_id = {id} and lab_requests.status > 0"""
		patient_rooms  = select_sql(connect_cursor[1], sql)
		if patient_rooms:
			persons['labs'] = patient_rooms

		# get Appointment details
		persons['appointments'] = []
		sql = f"SELECT appointments.*, concat(employees.first_name, ' ',employees.last_name) as doctor_name FROM appointments, employees WHERE patient_id = {id} and appointments.status > 0 and appointments.appointed_by = employees.id"
		appointments  = select_sql(connect_cursor[1], sql)
		if appointments:
			persons['appointments'] = appointments

		close_connect_cursor(connect_cursor)
		if  persons is None:
			raise  PersonsNotFoundError()
		return {'patient': persons}
		