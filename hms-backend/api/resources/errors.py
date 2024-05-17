from werkzeug.exceptions import HTTPException

class PersonNotFoundError(HTTPException):
    """Class to handle error if Person Id not found 
    Attributes:
        status_code: Error status code.
        message: Error message.
        response: Contains status, message and status code.
    """
    def __init__(self):
        """Inits PersonNotFoundError class."""
        self.status_code = 404
        self.message = "Please check the Person ID"
        self.status = "error"
        self.response = ({'status': self.status,'message': self.message},self.status_code)

class OrganizationNotFoundError(HTTPException):
	def __init__(self):
		self.status_code = 404
		self.message = 'Please check the organization ID'
		self.status = 'error'
		self.response = ({'status': self.status,'message': self.message},self.status_code)

class BuildingNotFoundError(HTTPException):
	def __init__(self):
		self.status_code = 404
		self.message = 'Please check the building ID'
		self.status = 'error'
		self.response = ({'status': self.status,'message': self.message},self.status_code)


class Bed_roomsNotFoundError(HTTPException):
	def __init__(self):
		self.status_code = 404
		self.message = 'Please check the bed_rooms ID'
		self.status = 'error'
		self.response = ({'status': self.status,'message': self.message},self.status_code)


class Bed_roomsNotFoundError(HTTPException):
	def __init__(self):
		self.status_code = 404
		self.message = 'Please check the bed_rooms ID'
		self.status = 'error'
		self.response = ({'status': self.status,'message': self.message},self.status_code)


class Service_categoryNotFoundError(HTTPException):
	def __init__(self):
		self.status_code = 404
		self.message = 'Please check the service_category ID'
		self.status = 'error'
		self.response = ({'status': self.status,'message': self.message},self.status_code)

class OfficeNotFoundError(HTTPException):
	def __init__(self):
		self.status_code = 404
		self.message = 'Please check the service_category ID'
		self.status = 'error'
		self.response = ({'status': self.status,'message': self.message},self.status_code)




class PrescriptionsNotFoundError(HTTPException):
	def __init__(self):
		self.status_code = 404
		self.message = 'Please check Person ID or prescriptions ID is correct or presecription is not Deleted'
		self.status = 'error'
		self.response = ({'status': self.status,'message': self.message},self.status_code)


class UsersNotFoundError(HTTPException):
	def __init__(self):
		self.status_code = 404
		self.message = 'Please check the users ID'
		self.status = 'error'
		self.response = ({'status': self.status,'message': self.message},self.status_code)


class Lab_groupNotFoundError(HTTPException):
	def __init__(self):
		self.status_code = 404
		self.message = 'Please check the lab_group ID'
		self.status = 'error'
		self.response = ({'status': self.status,'message': self.message},self.status_code)


class Lab_groupNotFoundError(HTTPException):
	def __init__(self):
		self.status_code = 404
		self.message = 'Please check the lab_group ID'
		self.status = 'error'
		self.response = ({'status': self.status,'message': self.message},self.status_code)


class Lab_groupNotFoundError(HTTPException):
	def __init__(self):
		self.status_code = 404
		self.message = 'Please check the lab_group ID'
		self.status = 'error'
		self.response = ({'status': self.status,'message': self.message},self.status_code)


class LabsNotFoundError(HTTPException):
	def __init__(self):
		self.status_code = 404
		self.message = 'Please check the labs ID'
		self.status = 'error'
		self.response = ({'status': self.status,'message': self.message},self.status_code)


class PersonsNotFoundError(HTTPException):
	def __init__(self):
		self.status_code = 404
		self.message = 'Please check the persons ID'
		self.status = 'error'
		self.response = ({'status': self.status,'message': self.message},self.status_code)


class PersonsNotFoundError(HTTPException):
	def __init__(self):
		self.status_code = 404
		self.message = 'Please check the persons ID'
		self.status = 'error'
		self.response = ({'status': self.status,'message': self.message},self.status_code)


class PatientsNotFoundError(HTTPException):
	def __init__(self):
		self.status_code = 404
		self.message = 'Please check the patients ID'
		self.status = 'error'
		self.response = ({'status': self.status,'message': self.message},self.status_code)


class Lab_requestsNotFoundError(HTTPException):
	def __init__(self):
		self.status_code = 404
		self.message = 'Please check the lab_requests ID'
		self.status = 'error'
		self.response = ({'status': self.status,'message': self.message},self.status_code)


