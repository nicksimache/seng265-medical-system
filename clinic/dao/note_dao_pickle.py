import pickle
import datetime
from clinic.note import Note
from clinic.dao.note_dao import NoteDAO
from clinic.exception.illegal_operation_exception import IllegalOperationException
import os

class NoteDAOPickle(NoteDAO):
    def __init__(self, phn, autosave=False):
        self.autocounter = 0
        self.phn = phn
        self.notes = []
        self.autosave = autosave
        self.file_name = os.path.join("clinic", "records", f"{self.phn}.dat")

        if self.autosave:
            self.load_notes()
        
    '''decodes and stores notes from the patients .dat file'''
    def load_notes(self):
        try:
            with open(self.file_name, 'rb') as file:
                self.notes = pickle.load(file)
                if self.notes:
                    self.autocounter =  max(note.code for note in self.notes)  # This sets autocounter to the highest code in notes
                else:
                    self.autocounter = 0
        except FileNotFoundError:
            self.notes = []
            self.autocounter = 0
        except Exception as e:
            self.notes = []
            self.autocounter = 0

    """Save notes to the binary file."""
    def save_notes(self):
        if self.autosave:
            os.makedirs(os.path.dirname(self.file_name), exist_ok=True)
            with open(self.file_name, "wb") as file:
                pickle.dump(self.notes, file)
            
    """Search for a note based on a specific key"""
    def search_note(self, key):
        return next((note for note in self.notes if note.code == key), None)

  
    """Create a note given text"""
    def create_note(self, text):
        self.autocounter += 1
        new_note = Note(self.autocounter, text)
        self.notes.append(new_note)
        if self.autosave:
            self.save_notes()
        return new_note
    
    """Retrieves all notes with text that contains a given input string"""
    def retrieve_notes(self, search_string):
        list = []
        """Loops through all notes to find search_string"""
        for note in self.notes:
            if(search_string in note.text):
                list.append(note)
        return list
    
    """Finds the note that matches the given key and updates its text"""
    def update_note(self, key, text):
        for note in self.notes:
            if(note.code == key):
                note.change_text(text)
                self.save_notes()
                note.timestamp = datetime.datetime.now()
                return True
        return False

    """Deletes a note with a specific key given that it exists"""
    def delete_note(self, key):
        note = self.search_note(key)
        if note:
            self.notes.remove(note)
            if self.autosave:
                self.save_notes()
            return True
        return False

    """Returns an array of all notes starting from the note with the highest code"""
    def list_notes(self):
        list = []
        for i in range(len(self.notes)):
            list.append(self.notes[len(self.notes) - 1 - i])
        return list