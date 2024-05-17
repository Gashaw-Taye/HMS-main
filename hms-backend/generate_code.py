from api.common.db import *
def generate(object_name, object_fields):
    f = open("api/resources/"+object_name+".py", "w")
    f.write("import re\n")
    f.write("from flask_restful import Resource,reqparse, marshal, fields\n")
    f.write("from resources.errors import "+object_name.capitalize()+"NotFoundError\n")
    f.write("from flask import request\n")
    f.write("from datetime import datetime\n")
    f.write("import copy\n")
    f.write("import shortuuid\n")
    f.write("import os\n")
    f.write("from common.db import *\n\n")
    
    f.write(object_name+"_fields = {\n")

    for field, data_type in object_fields.items():
        f.write("\t'"+field+"':fields."+data_type+",\n")
    
    f.write("\n\t}\n")
    validation = """
string_regex = '^[A-Za-z]\w'
num_regex = '^[0-9]'
def string_validator(value):
    if re.search(string_regex, value):
        return value
    else:
        raise ValueError("Name value is not valid")\n

def find_match(contact, key, value): 
    return [(index,details) for (index, details) in enumerate(contact) if key in details and details[key] == value]\n
        """
    f.write(validation)
    f.write("# parser\n")

    f.write("def "+object_name+"_request_parser():\n")
    f.write("\tinput_parser = reqparse.RequestParser()\n")
    for field, data_type in object_fields.items():
        if field == 'id':
            continue
        if data_type == "Integer":
            new_data_type = "int"
        elif  data_type == "String":
            new_data_type = "str"
        f.write("\tinput_parser.add_argument('"+field+"', type="+new_data_type+", required=False, location='json')\n")
    f.write("\treturn input_parser\n\n")

    f.write("def "+object_name+"_args_parser(args):\n")
    f.write("\t"+object_name+"_updates = {\n")
    for field, data_type in object_fields.items():
        if field == 'id':
            continue
        f.write("\t\t'"+field+"':args['"+field+"'],\n")

    f.write("\t}\n")
    f.write("\treturn "+object_name+"_updates\n\n")

    # class
    f.write("class "+object_name.capitalize()+"(Resource):\n")
    f.write("\tdef __init__(self):\n")
    f.write("\t\tself.reqparse = "+object_name+"_request_parser()\n")
    f.write("\t\tsuper("+object_name.capitalize()+", self).__init__()\n\n")

    # get method
    f.write("\t# @requires_auth\n")
    f.write("\tdef get(self, id):\n")
    f.write("\t\tconnect_cursor = get_connect_cursor()\n")
    f.write("\t\tsql = 'select * from "+object_name+" where id = %s'\n")
    f.write("\t\tc1 = format_number(id)\n")
    f.write("\t\t"+object_name+"  = select_sql(connect_cursor[1], sql % c1)\n")
    f.write("\t\tclose_connect_cursor(connect_cursor)\n")
    f.write("\t\tif  "+object_name+" is None:\n")
    f.write("\t\t\traise  "+object_name.capitalize()+"NotFoundError()\n")
    f.write("\t\treturn {' "+object_name+"': marshal( "+object_name+", "+object_name+"_fields)}\n\n")

    # put method
    # @requires_auth
    f.write("\tdef put(self, id):\n")
    f.write("\t\tconnect_cursor = get_connect_cursor()\n")
    f.write("\t\tsql = 'select * from "+object_name+" where id = %s'\n")
    f.write("\t\tc1 = format_number(id)\n")
    f.write("\t\t"+object_name+" = select_sql(connect_cursor[1], sql % c1)\n")

    f.write("\t\tif not "+object_name+":\n")
    f.write("\t\t\traise "+object_name.capitalize()+"NotFoundError()\n")
    
    f.write("\t\targs = self.reqparse.parse_args()\n")
    f.write("\t\t"+object_name+"_insert = "+object_name+"_args_parser(args)\n")
    sql = "update "+object_name+" set "
    count = 2
    update_value = ""
    update_value_format = ""
    for field, data_type in object_fields.items():
        
        if field == 'id':
            continue
        if field == "created_at":
            continue
        if field == "updated_at":
            sql = sql+field+" = unix_timestamp(),"
            continue
        sql = sql+field+"=%s,"
        if data_type == "String":
            format_type = "format_str"
        else:
            format_type = "format_number"
        update_value_format = update_value_format+"\t\tc"+str(count)+" = "+format_type+"("+object_name+"_insert['"+field+"'])\n"
        
        update_value = update_value+"c"+str(count)+","
        count += 1
    sql = sql[:-1]+" WHERE id=%s"
    f.write("\t\tsql = '"+sql+"'\n")
    f.write(update_value_format) 
    f.write("\t\tr = update_sql(connect_cursor[1], sql % ("+update_value[:-1]+",c1))\n")
    f.write("\t\tclose_connect_cursor(connect_cursor)\n")
    f.write("\t\treturn {'update':'success'}\n\n")

    # delete
    f.write("\t# @requires_auth\n") 
    f.write("\tdef delete(self, id):\n") 
    f.write("\t\tconnect_cursor = get_connect_cursor()\n") 
    f.write("\t\tsql = 'select * from "+object_name+" where id = %s'\n") 
    f.write("\t\tc1 = format_number(id)\n") 
    f.write("\t\t"+object_name+" = select_sql(connect_cursor[1], sql % c1)\n") 

    f.write("\t\tif not "+object_name+":\n") 
    f.write("\t\t\traise "+object_name.capitalize()+"NotFoundError()\n") 

    f.write("\t\tsql = 'update "+object_name+" set status = %s, updated_at = unix_timestamp() where id = %s'\n") 
    f.write("\t\tc1 = False\n") 
    f.write("\t\tc2 = format_number(id)\n") 
    f.write("\t\tr = update_sql(connect_cursor[1], sql % (c1, c2))\n") 
    f.write("\t\tclose_connect_cursor(connect_cursor)\n") 
    f.write("\t\treturn {'Deleted':'success'}\n\n") 

    # class 2
    f.write("class "+object_name.capitalize()+"List(Resource):\n")
    f.write("\tdef __init__(self):\n")
    f.write("\t\tself.reqparse = "+object_name+"_request_parser()\n")
    f.write("\t\tsuper("+object_name.capitalize()+"List, self).__init__()\n\n")

    # getmethod
    # get method
    f.write("\t# @requires_auth\n")
    f.write("\tdef get(self):\n")
    f.write("\t\tconnect_cursor = get_connect_cursor()\n")
    f.write("\t\tsql = 'select * from "+object_name+"'\n")
    f.write("\t\t"+object_name+"s = select_sql(connect_cursor[1], sql)\n")
    f.write("\t\tclose_connect_cursor(connect_cursor)\n")
    f.write("\t\tif  "+object_name+"s is None:\n")
    f.write("\t\t\traise  "+object_name.capitalize()+"NotFoundError()\n")
    f.write("\t\tall_"+object_name+"s = [marshal("+object_name+", "+object_name+"_fields) for "+object_name+" in "+object_name+"s]\n")
    f.write("\t\tactive_"+object_name+"s  = ["+object_name+"_dict for "+object_name+"_dict in all_"+object_name+"s if "+object_name+"_dict['status'] != False]\n")
    f.write("\t\treturn {' "+object_name+"': marshal( active_"+object_name+"s, "+object_name+"_fields)}\n\n")

    # Post method
    # @requires_auth
    f.write("\tdef post(self):\n")
    f.write("\t\targs = self.reqparse.parse_args()\n")
    f.write("\t\t"+object_name+"_insert = "+object_name+"_args_parser(args)\n")
    f.write("\t\tconnect_cursor = get_connect_cursor()\n\n")
 
    sql = "INSERT INTO "+object_name
    count = 1
    update_value = ""
    update_value_format = ""
    update_per = ""
    sql_fields = ""
    for field, data_type in object_fields.items():
        if field in ['updated_at', 'created_at', 'id']:
            continue
        sql_fields = sql_fields+field+","
        if data_type == "String":
            format_type = "format_str"
        else:
            format_type = "format_number"
        update_value_format = update_value_format+"\t\tc"+str(count)+" = "+format_type+"("+object_name+"_insert['"+field+"'])\n"
        update_value = update_value+"c"+str(count)+","
        update_per = update_per+"%s,"
        count = count+1 
    sql = sql+"("+sql_fields+" created_at, updated_at) VALUES ("+update_per+" unix_timestamp(), unix_timestamp())"
    # f.write("\t\t"+update_value+"\n")
    # f.write(("\t\t"+update_value_format))
    # str = str[:-1]

    # sql_fields = sql_fields+" WHERE id=%s"
    f.write("\t\tsql = '"+sql+"'\n")
    f.write(update_value_format) 
    f.write("\t\tr = insert_sql(connect_cursor[1], sql % ("+update_value[:-1]+"))\n")
    f.write("\t\tclose_connect_cursor(connect_cursor)\n")
    f.write("\t\treturn {'insert':"+object_name+"_insert }\n\n")
     
        
    f.close()

    # append error.py
    f_error = open("api/resources/errors.py", "a")
    f_error.write("\n\nclass "+object_name.capitalize()+"NotFoundError(HTTPException):\n")
    f_error.write("\tdef __init__(self):\n")
    f_error.write("\t\tself.status_code = 404\n")
    f_error.write("\t\tself.message = 'Please check the "+object_name+" ID'\n")
    f_error.write("\t\tself.status = 'error'\n")
    f_error.write("\t\tself.response = ({'status': self.status,'message': self.message},self.status_code)\n")
    f_error.close()

