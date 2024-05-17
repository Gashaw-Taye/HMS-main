import re
from flask_restful import Resource,reqparse, marshal, fields
from resources.errors import Office_expensesNotFoundError
from flask import request
from datetime import datetime
import copy
import shortuuid
import os
from common.db import *

office_expenses_fields = {
	'id':fields.Integer,
	'reason':fields.String,
	'price':fields.Integer,
	'paid_by':fields.String,
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
def office_expenses_request_parser():
	input_parser = reqparse.RequestParser()
	input_parser.add_argument('reason', type=str, required=False, location='json')
	input_parser.add_argument('price', type=str, required=False, location='json')
	input_parser.add_argument('paid_by', type=str, required=False, location='json')
	input_parser.add_argument('status', type=int, required=False, location='json')
	input_parser.add_argument('created_at', type=int, required=False, location='json')
	input_parser.add_argument('updated_at', type=int, required=False, location='json')
	return input_parser

def office_expenses_args_parser(args):
	office_expenses_updates = {
		'reason':args['reason'],
		'price':args['price'],
		'paid_by':args['paid_by'],
		'status':args['status'],
		'created_at':args['created_at'],
		'updated_at':args['updated_at'],
	}
	return office_expenses_updates

class Office_expenses(Resource):
	def __init__(self):
		self.reqparse = office_expenses_request_parser()
		super(Office_expenses, self).__init__()

	# @requires_auth
	def get(self, id):
		connect_cursor = get_connect_cursor()
		sql = 'select * from office_expenses where id = %s'
		c1 = format_number(id)
		office_expenses  = select_sql(connect_cursor[1], sql % c1)
		close_connect_cursor(connect_cursor)
		if  office_expenses is None:
			raise  Office_expensesNotFoundError()
		return {' office_expenses': marshal( office_expenses, office_expenses_fields)}

	def put(self, id):
		connect_cursor = get_connect_cursor()
		sql = 'select * from office_expenses where id = %s'
		c1 = format_number(id)
		office_expenses = select_sql(connect_cursor[1], sql % c1)
		if not office_expenses:
			raise Office_expensesNotFoundError()
		args = self.reqparse.parse_args()
		office_expenses_insert = office_expenses_args_parser(args)
		sql = 'update office_expenses set reason=%s,price=%s,paid_by=%s,status=%s,updated_at = unix_timestamp() WHERE id=%s'
		c2 = format_str(office_expenses_insert['reason'])
		c3 = format_number(office_expenses_insert['price'])
		c4 = format_str(office_expenses_insert['paid_by'])
		c5 = format_number(office_expenses_insert['status'])
		r = update_sql(connect_cursor[1], sql % (c2,c3,c4,c5,c1))
		close_connect_cursor(connect_cursor)
		return {'update':'success'}

	# @requires_auth
	def delete(self, id):
		connect_cursor = get_connect_cursor()
		sql = 'select * from office_expenses where id = %s'
		c1 = format_number(id)
		office_expenses = select_sql(connect_cursor[1], sql % c1)
		if not office_expenses:
			raise Office_expensesNotFoundError()
		sql = 'update office_expenses set status = %s, updated_at = unix_timestamp() where id = %s'
		c1 = False
		c2 = format_number(id)
		r = update_sql(connect_cursor[1], sql % (c1, c2))
		close_connect_cursor(connect_cursor)
		return {'Deleted':'success'}

class Office_expensesList(Resource):
	def __init__(self):
		self.reqparse = office_expenses_request_parser()
		super(Office_expensesList, self).__init__()

	# @requires_auth
	def get(self):
		connect_cursor = get_connect_cursor()
		sql = 'select * from office_expenses'
		office_expensess = select_sql(connect_cursor[1], sql)
		close_connect_cursor(connect_cursor)
		if  office_expensess is None:
			raise  Office_expensesNotFoundError()
		all_office_expensess = [marshal(office_expenses, office_expenses_fields) for office_expenses in office_expensess]
		active_office_expensess  = [office_expenses_dict for office_expenses_dict in all_office_expensess if office_expenses_dict['status'] != False]
		return {' office_expenses': marshal( active_office_expensess, office_expenses_fields)}

	def post(self):
		args = self.reqparse.parse_args()
		office_expenses_insert = office_expenses_args_parser(args)
		connect_cursor = get_connect_cursor()

		sql = 'INSERT INTO office_expenses(reason,price,paid_by,status, created_at, updated_at) VALUES (%s,%s,%s,%s, unix_timestamp(), unix_timestamp())'
		c1 = format_str(office_expenses_insert['reason'])
		c2 = format_number(office_expenses_insert['price'])
		c3 = format_str(office_expenses_insert['paid_by'])
		c4 = format_number(office_expenses_insert['status'])
		r = insert_sql(connect_cursor[1], sql % (c1,c2,c3,c4))
		close_connect_cursor(connect_cursor)
		return {'insert':office_expenses_insert }

