import json
import os
from clinic.dao.patient_dao import PatientDAO
from clinic.patient import Patient
from clinic.exception.duplicate_login_exception import DuplicateLoginException
from clinic.exception.illegal_access_exception import IllegalAccessException
from clinic.exception.illegal_operation_exception import IllegalOperationException
from clinic.exception.invalid_login_exception import InvalidLoginException
from clinic.exception.invalid_logout_exception import InvalidLogoutException
from clinic.exception.no_current_patient_exception import NoCurrentPatientException
from clinic.dao.patient_decoder import PatientDecoder
from clinic.dao.patient_encoder import PatientEncoder

class PatientDAOJSON(PatientDAO):
    def __init__(self, autosave=True):
        self.patients = {}
        self.autosave = autosave

        if self.autosave:
            self.load_patients()

    """Decodes the JSON file and saves the patient data in a dictionary"""
    def load_patients(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(current_dir, "../records/patients.json")
        try:
            with open(file_path, "r") as file:
                patients_list = json.load(file, cls=PatientDecoder)
                self.patients = {p.phn: p for p in patients_list}
        except (FileNotFoundError, json.JSONDecodeError):
            self.patients = {}

    """Stores the current patient list in the json file"""
    def save_patients(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(current_dir, "../records/patients.json")
        if self.autosave:
            with open(file_path, "w") as file:
                json.dump(list(self.patients.values()), file, cls=PatientEncoder)

    """Creates a new patient given that the phn doesnt match an already existing patient"""
    def create_patient(self, phn, name, birth_date, phone, email, address):
        if phn in self.patients:
            raise IllegalOperationException
        new_patient = Patient(phn, name, birth_date, phone, email, address)
        self.patients[phn] = new_patient
        if self.autosave:
            self.save_patients()
        return new_patient

    """Searches for a patient given a phn, returns None if noone found"""
    def search_patient(self, phn):
        return self.patients.get(phn, None)

    """Returns a list of all patients with names matching the given input"""
    def retrieve_patients(self, name):
        return [patient for patient in self.patients.values() if name in patient.getName()]

    """Updates all of a patients data given input"""
    def update_patient(self, oldphn, phn, name, birth_date, phone, email, address):
        if (oldphn != phn and phn in self.patients) or oldphn not in self.patients:
            raise IllegalOperationException

        self.patients.pop(oldphn)
        new_patient_data = Patient(phn, name, birth_date, phone, email, address)
        self.patients[phn] = new_patient_data
        if self.autosave:
            self.save_patients()
        return True

    """Deletes a patient given that they exist in the database"""
    def delete_patient(self, phn):
        if phn not in self.patients:
            raise IllegalOperationException
        self.patients.pop(phn)
        if self.autosave:
            self.save_patients()
        return True

    """Returns a list of all patients"""
    def list_patients(self):
        return list(self.patients.values())
