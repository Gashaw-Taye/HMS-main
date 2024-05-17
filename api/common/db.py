import pymysql
import os


def get_db_host():
    env_db_host = os.environ.get('DB_HOST')
    db_host = "localhost"
    if env_db_host is not None and len(env_db_host.strip()) > 0:
        db_host = env_db_host.strip()
    return db_host


def get_db_username():
    env_db_username = os.environ.get('DB_USERNAME')
    db_username = "root"
    if env_db_username is not None and len(env_db_username.strip()) > 0:
        db_username = env_db_username.strip()
    return db_username


def get_db_password():
    env_db_password = os.environ.get('DB_PASSWORD')
    db_password = ""
    if env_db_password is not None and len(env_db_password.strip()) > 0:
        db_password = env_db_password.strip()
    return db_password


def get_connect_cursor(db='bernos'):
    connect = pymysql.Connect(
        host=get_db_host(),
        port=3306,
        user=get_db_username(),
        passwd=get_db_password(),
        db=db,
        charset='utf8'
    )
    # Get cursor
    cursor = connect.cursor(pymysql.cursors.DictCursor)
    return (connect, cursor)

def close_connect_cursor(connect_cursor_tuple):
    connect = connect_cursor_tuple[0]
    cursor = connect_cursor_tuple[1]
    cursor.close()
    connect.close()


def select_sql(cursor, sql):
    cursor.execute(sql)
    my_result = []
    for row in cursor.fetchall():
        my_result.append(row)
    return my_result


def insert_sql(cursor, sql):
    cursor.execute(sql)
    r = cursor.lastrowid
    r = cursor.connection.insert_id()
    cursor.connection.commit()
    return r


def update_sql(cursor, sql):
    cursor.execute(sql)
    cursor.connection.commit()
    return cursor.rowcount


def delete_sql(cursor, sql):
    cursor.execute(sql)
    cursor.connection.commit()
    return cursor.rowcount


def format_str(input_str):
    if input_str is None:
        return "null"
    tmp = str(input_str)
    while len(tmp) > 0 and tmp[-1] == "\\":
        tmp = tmp[0:-1]
    my_result = "'" + tmp.replace("'", "\\'") + "'"
    return my_result


def format_number(input_str):
    if input_str is None:
        return "null"
    return int(input_str)


def format_date(input_str):
    if input_str is None:
        return "null"
    if type(input_str) is str and input_str.strip() == 'unix_timestamp()':
        return 'unix_timestamp()'
    if type(input_str) is int:
        return input_str
    raise Exception("ellegal date input: %s" % input_str)


def format_like(input_str):
    if input_str is None:
        raise Exception('ellegal like for None.')
    tmp = str(input_str)
    tmp = tmp.replace("'", "\\'")
    tmp = tmp.replace("%", "\\%")
    my_result = "'%" + tmp + "%'"
    return my_result


def format_like_right(input_str):
    if input_str is None:
        raise Exception('ellegal like for None.')
    tmp = str(input_str)
    tmp = tmp.replace("'", "\\'")
    tmp = tmp.replace("%", "\\%")
    my_result = "'" + tmp + "%'"
    return my_result