def checkTableExists(dbcon, tablename, drop=False):
    # tablename = 'person'
    dbcur = dbcon.cursor()
    sql = "SELECT COUNT(*) FROM information_schema.tables WHERE table_name='%s'"%(tablename)
    # print({"SQL": sql})
    dbcur.execute(sql)
    result = dbcur.fetchone()[0]
    print(result, dbcur.fetchone())
    if result > 1:
        if drop:
            sql = "DROP TABLE %s"%(tablename)
            dbcur.execute(sql)
            dbcur.close()
            return True
        dbcur.close()
        return True

    dbcur.close()
    return True

def create_table(object_name, schema, drop=False):
    connect_cursor = get_connect_cursor()
    if checkTableExists(connect_cursor[0], object_name, drop):
        connect_cursor[1].execute(schema)
        print("----------- Table created successfully ----------------")
        # Commit your changes in the database
        connect_cursor[0].commit()
        #Closing the connection
        close_connect_cursor(connect_cursor)
    else:
        print("***************Table exists************************")

# tables and model generations

persons_object_name = "persons"
persons_object_fields = {"id":"Integer","org_id":"Integer","first_name": "String", "last_name": "String", "grand_father": "String", "gender": "String", "date_of_birth": "String", "email": "String", "person_type": "String", "prefix": "String",  "profile_image": "String", "status":"Boolean", "created_at":"Integer", "updated_at":"Integer"}
persons_table_schema = """
    CREATE TABLE `persons` (
    `id` int(11) NOT NULL auto_increment,
    `first_name` varchar(50) NOT NULL,
    `last_name` varchar(50) NOT NULL,
    `grand_father` varchar(50) NULL,
    `gender` varchar(5) NOT NULL,
    `date_of_birth` varchar(20) NOT NULL,
    `email` varchar(50) NULL,
    `person_type` varchar(20) NOT NULL,
    `prefix` varchar(10) NULL,
    `profile_image` varchar(200) NULL,
    `org_id` int(11) NOT NULL,
    `created_at` int(11) NOT NULL,
    `updated_at` int(11) NOT NULL,
    `status` tinyint(4) NOT NULL,
    PRIMARY KEY(id), 
    FOREIGN KEY(org_id) REFERENCES organization(id)
    );
"""

