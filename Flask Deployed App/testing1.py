import unittest
import os
from werkzeug.datastructures import FileStorage

# Simple utility functions to isolate for testing
def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def format_prediction_label(raw_label):
    return raw_label.replace("_", " ").title()

class TestBackendUtilities(unittest.TestCase):
    
    # Test Case 1: Verifying image extension safety filtering
    def test_allowed_file_valid(self):
        self.assertTrue(allowed_file("leaf_spot.jpg"))
        self.assertTrue(allowed_file("sign.png"))
        
    def test_allowed_file_invalid(self):
        self.assertFalse(allowed_file("malicious_script.exe"))
        self.assertFalse(allowed_file("report.pdf"))

    # Test Case 2: Verifying UI string formatting engine
    def test_label_formatting(self):
        self.assertEqual(format_prediction_label("tomato_late_blight"), "Tomato Late Blight")
        self.assertEqual(format_prediction_label("stop_sign"), "Stop Sign")

if __name__ == '__main__':
    unittest.main()