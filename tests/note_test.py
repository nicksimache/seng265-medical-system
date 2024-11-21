import unittest
from clinic.note import Note

class NoteTest(unittest.TestCase):
    def setUp(self):
        # Create some example notes
        self.N1 = Note(1, "Nick")
        self.N2 = Note(2, "Enrique")
        self.N3 = Note(1, "Nick")  # Same as note 1
        self.N4 = Note(1, "")  # Note with empty string
        self.N5 = Note(-1, "Bob")  # Note with negative code

    def test_eq(self):
        # Testing that notes with same code and message are equal
        self.assertEqual(self.N1, self.N3)
        self.assertNotEqual(self.N1, self.N2)

    def test_code_ineq(self):
        # Testing if notes with different code are not equal
        self.assertNotEqual(self.N1, Note(63, "Nick"))

    def test_msg_ineq(self):
        # Testing if notes with different text are not equal
        self.assertNotEqual(self.N1, Note(1, "Keptin"))

    def test_empty_string(self):
        # Testing note with empty string
        self.assertEqual(self.N4.text, "")

    def test_neg(self):
        # Testing note with a negative code
        self.assertEqual(self.N5.code, -1)

if __name__ == "__main__":
    unittest.main()