# buildings -------------------------
buildings_object_name = "buildings"
buildings_object_fields = {"id":"Integer","org_id":"Integer","name":"String","description":"String", "status":"Boolean", "created_at":"Integer", "updated_at":"Integer"}
buildings_table_schema = """
    CREATE TABLE `buildings` (
        `id` int(11) NOT NULL,
        `org_id` int(11) NOT NULL,
        `name` varchar(100) NOT NULL,
        `description` varchar(100) DEFAULT NULL,
        `status` bool DEFAULT 1,
        `created_at` int(11) DEFAULT NULL,
        `updated_at` int(11) DEFAULT NULL,
        PRIMARY KEY(id), 
        FOREIGN KEY(org_id) REFERENCES organizations(id)
        );
"""

# rooms
rooms_object_name = "rooms"
rooms_object_fields = {"id":"Integer", "bld_id":"Integer","room_name":"String","description":"String", "status":"Boolean", "created_at":"Integer", "updated_at":"Integer"}
rooms_table_schema = """
    CREATE TABLE `rooms` (
        `id` int(11) NOT NULL,
        `bld_id` int(11) NOT NULL,
        `name` varchar(100) NOT NULL,
        `description` varchar(100) DEFAULT NULL,
        `status` bool NOT NULL,
        `created_at` int(11) DEFAULT NULL,
        `updated_at` int(11) DEFAULT NULL,
        PRIMARY KEY(id), 
        FOREIGN KEY(bld_id) REFERENCES buildings(id)
        );
 """

