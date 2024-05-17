from flask_restful import fields

roles_fields = {
    'id':fields.Integer,
    'org_id':fields.Integer,
    'name':fields.String,
    'description':fields.String,
    'status':fields.Integer,
    'created_at':fields.Integer,
    'updated_at':fields.Integer,
}

persons_fields = {
	'id':fields.Integer,
	'org_id':fields.Integer,
	'first_name':fields.String,
	'last_name':fields.String,
	'grand_father':fields.String,
	'gender':fields.String,
	'date_of_birth':fields.String,
	'email':fields.String,
	'person_type':fields.String,
	'prefix':fields.String,
	'profile_image':fields.String,
	'status':fields.Integer,
	'created_at':fields.Integer,
	'updated_at':fields.Integer,
}

prescriptions_fields = {
	'person_id':fields.Integer,
	'prescription':fields.String,
	'provided_by':fields.String,
	'approved_pharmacist':fields.String,
	'dosage':fields.String,
	'frequancy':fields.String,
	'no_of_day':fields.String,
	'food_relation':fields.String,
	'instruction':fields.String,
	'status':fields.Integer,
	'created_at':fields.Integer,
	'updated_at':fields.Integer,
}

lab_requests_fields = {
	'id':fields.Integer,
	'patient_id':fields.Integer,
	'requested_by':fields.Integer,
	'lab_expert':fields.Integer,
	'lab_id':fields.Integer,
	'lab_result':fields.String,
	'lab_result_attachment':fields.String,
	'status':fields.Integer,
	'created_at':fields.Integer,
	'updated_at':fields.Integer,

	}
    
patients_fields = {
	'id':fields.Integer,
	'patient_id':fields.Integer,
	'consulted_by':fields.Integer,
	'pre_examination':fields.String,
	'examinations':fields.String,
	'status':fields.Integer,
	'created_at':fields.Integer,
	'updated_at':fields.Integer,

	}

patient_room_fields = {
	'id':fields.Integer,
	'person_id':fields.Integer,
	'room_id':fields.Integer,
	'enterance_date':fields.Integer,
	'leave_date':fields.Integer,
	'status':fields.Integer,
	'created_at':fields.Integer,
	'updated_at':fields.Integer,
}

patients_full_fields = {
	'id':fields.Integer,
	'org_id':fields.Integer,
	'first_name':fields.String,
	'last_name':fields.String,
	'grand_father':fields.String,
	'gender':fields.String,
	'date_of_birth':fields.String,
	'email':fields.String,
	'person_type':fields.String,
	'prefix':fields.String,
	'profile_image':fields.String,
	'status':fields.Integer,
	'created_at':fields.Integer,
	'updated_at':fields.Integer,
	'patient':fields.Nested(patients_fields),
	'prescriptions': fields.Nested(prescriptions_fields),
	'lab':fields.Nested(lab_requests_fields),
	'bed_room':fields.Nested(patient_room_fields)
}

employee_full_fields = {
	'id':fields.Integer,
	'org_id':fields.Integer,
	'first_name':fields.String,
	'last_name':fields.String,
	'grand_father':fields.String,
	'gender':fields.String,
	'date_of_birth':fields.String,
	'email':fields.String,
	'person_type':fields.String,
	'prefix':fields.String,
	'profile_image':fields.String,
	'status':fields.Integer,
	'created_at':fields.Integer,
	'updated_at':fields.Integer,
	'roles':fields.Nested(roles_fields)

}