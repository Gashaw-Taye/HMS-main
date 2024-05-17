from common.db import *
import requests
import json

def fetch_sql(sql):
    print(sql)
    connect_cursor = get_connect_cursor()
    result  = select_sql(connect_cursor[1], sql)
    close_connect_cursor(connect_cursor)
    if result:
        return result
    return None

def sql_execute(sql):

    url = "http://localhost:9000/update"
    payload = json.dumps({
        "sql": sql
    })
    headers = {
        'Content-Type': 'application/json',
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    return response.text
   

    