# bed_rooms
bed_rooms_object_name = "bed_rooms"
bed_rooms_object_fields = {"id":"Integer","room_id":"Integer","bed_name": "String", "description": "String", "status":"Boolean", "created_at":"Integer", "updated_at":"Integer"}

bed_rooms_table_schema = """
    CREATE TABLE `bed_rooms` (
        `id` int(11) NOT NULL,
        `room_id` int(11) NOT NULL,
        `bed_name` varchar(100) NOT NULL,
        `description` varchar(100) NOT NULL,
        `status` bool NOT NULL,
        `created_at` int(11) DEFAULT NULL,
        `updated_at` int(11) DEFAULT NULL,
        PRIMARY KEY(id), 
        FOREIGN KEY(room_id) REFERENCES rooms(id)
        ) ENGINE=InnoDB DEFAULT CHARSET=latin1;
    """

# service_category
service_category_object_name = "service_category"
service_category_object_fields = {"id":"Integer", "office_id":"Integer","cat_name": "String","cat_description":"String","status":"Boolean","created_at":"Integer","updated_at":"Integer"}
service_category_table_schema = """
    CREATE TABLE `service_category` (
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `office_id` int(11) NOT NULL,
    `cat_name` varchar(50) NOT NULL,
    `cat_description` varchar(50) NOT NULL,
    `created_at` int(11) NOT NULL,
    `updated_at` int(11) NOT NULL,
    `status` tinyint(4) NOT NULL,
    PRIMARY KEY(id), 
    FOREIGN KEY(office_id) REFERENCES office(id)
    ) ENGINE=InnoDB DEFAULT CHARSET=latin1;
"""
# prescriptions
prescriptions_object_name = "prescriptions"
prescriptions_object_fields = {"id":"Integer", "person_id":"Integer","prescription": "String","provided_by": "String","approved_pharmacist":"String","dosage":"String","frequancy": "String","no_of_day":"String","food_relation":"String","instruction": "String","status":"Boolean","created_at":"Integer","updated_at":"Integer"}
prescriptions_table_schema = """
    CREATE TABLE `prescriptions`(
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `person_id` int(11) NOT NULL,
    `prescription` varchar(50) NOT NULL,
    `provided_by` int(11) NULL,
    `approved_pharmacist` int(11) NULL,
    `dosage` varchar(50) NOT NULL,
    `frequancy` varchar(50) NOT NULL,
    `no_of_day` varchar(50) NOT NULL,
    `food_relation` varchar(50) NOT NULL,
    `instruction` varchar(50) NOT NULL,
    `status` tinyint(4) NOT NULL,
    `created_at` int(11) NOT NULL,
    `updated_at` int(11) NOT NULL,    
    PRIMARY KEY(id),
    FOREIGN KEY(person_id) REFERENCES persons(id),
    FOREIGN KEY(provided_by) REFERENCES persons(id),
    FOREIGN KEY(approved_pharmacist) REFERENCES persons(id)
    );
"""

# users
users_object_name = "users"
users_object_fields = {"id":"Integer","person_id":"Integer","username": "String","password": "String","public_id":"Integer","token":"String","first_login": "String","last_login":"String","status":"Boolean","created_at":"Integer","updated_at":"Integer"}
users_table_schema = """
    CREATE TABLE `users`(
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `person_id` int(11) NOT NULL,
    `username` varchar(50) NOT NULL,
    `password` varchar(80) NOT NULL,
    `public_id` int(11) NOT NULL,
    `token` varchar(255) NOT NULL,
    `first_login` varchar(50) NOT NULL,
    `last_login` varchar(50) NOT NULL,
    `status` tinyint(4) NOT NULL,
    `created_at` int(11) NOT NULL,
    `updated_at` int(11) NOT NULL,    
    PRIMARY KEY(id),
    FOREIGN KEY(person_id) REFERENCES persons(id)
    ) ENGINE=InnoDB DEFAULT CHARSET=latin1;
"""

