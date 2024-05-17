import os
from flask import Flask, jsonify, request, make_response
from flask.globals import request
from flask.helpers import make_response
from flask_restful import  Api
from flask_cors import CORS
from resources import cache, cache2

from resources.service_category import Service_category, Service_categoryList
from resources.prescriptions import Prescriptions, PrescriptionsList
from resources.office import Office, OfficeList
from resources.persons import Persons, PersonsList, patientDetail
from resources.employees import Employees, EmployeesList, EmployeDetails
from resources.organization import Organization, OrganizationList
from resources.buildings import Buildings, BuildingsList
from resources.bed_rooms import Bed_rooms, Bed_roomsList
from resources.rooms import Rooms, RoomsList
from resources.errors import PersonNotFoundError
from resources.users import UserLogin, Users#, UsersList
from resources.lab_group import Lab_group, Lab_groupList
from resources.labs import Labs, LabsList
from resources.departments import Departments, DepartmentsList
from resources.patients import Patients, PatientsList
from resources.lab_requests import Lab_requests, Lab_requestsList
from resources.pharmacy import Pharmacy, PharmacyList, PharmacyListPetient
from resources.roles import Roles, RolesList
from resources.role_users import Role_users, Role_usersList
from resources.office_expenses import Office_expenses, Office_expensesList
from resources.patient_room import Patient_room, Patient_roomList
from resources.update_table import UpdateTable
from resources.appointments import AppointmentsList, Appointments

from flask_jwt_extended import JWTManager
from common.auth import *
from flask_jwt_extended import jwt_required


JWT_SECRET = os.getenv("JWT_SECRET")

app = Flask(__name__)
# Setup the Flask-JWT-Extended extension
app.config["JWT_SECRET_KEY"] = JWT_SECRET
jwt = JWTManager(app)

app.config['BUNDLE_ERRORS'] = True 
app.config['SECRET_KEY'] = 'thisisthesecretkey'
errors=[PersonNotFoundError]

api = Api(app,errors=errors)

cors = CORS(app, resources={r"/*": {"origins": "*"}})

cache.init_app(app)
cache2.init_app(app)

# patients API endpoints
api.add_resource(Persons, '/persons/<int:id>')
api.add_resource(PersonsList, '/persons')
api.add_resource(patientDetail, '/persons/<int:id>/patient-details')

# Employees API endpoints
api.add_resource(Employees, '/employees/<int:id>')
api.add_resource(EmployeesList, '/employees')
api.add_resource(EmployeDetails, '/employees/<int:id>/employee-details')


# organisation API endpoints
api.add_resource(Organization, '/organizations/<int:id>')
api.add_resource(OrganizationList, '/organizations')

# Buildings API endpoints
api.add_resource(Buildings, '/buildings/<int:id>')
api.add_resource(BuildingsList, '/buildings')

# diagnosis API endpoints
api.add_resource(Patients, '/persons/<int:id>/diagnosis/<int:pid>')
api.add_resource(PatientsList, '/persons/<int:id>/diagnosis')

# Lab group API endpoints
api.add_resource(Lab_group, '/lab-groups/<int:id>')
api.add_resource(Lab_groupList, '/lab-groups')

# Lab API endpoints
api.add_resource(Labs, '/labs/<int:id>')
api.add_resource(LabsList, '/labs')

# lab request API endpoints
api.add_resource(Lab_requests, '/persons/<int:id>/lab-requests/<int:lid>')
api.add_resource(Lab_requestsList, '/persons/<int:id>/lab-requests')

# Presecription API endpoints
api.add_resource(Prescriptions, '/persons/<int:id>/prescriptions/<int:pid>')
api.add_resource(PrescriptionsList, '/persons/<int:id>/prescriptions')

# Appointments API endpoints
api.add_resource(Appointments, '/persons/<int:id>/appointments/<int:aid>')
api.add_resource(AppointmentsList, '/persons/<int:id>/appointments')

# Users API endpoints
api.add_resource(Users, '/employees/<int:id>/users')
# api.add_resource(UsersList, '/users')
api.add_resource(UserLogin, '/users/login')

# Role API endpoints
api.add_resource(Roles, '/roles/<int:id>')
api.add_resource(RolesList, '/roles')

# Role user endpoints
api.add_resource(Role_users, '/role-users/<int:id>')
api.add_resource(Role_usersList, '/role-users')

# Pharmacy API endpoints
api.add_resource(Pharmacy, '/pharmacy/<int:id>')
api.add_resource(PharmacyList, '/pharmacy') 

## This api added by mule on 2022-08-27
api.add_resource(PharmacyListPetient, '/order/<string:name>/pharmacy') 

api.add_resource(Bed_rooms, '/bed-rooms/<int:id>')
api.add_resource(Bed_roomsList, '/bed-rooms')

api.add_resource(Office, '/offices/<int:id>')
api.add_resource(OfficeList, '/offices')

api.add_resource(Service_category, '/service-categories/<int:id>')
api.add_resource(Service_categoryList, '/service-categories')





api.add_resource(Departments, '/departments/<int:id>')
api.add_resource(DepartmentsList, '/departments')



api.add_resource(Rooms, '/rooms/<int:id>')
api.add_resource(RoomsList, '/rooms')






api.add_resource(Office_expenses, '/office-expenses/<int:id>')
api.add_resource(Office_expensesList, '/office-expenses')

api.add_resource(Patient_room, '/persons/<int:id>/patient-rooms/<int:rid>')
api.add_resource(Patient_roomList, '/persons/<int:id>/patient-rooms')
api.add_resource(UpdateTable, '/update')


@app.route('/')
def health_check():
    return 'ok'

@app.route("/doctor-role", methods=["GET"])
@doctor_required()
def doctor_role():
    return jsonify(foo="bar")

@app.route("/admin-role", methods=["GET"])
@admin_required()
def admin():
    return jsonify(foo="bar")

@app.route("/protected", methods=["GET"])
@jwt_required() #check logged in
def protected():
    return jsonify(foo="logged in")

if __name__ == '__main__':
    app.run(host='localhost', debug=True, port=9000)
