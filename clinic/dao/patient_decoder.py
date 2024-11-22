import json
from clinic.patient import Patient

class PatientDecoder(json.JSONDecoder):
    def __init__(self, *args, **kwargs):
        super().__init__(object_hook=self.object_hook, *args, **kwargs)

    """Returns a Patient object from the given json file"""
    def object_hook(self, obj):
        if "phn" in obj and "name" in obj:
            return Patient(
                obj["phn"],
                obj["name"], 
                obj["birth_date"], 
                obj["phone"], 
                obj["email"], 
                obj["address"], 
                autosave=True
            )
        return obj