# lab_group
lab_group_object_name = "lab_group"
lab_group_object_fields = {"id":"Integer", "org_id":"Integer", "name": "String", "created_at":"Integer", "status":"Boolean", "updated_at":"Integer"}
lab_group_table_schema = """
    CREATE TABLE `lab_group`(
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `org_id` int(11) NOT NULL,
    `name` varchar(50) NOT NULL,
    `status` tinyint(4) NOT NULL,
    `created_at` int(11) NOT NULL,
    `updated_at` int(11) NOT NULL,    
    PRIMARY KEY(id),
    FOREIGN KEY(org_id) REFERENCES organization(id)
    )
"""

# labs
labs_object_name = "labs"
labs_object_fields = {"id":"Integer","lab_group_id":"Integer","name": "String", "description": "String", "status":"Boolean", "created_at":"Integer", "updated_at":"Integer"}
labs_table_schema = """
    CREATE TABLE `labs`(
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `lab_group_id` int(11) NOT NULL,
    `name` varchar(50) NOT NULL,
    `description` varchar(50) NULL,
    `status` tinyint(4) NOT NULL,
    `created_at` int(11) NOT NULL,
    `updated_at` int(11) NOT NULL,    
    PRIMARY KEY(id),
    FOREIGN KEY(lab_group_id) REFERENCES lab_group(id)
    )
"""

# patients
patients_object_name = "patients"
patients_object_fields = {"id":"Integer","patient_id":"Integer","consulted_by":"Integer","pre_examination": "String", "examinations": "String", "status":"Boolean", "created_at":"Integer", "updated_at":"Integer"}
patients_table_schema = """
    CREATE TABLE `patients`(
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `patient_id` int(11) NOT NULL,
    `consulted_by` int(11) NOT NULL,
    `pre_examination` json NOT NULL,
    `examinations` json NULL,
    `status` tinyint(4) NOT NULL,
    `created_at` int(11) NOT NULL,
    `updated_at` int(11) NOT NULL,    
    PRIMARY KEY(id),
    FOREIGN KEY(patient_id) REFERENCES persons(id),
    FOREIGN KEY(consulted_by) REFERENCES persons(id)
    )
"""

# lab_requests
lab_requests_object_name = "lab_requests"
lab_requests_object_fields = {"id":"Integer","patient_id":"Integer","requested_by":"Integer","lab_expert":"Integer", "lab_id": "Integer", "lab_result": "String","lab_result_attachment": "String", "status":"Boolean", "created_at":"Integer", "updated_at":"Integer"}
lab_requests_table_schema = """
    CREATE TABLE `lab_requests`(
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `patient_id` int(11) NOT NULL,
    `requested_by` int(11) NOT NULL,
    `lab_expert` int(11) NULL,
    `lab_id` int(11) NOT NULL,
    `lab_result` varchar(255) NULL,
    `lab_result_attachment` varchar(255) NULL,
    `status` tinyint(4) NOT NULL,
    `created_at` int(11) NOT NULL,
    `updated_at` int(11) NOT NULL,    
    PRIMARY KEY(id),
    FOREIGN KEY(patient_id) REFERENCES persons(id),
    FOREIGN KEY(lab_id) REFERENCES labs(id),
    FOREIGN KEY(requested_by) REFERENCES persons(id),
    FOREIGN KEY(lab_expert) REFERENCES persons(id)
    )
"""

# departments
departments_requests_object_name = "departments"
departments_requests_object_fields = {"id":"Integer", "report_to":"Integer", "org_id":"Integer", "name": "String", "status":"Boolean", "created_at":"Integer", "updated_at":"Integer"}
departments_requests_table_schema = """
    CREATE TABLE `departments`(
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `report_to` int(11) DEFAULT NULL,
    `org_id` int(11) NOT NULL,
    `name` varchar(50) NOT NULL,
    `status` tinyint(4) DEFAULT 1,
    `created_at` int(11) NOT NULL,
    `updated_at` int(11) NOT NULL,    
    PRIMARY KEY(id),
    FOREIGN KEY(report_to) REFERENCES departments(id),
    FOREIGN KEY(org_id) REFERENCES organization(id)
    )
"""