class PatientsNotFoundError(HTTPException):
	def __init__(self):
		self.status_code = 404
		self.message = 'Please check the patients ID'
		self.status = 'error'
		self.response = ({'status': self.status,'message': self.message},self.status_code)


class Lab_requestsNotFoundError(HTTPException):
	def __init__(self):
		self.status_code = 404
		self.message = 'Please check the lab_requests ID or Person ID is correct or Lab request is not deleted'
		self.status = 'error'
		self.response = ({'status': self.status,'message': self.message},self.status_code)


class PatientsNotFoundError(HTTPException):
	def __init__(self):
		self.status_code = 404
		self.message = 'Please check the patients ID'
		self.status = 'error'
		self.response = ({'status': self.status,'message': self.message},self.status_code)


class BuildingsNotFoundError(HTTPException):
	def __init__(self):
		self.status_code = 404
		self.message = 'Please check the buildings ID'
		self.status = 'error'
		self.response = ({'status': self.status,'message': self.message},self.status_code)


class RoomsNotFoundError(HTTPException):
	def __init__(self):
		self.status_code = 404
		self.message = 'Please check the rooms ID'
		self.status = 'error'
		self.response = ({'status': self.status,'message': self.message},self.status_code)


class Bed_roomsNotFoundError(HTTPException):
	def __init__(self):
		self.status_code = 404
		self.message = 'Please check the bed_rooms ID'
		self.status = 'error'
		self.response = ({'status': self.status,'message': self.message},self.status_code)


class DepartmentsNotFoundError(HTTPException):
	def __init__(self):
		self.status_code = 404
		self.message = 'Please check the departments ID'
		self.status = 'error'
		self.response = ({'status': self.status,'message': self.message},self.status_code)


class PharmacyNotFoundError(HTTPException):
	def __init__(self):
		self.status_code = 404
		self.message = 'Please check the pharmacy ID'
		self.status = 'error'
		self.response = ({'status': self.status,'message': self.message},self.status_code)
class UsersNotFoundError(HTTPException):
	def __init__(self):
		self.status_code = 401
		self.message = 'Please check Username or Password is correct'
		self.status = 'error'
		self.response = ({'status': self.status,'message': self.message},self.status_code)

class RolesNotFoundError(HTTPException):
	def __init__(self):
		self.status_code = 404
		self.message = 'Please check the roles ID'
		self.status = 'error'
		self.response = ({'status': self.status,'message': self.message},self.status_code)

class Role_usersNotFoundError(HTTPException):
	def __init__(self):
		self.status_code = 404
		self.message = 'Please check the role_users ID'
		self.status = 'error'
		self.response = ({'status': self.status,'message': self.message},self.status_code)


class Office_expensesNotFoundError(HTTPException):
	def __init__(self):
		self.status_code = 404
		self.message = 'Please check the office_expenses ID'
		self.status = 'error'
		self.response = ({'status': self.status,'message': self.message},self.status_code)


class Patient_roomNotFoundError(HTTPException):
	def __init__(self):
		self.status_code = 404
		self.message = 'Please check the patient_room ID'
		self.status = 'error'
		self.response = ({'status': self.status,'message': self.message},self.status_code)


class EmployeesNotFoundError(HTTPException):
	def __init__(self):
		self.status_code = 404
		self.message = 'Please check the employees ID'
		self.status = 'error'
		self.response = ({'status': self.status,'message': self.message},self.status_code)


class EmployeesNotFoundError(HTTPException):
	def __init__(self):
		self.status_code = 404
		self.message = 'Please check the employees ID'
		self.status = 'error'
		self.response = ({'status': self.status,'message': self.message},self.status_code)


class AppointmentsNotFoundError(HTTPException):
	def __init__(self):
		self.status_code = 404
		self.message = 'Please check the appointments ID'
		self.status = 'error'
		self.response = ({'status': self.status,'message': self.message},self.status_code)

class UserAlreadyFoundError(HTTPException):
	def __init__(self):
		self.status_code = 404
		self.message = 'This Employee already have an account. You can update if it is disabled'
		self.status = 'error'
		self.response = ({'status': self.status,'message': self.message},self.status_code)


class UserNameFoundError(HTTPException):
	def __init__(self):
		self.status_code = 404
		self.message = 'Select a different username. This username already taken'
		self.status = 'error'
		self.response = ({'status': self.status,'message': self.message},self.status_code)