import csv
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest


class TestCsvFilenameDemo(unittest.TestCase):
    def test_can_run_from_another_directory_without_overwriting_its_csv(self):
        source = Path(__file__).resolve().parents[1] / "pandass.py"
        with tempfile.TemporaryDirectory() as tmp:
            exercise = Path(tmp) / "exercise"
            exercise.mkdir()
            entry = exercise / source.name
            shutil.copyfile(source, entry)
            (exercise / "products.csv").write_text(
                'title,price\n"  Red Bike!  ",42\n"Blue, Green",13\n',
                encoding="utf-8",
            )

            caller = Path(tmp) / "caller"
            caller.mkdir()
            (caller / "products.csv").write_text("title,price\nDo not use,1\n")
            caller_output = caller / "products_with_images.csv"
            caller_output.write_text("leave unchanged\n")

            subprocess.run([sys.executable, str(entry)], cwd=caller, check=True, timeout=10)

            self.assertEqual(caller_output.read_text(), "leave unchanged\n")
            with (exercise / "products_with_images.csv").open(newline="", encoding="utf-8") as csv_file:
                self.assertEqual(list(csv.DictReader(csv_file)), [
                    {"title": "  Red Bike!  ", "price": "42", "image": "red_bike.png"},
                    {"title": "Blue, Green", "price": "13", "image": "blue_green.png"},
                ])