# pharmacy
pharmacy_requests_object_name = "pharmacy"
pharmacy_requests_object_fields = {"id":"Integer", "name":"String", "properties":"String", "order_price":"Float", "sell_price": "Float", "expire_date": "String", "status":"Boolean", "created_at":"Integer", "updated_at":"Integer"}
pharmacy_requests_table_schema = """
    CREATE TABLE `pharmacy`(
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `name` varchar(50) NOT NULL,
    `properties` json DEFAULT NULL,
    `order_price` float(11) DEFAULT NULL,
    `sell_price` float(11) DEFAULT NULL,
    `org_id` int(11) NOT NULL,
    `expire_date` varchar(20) NOT NULL,
    `status` tinyint(4) DEFAULT 1,
    `created_at` int(11) NOT NULL,
    `updated_at` int(11) NOT NULL,    
    PRIMARY KEY(id),
    FOREIGN KEY(org_id) REFERENCES organization(id)
    )
"""

# roles
roles_requests_object_name = "roles"
roles_requests_object_fields = {"id":"Integer", "org_id":"Integer", "name":"String", "description":"String", "status":"Boolean", "created_at":"Integer", "updated_at":"Integer"}
roles_requests_table_schema = """
    CREATE TABLE `roles`(
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `org_id` int(11) NOT NULL,
    `name` varchar(50) NOT NULL,
    `description` varchar(50) DEFAULT NULL,
    `status` tinyint(4) DEFAULT 1,
    `created_at` int(11) NOT NULL,
    `updated_at` int(11) NOT NULL,    
    PRIMARY KEY(id),
    FOREIGN KEY(org_id) REFERENCES organization(id)
    )
"""

# roles
role_users_requests_object_name = "role_users"
role_users_requests_object_fields = {"id":"Integer", "role_id":"Integer", "user_id":"integer", "status":"Boolean", "created_at":"Integer", "updated_at":"Integer"}
role_users_requests_table_schema = """
    CREATE TABLE `role_users`(
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `role_id` int(11) NOT NULL,
    `user_id` int(11) NOT NULL,
    `status` tinyint(4) DEFAULT 1,
    `created_at` int(11) NOT NULL,
    `updated_at` int(11) NOT NULL,    
    PRIMARY KEY(id),
    FOREIGN KEY(role_id) REFERENCES roles(id),
    FOREIGN KEY(user_id) REFERENCES users(id)
    )
"""

# roles
expenses_requests_object_name = "office_expenses"
expenses_requests_object_fields = {"id":"Integer", "reason":"String", "price":"integer", "paid_by":"String", "status":"Boolean", "created_at":"Integer", "updated_at":"Integer"}
expenses_requests_table_schema = """
    CREATE TABLE `office_expenses`(
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `reason` varchar(50) NOT NULL,
    `price` int(11) NOT NULL,
    `paid_by` varchar(50) NOT NULL,
    `status` tinyint(4) DEFAULT 1,
    `created_at` int(11) NOT NULL,
    `updated_at` int(11) NOT NULL,    
    PRIMARY KEY(id)
    )
"""

# patient-rooms
patient_room_requests_object_name = "patient_room"
patient_room_requests_object_fields = {"id":"Integer", "person_id":"Integer", "room_id":"integer", "enterance_date":"Integer", "leave_date":"Integer", "status":"Boolean", "created_at":"Integer", "updated_at":"Integer"}
patient_room_requests_table_schema = """
    CREATE TABLE `patient_room`(
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `person_id` int(11) NOT NULL,
    `room_id` int(11) NOT NULL,
    `enterance_date` int(11) NOT NULL,
    `leave_date` int(11),
    `status` tinyint(4) DEFAULT 1,
    `created_at` int(11) NOT NULL,
    `updated_at` int(11) NOT NULL,    
    PRIMARY KEY(id),
    FOREIGN KEY(person_id) REFERENCES persons(id),
    FOREIGN KEY(room_id) REFERENCES rooms(id)
    )
"""

