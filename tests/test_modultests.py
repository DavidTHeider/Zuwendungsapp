import unittest
from src.modules.forms import convert_dates

class TestForms(unittest.TestCase):
    def test_convert_dates(self):
        import datetime
        data = {"datum": datetime.date(2025, 1, 1)}
        converted = convert_dates(data)
        self.assertEqual(converted["datum"], "2025-01-01")

if __name__ == '__main__':
    unittest.main()