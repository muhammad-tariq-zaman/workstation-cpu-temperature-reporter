import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import unittest
from main import report

def row(workstation, core, temp):
    return {"workstation": workstation, "core": core,
            "temperature_c": str(temp)}

class TestCpuTemperatureReporter(unittest.TestCase):
    def test_over_threshold(self):
        r, _ = report([row("WS-01", "0", 94)])
        self.assertEqual(r[0][3], "OVER")
        self.assertIn("over 80 C limit", r[0][4])

    def test_exactly_max_is_ok(self):
        r, _ = report([row("WS-01", "0", 80)])
        self.assertEqual(r[0][3], "OK")

    def test_custom_max(self):
        r, _ = report([row("WS-01", "0", 85)], max_temp=90)
        self.assertEqual(r[0][3], "OK")

    def test_hottest_first(self):
        r, _ = report([row("WS-01", "0", 55), row("WS-02", "3", 94),
                       row("WS-01", "1", 72)])
        self.assertEqual([(x[0], x[1]) for x in r],
                         [("WS-02", "3"), ("WS-01", "1"), ("WS-01", "0")])

    def test_negative_temperature_is_valid(self):
        r, _ = report([row("WS-01", "0", -5)])
        self.assertEqual(r[0][3], "OK")

    def test_invalid_row_is_skipped(self):
        r, skipped = report([row("WS-01", "0", "hot"),
                             row("WS-01", "1", 55)])
        self.assertEqual((len(r), skipped), (1, 1))

    def test_empty_input(self):
        self.assertEqual(report([]), ([], 0))
