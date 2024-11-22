import datetime
from clinic.note import Note
from clinic.dao.note_dao_pickle import NoteDAOPickle

class PatientRecord():
    def __init__(self, phn, autosave=False):
        self.phn = phn
        self.autosave = autosave
        self.notes = NoteDAOPickle(phn, autosave)

    """add_note creates a new note object and adds it into the notes array"""
    def add_note(self, text):
        return self.notes.create_note(text)

    """delete_note removes a note from notes based off of the note's code"""
    def delete_note(self, num):
        self.notes.delete_note(num)

    """code_not_in_notes searches for a code and if it is, then returns false; if not, returns true"""
    def code_not_in_notes(self, num):
        if(self.notes.search_note(num) is None):
            return True
        return False