# Employee
employee_requests_object_name = "employees"
employee_requests_object_fields =  {"id":"Integer","org_id":"Integer","first_name": "String", "last_name": "String", "grand_father": "String", "gender": "String", "date_of_birth": "String", "email": "String", "person_type": "String", "prefix": "String",  "profile_image": "String", "status":"Boolean", "created_at":"Integer", "updated_at":"Integer"}
employee_requests_table_schema = """
CREATE TABLE `employees` (
  `id` int(11) NOT NULL,
  `first_name` varchar(50) NOT NULL,
  `last_name` varchar(50) NOT NULL,
  `grand_father` varchar(50) DEFAULT NULL,
  `gender` varchar(5) NOT NULL,
  `date_of_birth` varchar(20) NOT NULL,
  `email` varchar(50) DEFAULT NULL,
  `person_type` varchar(20) NOT NULL,
  `prefix` varchar(10) DEFAULT NULL,
  `profile_image` varchar(200) DEFAULT NULL,
  `org_id` int(11) NOT NULL,
  `created_at` int(11) NOT NULL,
  `updated_at` int(11) NOT NULL,
  `status` tinyint(4) NOT NULL
)
"""

# appointments
appointments_requests_object_name = "appointments"
appointments_requests_object_fields =  {"id":"Integer","appointed_by":"Integer","patient_id": "Integer", "description": "String", "status":"Boolean", "created_at":"Integer", "updated_at":"Integer"}
appointments_requests_table_schema = """
CREATE TABLE `appointments` (
  `id` int(11) NOT NULL,
  `appointed_by` int(11) NOT NULL,
  `patient_id` int(11) NOT NULL,
  `description` varchar(150) DEFAULT NULL,
  `created_at` int(11) NOT NULL,
  `updated_at` int(11) NOT NULL,
  `status` tinyint(4) NOT NULL
)
"""


# # person
# generate(persons_object_name, persons_object_fields)
# create_table(persons_object_name, persons_table_schema, True)

# # buildings
# generate(buildings_object_name, buildings_object_fields)
# create_table(buildings_object_name, buildings_table_schema, True)

# # rooms
# generate(rooms_object_name, rooms_object_fields)
# create_table(rooms_object_name, rooms_table_schema, True)

# # bed_rooms
# generate(bed_rooms_object_name, bed_rooms_object_fields)
# create_table(bed_rooms_object_name, bed_rooms_table_schema, True)

# # service_category
# generate(service_category_object_name, service_category_object_fields)
# create_table(service_category_object_name, service_category_table_schema, True)

# # presecriptions
# generate(prescriptions_object_name, prescriptions_object_fields)
# create_table(prescriptions_object_name, prescriptions_table_schema, True)

# # users
# generate(users_object_name, users_object_fields)
# create_table(users_object_name, users_table_schema, True)

# # lab_groups
# generate(lab_group_object_name, lab_group_object_fields)
# create_table(lab_group_object_name, lab_group_table_schema, True)

# # labs
# generate(labs_object_name, labs_object_fields)
# create_table(labs_object_name, labs_table_schema, True)

# patients
# generate(patients_object_name, patients_object_fields)
# create_table(patients_object_name, patients_table_schema, True)

# # lab_requests
# generate(lab_requests_object_name, lab_requests_object_fields)
# create_table(lab_requests_object_name, lab_requests_table_schema, True)

# departments
# generate(departments_requests_object_name, departments_requests_object_fields)
# create_table(departments_requests_object_name, departments_requests_table_schema, True)

# pharmacy
# create_table(pharmacy_requests_object_name, pharmacy_requests_table_schema, True)
# generate(pharmacy_requests_object_name, pharmacy_requests_object_fields)

# roles
# create_table(roles_requests_object_name, roles_requests_table_schema, True)
# generate(roles_requests_object_name, roles_requests_object_fields)

# role_users
# create_table(role_users_requests_object_name, role_users_requests_table_schema, True)
# generate(role_users_requests_object_name, role_users_requests_object_fields)

# our office expenses
# create_table(expenses_requests_object_name, expenses_requests_table_schema, True)
# generate(expenses_requests_object_name, expenses_requests_object_fields)

# patient_room
# create_table(patient_room_requests_object_name, patient_room_requests_table_schema, True)
# generate(patient_room_requests_object_name, patient_room_requests_object_fields)

# employee
# create_table(employee_requests_object_name, employee_requests_table_schema, True)
# generate(employee_requests_object_name, employee_requests_object_fields)

# Appointments
# create_table(appointments_requests_object_name, appointments_requests_table_schema, True)
# generate(appointments_requests_object_name, appointments_requests_object_fields)