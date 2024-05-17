# HMS
# Evniroment Variables

To run on docker
```
docker build -t bernos-person:latest -f Dockerfile .
docker run --rm -d -p 8000:8000 --name bernos-person-profile bernos-person:latest
```

Postman links
https://www.getpostman.com/collections/4036f220707354393e09

## WEB ENV
SKIP_PREFLIGHT_CHECK=<<boolean>>
REACT_APP_BASENAME= <<>>

JWT_SECRET=mysecret
SALT_CONFIG=password-salt

## DB env
DB_HOST=
DB_USERNAME=
DB_PASSWORD=

### To Build and run the API
``` 
docker build -t hms-app:dev .
docker volume create hms-vol
docker run -p 9000:8000 --mount type=volume,src=hms-vol,dst=/data --mount type=bind,source=D:/bernos/HMS,target=/user/src/app --rm  --name hms-app-container hms-app:dev 
```
docker run -d -p 9000:8000 --mount type=volume,src=hms-vol, dst=/data  --mount type=bind,source=D:\vv-project\export-files-mine,target=/import-folder --rm --name hms-emulator hms-app:dev


# APIs
## Patients API endpoints
- Verb - POST/GET - /persons to GET all and add new persons.  For the get method we can use query parm ?status={a single value or a comma separated value}
- Verb - GET/PUT/DELETE: /persons/<int:id> to get, delete and update a single person basic information
- Verb - GET: /persons/<int:id>/patient-details to get a single patient details

## Employee API endpoints
- Verb - POST/GET - /employees to GET all and add new persons 
- Veerb - GET/PUT/DELETE: /employees/<int:id> to get, delete and update a single person basic information
- Verb - GET -/employees/<int:id>/employee-details to get a single employee details

## Buildings API endpoints
- Verb - POST/GET - /buildings to GET all and add new building
- Veerb - GET/PUT/DELETE: /buildings/<int:id> to get, delete and update a single building basic information

## Organizations API endpoints
- Verb - POST/GET - /organizations to GET all and add new organization
- Veerb - GET/PUT/DELETE: /organizations/<int:id> to get, delete and update a single organization basic information

## Diagnosis API endpoints
- Verb - POST - /persons/<int:id>/diagnosis to add new diagnosis 
- Veerb - PUT/DELETE: /persons/<int:id>/diagnosis/<int:pid> delete and update a single diagnosis

## Lab Group API endpoints
- Verb - POST/GET - /lab-groups to GET all and add new lab-groups 
- Veerb - GET/PUT/DELETE: /lab-groups/<int:id> to get, delete and update a single lab-groups information

## Lab API endpoints
- Verb - POST/GET - /labs to GET all and add new lab 
- Veerb - GET/PUT/DELETE: /labs/<int:id> to get, delete and update a single lab information

## Lab Request API endpoints
- Verb - POST - /persons/<int:id>/lab-requests to add new lab-requests 
- Veerb - PUT/DELETE: /persons/<int:id>/lab-requests/<int:id> to delete and update a single lab-requests information

## Presecription API endpoints
- Verb - POST - /persons/<int:id>/prescriptions to add new prescription
- Veerb - PUT/DELETE: /persons/<int:id>/prescriptions/<int:id> to delete and update a single prescription information

## Appointments API endpoints
- Verb - POST - /persons/<int:id>/appointments to add new prescription
- Veerb - PUT/DELETE: /persons/<int:id>/appointments/<int:id> to delete and update a single prescription information