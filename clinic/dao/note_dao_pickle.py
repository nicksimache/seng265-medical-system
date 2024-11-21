from clinic.dao.note_dao import NoteDAO
from clinic.note import Note

class NoteDAOPickle(NoteDAO):
    def __init__(self):
        self.autocounter = 0
        self.notes = []

    def search_note(self, key):
        for note in self.notes:
            if(note.code == key):
                return note
        return None
    
    def create_note(self, text):
        self.autocounter += 1
        new_note = Note(self.autocounter, text)
        self.notes.append(new_note)
        return new_note
    
    def retrieve_notes(self, search_string):
        list = []
        for note in self.notes:
            if(search_string in note.text):
                list.append(note)
        return list
   
    def update_note(self, key, text):
        for note in self.notes:
            if(note.code == key):
                note.change_text(text)
   
    def delete_note(self, key):
        for note in self.notes:
            if(note.code == key):
                self.notes.remove(note)

    def list_notes(self):
        list = []
        for i in range(len(self.notes)):
            list.append(self.notes[len(self.notes) - 1 - i])
        return list
