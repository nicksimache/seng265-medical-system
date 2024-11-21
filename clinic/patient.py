from clinic.patient_record import PatientRecord
"""Patient class represents a patient and holds a PatientRecord for each patient"""

class Patient:
    def __init__(self, phn, name, birth_date, phone, email, address):
        self.phn = phn
        self.name = name
        self.birth_date = birth_date
        self.phone = phone
        self.email = email
        self.address = address
        self.record = PatientRecord()

    """ensures that when two patients are compared they check all variables to see if they are the same"""
    def __eq__(self, other):
        if (self.phn == other.phn and 
            self.name == other.name and 
            self.birth_date == other.birth_date and 
            self.phone == other.phone and 
            self.email == other.email and 
            self.address == other.address):
            return True
        return False

    """getName returns the name of the patient"""
    def getName(self):
        return self.name
