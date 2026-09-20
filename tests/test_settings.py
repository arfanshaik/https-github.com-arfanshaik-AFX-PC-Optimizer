import unittest
from app.settings import DEFAULT_SETTINGS

class TestSettings(unittest.TestCase):
    def test_profile(self):
        self.assertIn(DEFAULT_SETTINGS["profile"], {"Low", "Balanced", "High"})

    def test_priority_type(self):
        self.assertIsInstance(DEFAULT_SETTINGS["auto_raise_priority"], bool)

if __name__ == "__main__":
    unittest.main()
