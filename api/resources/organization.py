import re
from flask_restful import Resource,reqparse, marshal, fields
from resources.errors import OrganizationNotFoundError
from common.db import *

organization_fields = {
	'id':fields.Integer,
	'org_name':fields.String,
	'status':fields.Integer,

	}
# parser
def organization_request_parser():
	input_parser = reqparse.RequestParser()
	input_parser.add_argument('org_name', type=str, required=False, location='json')
	input_parser.add_argument('status', type=int, required=False, location='json')
	return input_parser

def organization_args_parser(args):
	organization_updates = {
		'org_name':args['org_name'],
		'status':args['status'],
	}
	return organization_updates

class Organization(Resource):
	def __init__(self):
		self.reqparse = organization_request_parser()
		super(Organization, self).__init__()

	# @requires_auth
	def get(self, id):
		connect_cursor = get_connect_cursor()
		sql = f'select * from organization where id = {id}'
		organization  = select_sql(connect_cursor[1], sql)
		close_connect_cursor(connect_cursor)
		if  organization is None:
			raise  OrganizationNotFoundError()
		return {'organization': marshal( organization, organization_fields)}

	def put(self, id):
		try:
			connect_cursor = get_connect_cursor()
			sql = f'select * from organization where id = {id}'
			c1 = format_number(id)
			organization = select_sql(connect_cursor[1], sql)
			if not organization:
				raise OrganizationNotFoundError()
			args = self.reqparse.parse_args()
			organization_insert = organization_args_parser(args)
			pre_sql = ""
			for k, v in organization_insert.items():
				if v not in ["", None]:
					if isinstance(v, int):
						pre_sql += f"{k}={v}, "
					else:
						pre_sql += f"{k}='{v}', "
			sql = f"UPDATE organization SET {pre_sql}updated_at = unix_timestamp() WHERE id={id}"
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
			sql = f'select * from organization where id = {id} and status > 0'
			organization = select_sql(connect_cursor[1], sql)
			if not organization:
				raise OrganizationNotFoundError()
			sql = f'update organization set status = 0, updated_at = unix_timestamp() where id = {id}'
			r = update_sql(connect_cursor[1], sql)
			close_connect_cursor(connect_cursor)
			if r:
				return {'status':'SUCCESS'}, 200
			else:
				return {"status":"ERROR"}, 404
		except Exception as e:
			return {"status":"ERROR", "msg": f"{e}"}, 500

class OrganizationList(Resource):
	def __init__(self):
		self.reqparse = organization_request_parser()
		super(OrganizationList, self).__init__()

	# @requires_auth
	def get(self):
		connect_cursor = get_connect_cursor()
		sql = 'select * from organization'
		organizations = select_sql(connect_cursor[1], sql)
		close_connect_cursor(connect_cursor)
		if  organizations is None:
			raise  OrganizationNotFoundError()
		all_organizations = [marshal(organization, organization_fields) for organization in organizations]
		active_organizations  = [organization_dict for organization_dict in all_organizations if organization_dict['status'] != False]
		return {'organization': marshal( active_organizations, organization_fields)}, 200

	def post(self):
		try:
			args = self.reqparse.parse_args()
			organization_insert = organization_args_parser(args)
			connect_cursor = get_connect_cursor()

			keys = ""
			values = ""
			for k, v in organization_insert.items():
				if v not in ["", None]:
					if isinstance(v, int):
						keys += f"{k}, "
						values += f"{v}, "
					else:
						keys += f"{k}, "
						values += f"'{v}', "
			sql = f'INSERT INTO organization({keys}created_at, updated_at) VALUES ({values}unix_timestamp(), unix_timestamp())'
			r = insert_sql(connect_cursor[1], sql)
			close_connect_cursor(connect_cursor)
			if r:
				return {'status':'SUCCESS', "data":organization_insert}, 200
			else:
				return {"status":"ERROR"}, 404
		except Exception as e:
			return {"status":"ERROR", "msg": f"{e}"}, 500