import os
import unittest
from voliboli_pdf_scraper.main import process_pdf

class TestPDFScraper(unittest.TestCase):
    STAT_DIRECTORY = 'stats'
    DEBUG = False

    def test_processing(self):
        for f in os.listdir(self.STAT_DIRECTORY):
            print(f"Processing {f} file...")
            file = os.path.join(self.STAT_DIRECTORY, f)
            output = process_pdf(file, debug=self.DEBUG)
            print(output)

        self.assertIsNotNone(output)

if __name__ == '__main__':
    unittest.main()
