import unittest
from clinic.patient_record import PatientRecord
from clinic.note import Note

class PatientRecordTest(unittest.TestCase):

    def setUp(self):
        # Create a new patient record for testing
        self.record = PatientRecord()

    def test_add_note(self):
        # Tests if adding notes increments the autocounter correctly and that the note is added
        note1 = self.record.add_note("Right Nick")
        self.assertEqual(self.record.autocounter, 1)

        note2 = self.record.add_note("Faded by Carter")
        self.assertEqual(self.record.autocounter, 2)

        self.assertEqual(note1.code, 1)
        self.assertEqual(note1.text, "Right Nick")
        self.assertEqual(note2.code, 2)
        self.assertEqual(note2.text, "Faded by Carter")

    def test_add_empty_string_note(self):
        # Tests if we can add a note with no text
        note = self.record.add_note("")
        self.assertEqual(note.code, 1)
        self.assertEqual(note.text, "")

    def test_search(self):
        # Tests whether we can find a note in an empty record
        search = self.record.code_not_in_notes(1)
        self.assertTrue(search)

        # Tests whether we can search for a note with a valid code
        self.record.add_note("Michael has 1 month to live")
        search = self.record.code_not_in_notes(1)
        self.assertFalse(search)

        # We also test whether searching for a note with an invalid code does not work
        search = self.record.code_not_in_notes(2)
        self.assertTrue(search)

    def test_delete_note(self):
        # Tests whether after we remove the note, it cannot be found in the record
        self.record.delete_note(1)

        self.record.add_note("Delete this note fam")
        self.record.delete_note(2)

        # Tests deleting a note with a valid code
        self.record.delete_note(1)
        search = self.record.code_not_in_notes(1)
        self.assertTrue(search)

if __name__ == "__main__":
    unittest.main()
