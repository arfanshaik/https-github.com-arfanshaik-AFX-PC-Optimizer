import unittest
from app.profiles import recommend_profile, get_profile

class TestProfiles(unittest.TestCase):
    def test_low(self):
        self.assertEqual(recommend_profile({"ram_gb": 4, "cpu_cores": 4}), "Low")

    def test_balanced(self):
        self.assertEqual(recommend_profile({"ram_gb": 8, "cpu_cores": 4}), "Balanced")

    def test_high(self):
        self.assertEqual(recommend_profile({"ram_gb": 16, "cpu_cores": 8}), "High")

    def test_fallback(self):
        self.assertEqual(get_profile("Unknown"), get_profile("Balanced"))

if __name__ == "__main__":
    unittest.main()
