import unittest
from src.modules.user_management import check_login

class TestIntegration(unittest.TestCase):
    def test_login(self):
        # Beispielhafter Test, ob Login funktioniert
        role = check_login("Bürger", "Passwort")
        self.assertEqual(role, "Bürger")

if __name__ == '__main__':
    unittest.main()