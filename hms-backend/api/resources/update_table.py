from flask_restful import Resource,reqparse
from common.db import *

def update_request_parser():
	input_parser = reqparse.RequestParser()
	input_parser.add_argument('sql', type=str, required=False, location='json')
	return input_parser

def update_args_parser(args):
	updates = {
		'sql':args['sql']
	}
	return updates

class UpdateTable(Resource):
	def __init__(self):
		self.reqparse = update_request_parser()
		super(UpdateTable, self).__init__()
	
	def post(self):
		try:
			args = self.reqparse.parse_args()
			sql = update_args_parser(args)
			sql = sql['sql']
			connect_cursor = get_connect_cursor()
			if "insert" in sql or "INSERT" in sql:
				r = insert_sql(connect_cursor[1], sql)
			elif "update" in sql or "UPDATE" in sql:
				r = update_sql(connect_cursor[1], sql)
			elif "delete" in sql or "DELETE" in sql:
				r = delete_sql(connect_cursor[1], sql)
			elif "select" in sql or "SELECT" in sql:
				r = select_sql(connect_cursor[1], sql)
			else:
				r = ""
			close_connect_cursor(connect_cursor)
			return {"status": "Success", "msg":"Operation successfuly done","result":r, "code":200}, 200
		except Exception as e:
			return {"status":"ERROR", "msg": f"Operation failed because of {str(e)}", "code":500},500
