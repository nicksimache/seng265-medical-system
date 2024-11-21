import unittest
from clinic.patient import Patient

class IntegrationTests(unittest.TestCase):
    def setUp(self):
        # Example patients
        self.P1 = Patient(1, "Enrique Brolo", "2005-09-28", "250 946 0239", "enrique.brolo@gmail.com", "799 Glink St, Victoria")
        self.P2 = Patient(2, "Krapetar Prime", "1768-08-28", "256 956 9034", "krapetar.prime@gmail.com", "438 Evabeen St, Victoria")
        self.P3 = Patient(1, "Enrique Brolo", "2005-09-28", "250 946 0239", "enrique.brolo@gmail.com", "799 Glink St, Victoria")  # Same as patient 1
        self.P4 = Patient(1234567890, "", "", "", "", "")  # Patient with empty strings
        self.P5 = Patient(-1, "Ombladon", "1968-03-23", "594 954 5443", "ombladon.business@gmail.com", "5432 Hood St, Bucharest")  # Patient with negative phn

    def test_equality(self):
        # Testing that patients with all fields equal are equal
        self.assertEqual(self.P1, self.P3)
        self.assertNotEqual(self.P1, self.P2)

    def test_empty_string(self):
        # Testing the creation of a patient with empty strings
        self.assertEqual(self.P4.name, "")
        self.assertEqual(self.P4.birth_date, "")
        self.assertEqual(self.P4.phone, "")
        self.assertEqual(self.P4.email, "")
        self.assertEqual(self.P4.address, "")

    def test_negative_phn(self):
        # Testing a patient with a negative phn
        self.assertEqual(self.P5.phn, -1)

    def test_phn_ineq(self):
        # Testing that patients with different phone numbers are not equal
        self.assertNotEqual(self.P1, Patient(55, "Enrique Brolo", "2005-09-28", "250 946 0239", "enrique.brolo@gmail.com", "799 Glink St, Victoria"))

    def test_name_ineq(self):
        # Testing that patients with different names are not equal
        self.assertNotEqual(self.P1, Patient(1, "Breck", "2005-09-28", "250 946 0239", "enrique.brolo@gmail.com", "799 Glink St, Victoria"))

    def test_dob_ineq(self):
        # Testing that patients with different date of birth are not equal
        self.assertNotEqual(self.P1, Patient(1, "Enrique Brolo", "1999-09-13", "250 946 0239", "enrique.brolo@gmail.com", "799 Glink St, Victoria"))

    def test_phonenr_ineq(self):
        # Testing that patients with different phone numbers are not equal
        self.assertNotEqual(self.P1, Patient(1, "Enrique Brolo", "2005-09-28", "778 928 4378", "enrique.brolo@gmail.com", "799 Glink St, Victoria"))

    def test_email_ineq(self):
        # Testing that patients with different emails are not equal
        self.assertNotEqual(self.P1, Patient(1, "Enrique Brolo", "2005-09-28", "250 946 0239", "kumarpatel@gmail.com", "799 Glink St, Victoria"))

    def test_address_ineq(self):
        # Testing that patients with different addresses are not equal
        self.assertNotEqual(self.P1, Patient(1, "Enrique Brolo", "2005-09-28", "250 946 0239", "enrique.brolo@gmail.com", "Bikini Bottom"))

if __name__ == "__main__":
    unittest.main()
