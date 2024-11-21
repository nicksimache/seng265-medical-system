from clinic.dao.patient_dao import PatientDAO
from clinic.patient import Patient
from clinic.exception.duplicate_login_exception import DuplicateLoginException
from clinic.exception.illegal_access_exception import IllegalAccessException
from clinic.exception.illegal_operation_exception import IllegalOperationException
from clinic.exception.invalid_login_exception import InvalidLoginException
from clinic.exception.invalid_logout_exception import InvalidLogoutException
from clinic.exception.no_current_patient_exception import NoCurrentPatientException

class PatientDAOJSON(PatientDAO):
    def __init__(self):
        self.patients = {}

    """create_patient uses the Patient class to create a new patient and stores it in the patients dictionary (returns the patient created)"""
    def create_patient(self, phn, name, birth_date, phone, email, address):
        if(phn in self.patients):
            raise IllegalOperationException
        new_patient = Patient(phn, name, birth_date, phone, email, address)
        self.patients[phn] = new_patient
        return new_patient

    """search_patient finds a patient based on their personal health number (returns found patient or none)"""
    def search_patient(self, id):
        if(id in self.patients):
                return self.patients[id]

    """retrieve_patients returns a list with all the patients with a certain name"""
    def retrieve_patients(self, name):
        found = []

        # loops through all elements in patients dictionary and finds patients with matching name
        for key in self.patients:
            if(name in self.patients[key].getName()):
                found.append(self.patients[key])
        return found

    """update_patient updates the values of the patient (given by their old health number)"""
    def update_patient(self, oldphn, phn, name, birth_date, phone, email, address):
        if((oldphn != phn and phn in self.patients) or oldphn not in self.patients):
            raise IllegalOperationException
        
        # deletes old patient data from patients and creates new Patient object with new data and adds it to the dictionary
        self.patients.pop(oldphn)
        new_patient_data = Patient(phn, name, birth_date, phone, email, address)
        self.patients[phn] = new_patient_data
        return True

    """delete_patient deletes a patient given by their health number"""
    def delete_patient(self, phn):
        # ensures that user is logged in and patient exists
        if(phn not in self.patients):
            raise IllegalOperationException
        self.patients.pop(phn)
        return True

    """list_patients returns array with all patients"""
    def list_patients(self):
        list = []
        for key in self.patients:
            list.append(self.patients[key])
        return list