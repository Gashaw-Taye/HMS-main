from flask_restful import Resource,reqparse, marshal
from resources.errors import PrescriptionsNotFoundError, PersonNotFoundError
from common.db import *
from resources.shared import prescriptions_fields

def prescriptions_request_parser():
	input_parser = reqparse.RequestParser()
	# input_parser.add_argument('person_id', type=int, required=False, location='json')
	input_parser.add_argument('prescription', type=str, required=False, location='json')
	input_parser.add_argument('provided_by', type=int, required=False, location='json')
	input_parser.add_argument('approved_pharmacist', type=str, required=False, location='json')
	input_parser.add_argument('dosage', type=str, required=False, location='json')
	input_parser.add_argument('frequancy', type=str, required=False, location='json')
	input_parser.add_argument('no_of_day', type=str, required=False, location='json')
	input_parser.add_argument('food_relation', type=str, required=False, location='json')
	input_parser.add_argument('instruction', type=str, required=False, location='json')
	input_parser.add_argument('status', type=int, required=False, location='json')
	input_parser.add_argument('created_at', type=int, required=False, location='json')
	input_parser.add_argument('updated_at', type=int, required=False, location='json')
	return input_parser

def prescriptions_args_parser(args):
	prescriptions_updates = {}
	for k, v in args.items():
		prescriptions_updates[k] = v
	return prescriptions_updates

class Prescriptions(Resource):
	def __init__(self):
		self.reqparse = prescriptions_request_parser()
		super(Prescriptions, self).__init__()

	# @requires_auth
	def get(self, id, pid):
		connect_cursor = get_connect_cursor()
		sql = 'select * from prescriptions where id = %s'
		c1 = format_number(id)
		prescriptions  = select_sql(connect_cursor[1], sql % c1)
		close_connect_cursor(connect_cursor)
		if  prescriptions is None:
			raise  PrescriptionsNotFoundError()
		return {'prescriptions': marshal( prescriptions, prescriptions_fields)}

	def put(self, id, pid):
		try:
			connect_cursor = get_connect_cursor()
			sql = f'select * from prescriptions where person_id={id} and id = {pid}'
			prescriptions = select_sql(connect_cursor[1], sql)
			if not prescriptions:
				raise PrescriptionsNotFoundError()
			args = self.reqparse.parse_args()
			prescriptions_insert = prescriptions_args_parser(args)
			pre_sql = ""
			for k, v in prescriptions_insert.items():
				if v not in ["", None]:
					if isinstance(v, int):
						pre_sql += f"{k}={v}, "
					else:
						pre_sql += f"{k}='{v}', "
			sql = f"UPDATE prescriptions SET {pre_sql}updated_at = unix_timestamp() WHERE id={pid}"
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
			sql = f'select * from prescriptions where person_id={id} and id = {pid} and status > 0'
			prescriptions = select_sql(connect_cursor[1], sql)
			if not prescriptions:
				raise PrescriptionsNotFoundError()
			sql = f'update prescriptionsset status = 0, updated_at = unix_timestamp() where id = {pid}'
			r = update_sql(connect_cursor[1], sql)
			close_connect_cursor(connect_cursor)
			if r:
				return {'status':'SUCCESS'}, 200
			else:
				return {"status":"ERROR"}, 404
		except Exception as e:
			return {"status":"ERROR", "msg": f"{e}"}, 500

class PrescriptionsList(Resource):
	def __init__(self):
		self.reqparse = prescriptions_request_parser()
		super(PrescriptionsList, self).__init__()

	# @requires_auth
	def get(self, id):
		connect_cursor = get_connect_cursor()
		sql = f'select * from prescriptions where person_id={id}'
		prescriptionss = select_sql(connect_cursor[1], sql)
		close_connect_cursor(connect_cursor)
		if  prescriptionss is None:
			raise  PrescriptionsNotFoundError()
		all_prescriptionss = [marshal(prescriptions, prescriptions_fields) for prescriptions in prescriptionss]
		active_prescriptionss  = [prescriptions_dict for prescriptions_dict in all_prescriptionss if prescriptions_dict['status'] != False]
		return {'prescriptions': marshal( active_prescriptionss, prescriptions_fields)}

	def post(self, id):
		try:
			args = self.reqparse.parse_args()
			prescriptions_insert = prescriptions_args_parser(args)
			connect_cursor = get_connect_cursor()
			sql = f'SELECT * FROM persons WHERE id={id} and status > 0'
			persons = select_sql(connect_cursor[1], sql)
			if persons is None:
				raise PersonNotFoundError()
			keys = "patient_id, "
			values = f"{id}, "
			for k, v in prescriptions_insert.items():
				if v not in ["", None]:
					if isinstance(v, int):
						keys += f"{k}, "
						values += f"{v}, "
					else:
						keys += f"{k}, "
						values += f"'{v}', "
			sql = f'INSERT INTO prescriptions ({keys}created_at, updated_at) VALUES ({values}unix_timestamp(), unix_timestamp())'
			r = insert_sql(connect_cursor[1], sql)
			close_connect_cursor(connect_cursor)
			if r:
				return {'status':'SUCCESS', "data":prescriptions_insert}, 200
			else:
				return {"status":"ERROR"}, 404
		
		except Exception as e:
			return {"status":"ERROR", "msg": f"{e}"}, 500

