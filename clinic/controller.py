from clinic.patient import Patient
from clinic.note import Note
from clinic.exception.duplicate_login_exception import DuplicateLoginException
from clinic.exception.illegal_access_exception import IllegalAccessException
from clinic.exception.illegal_operation_exception import IllegalOperationException
from clinic.exception.invalid_login_exception import InvalidLoginException
from clinic.exception.invalid_logout_exception import InvalidLogoutException
from clinic.exception.no_current_patient_exception import NoCurrentPatientException

from clinic.dao.patient_dao_json import PatientDAOJSON

import hashlib
import os

"""Controller class handles operations for Patient, PatientRecord and None classes"""

class Controller:

    def __init__(self, autosave):
        self.status = False
        self.users = {}

        """if autosave is turned on then we retrieve the user data from the users.txt"""
        """if autosave is turned off then we just hardcode it"""
        if autosave:

            current_dir = os.path.dirname(os.path.abspath(__file__))
            file_path = os.path.join(current_dir, "users.txt")
            with open(file_path, "r") as file:
                for line in file:
                    parts = line.strip().split(",")
                    self.users[parts[0]] = parts[1]
        else:
            self.users = {"user":"8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92", 
                          "ali" : "6394ffec21517605c1b426d43e6fa7eb0cff606ded9c2956821c2c36bfee2810", 
                          "kala" : "e5268ad137eec951a48a5e5da52558c7727aaa537c8b308b5e403e6b434e036e"}

        self.patients = PatientDAOJSON()
        self.current_login = None
        self.current_patient = None
        self.autosave = autosave

    """logout function logs the user out (ensures someone is logged in first)"""
    def logout(self):
        if(self.status != False):
            self.status = False
            self.current_login = None
            return True
        raise InvalidLogoutException

    """login function logs the user in"""
    def login(self, username, password):
        # checks to see if username exists, then sees if passwords match
        if(username in self.users):
            if(self.users[username] == hashlib.sha256(password.encode()).hexdigest()):
                if(self.status == False):
                    self.status = True
                    self.current_login = username
                    return True
                else:
                    raise DuplicateLoginException
            else:
                raise InvalidLoginException
        else:
            raise InvalidLoginException
    """create_patient uses the Patient class to create a new patient and stores it in the patients dictionary (returns the patient created)"""
    def create_patient(self, phn, name, birth_date, phone, email, address):
        
        # ensures that the user is logged in and there is not already a patient with the same health number
        if(self.status == False):
            raise IllegalAccessException
        return self.patients.create_patient(phn, name, birth_date, phone, email, address)

    """search_patient finds a patient based on their personal health number (returns found patient or none)"""
    def search_patient(self, id):
        if(self.status == True):
            return self.patients.search_patient(id)
        else:
            raise IllegalAccessException

    """retrieve_patients returns a list with all the patients with a certain name"""
    def retrieve_patients(self, name):
        if(self.status == False):
            raise IllegalAccessException
        return self.patients.retrieve_patients(name)

    """update_patient updates the values of the patient (given by their old health number)"""
    def update_patient(self, oldphn, phn, name, birth_date, phone, email, address):
        if (self.status == False):
            raise IllegalAccessException
        if(self.current_patient is not None):
            if(self.current_patient is self.patients.search_patient(oldphn)):
                raise IllegalOperationException
        return self.patients.update_patient(oldphn, phn, name, birth_date, phone, email, address)

    """delete_patient deletes a patient given by their health number"""
    def delete_patient(self, phn):
        if(self.status == False):
            raise IllegalAccessException
        if(self.current_patient is not None):
            if(self.patients.search_patient(phn) is self.current_patient):
                raise IllegalOperationException
        return self.patients.delete_patient(phn)


    """list_patients returns array with all patients"""
    def list_patients(self):
        if(self.status == False):
            raise IllegalAccessException
        return self.patients.list_patients()

    """set_current_patient sets the current patient based off their health number"""
    def set_current_patient(self, phn):
        # must be logged in and health number must be in patients dictionary
        if(self.status == False):
            raise IllegalAccessException
        
        patient_obj = self.patients.search_patient(phn)

        if(patient_obj is not None):
            self.current_patient = patient_obj
        else:
            raise IllegalOperationException

    """get_current_patient returns the current patient (must be logged in)"""
    def get_current_patient(self):
        if(self.status == False):
            raise IllegalAccessException
        return self.current_patient

    """unset_current_patient sets the current patient to None (must be logged in)"""
    def unset_current_patient(self):
        if(self.status == False):
            raise IllegalAccessException
        self.current_patient = None

    """create_note adds a note to the current patient's record"""
    def create_note(self, text):
        # must be logged in and there must be a current patient
        if(self.status == False):
            raise IllegalAccessException
        elif(self.current_patient is None):
            raise NoCurrentPatientException
        return self.current_patient.record.add_note(text)

    """search_note finds a certain note that is attached to the current patient's record"""
    def search_note(self, num):
        # ensures that user is logged in, current patient exists and the code of the note exists
        if(self.status == False):
            raise IllegalAccessException
        elif(self.current_patient is None):
            raise NoCurrentPatientException
        elif(self.current_patient.record.code_not_in_notes(num)):
            return None
        return self.current_patient.record.notes.search_note(num)

    """retrieve_notes returns all notes as an array that include a certain phrase (text)"""
    def retrieve_notes(self, text):
        # must be logged in and current patient must exist
        if(self.status == False):
            raise IllegalAccessException
        elif(self.current_patient is None):
            raise NoCurrentPatientException
        return self.current_patient.record.notes.retrieve_notes(text)

    """update_note updates the writing of a note which is found from the note's code"""
    def update_note(self, num, text):
        # ensures that user is logged in, current patient exists and the code of the note exists
        if(self.status == False):
            raise IllegalAccessException
        elif(self.current_patient is None):
            raise NoCurrentPatientException
        elif(self.current_patient.record.code_not_in_notes(num)):
            return None
        self.current_patient.record.notes.update_note(num, text)
        return True

    """delete_note removes a note attached to the current patient's record based on its code"""
    def delete_note(self, num):
        # ensures that user is logged in, current patient exists and the code of the note exists
        if(self.status == False):
            raise IllegalAccessException
        elif(self.current_patient is None):
            raise NoCurrentPatientException
        elif(self.current_patient.record.code_not_in_notes(num)):
            return None
        self.current_patient.record.delete_note(num)
        return True

    """list_notes lists all the current patient's notes in reverse order that they were added"""
    def list_notes(self):
        if(self.status == False):
            raise IllegalAccessException
        elif(self.current_patient is None):
            raise NoCurrentPatientException
        return self.current_patient.record.notes.list_notes()
