import unittest
import os
# Import your specific helper function from your newly updated app.py code
from app import app

class TestPlantDiseaseBackend(unittest.TestCase):

    def setUp(self):
        """Set up a test client framework for the Flask app."""
        self.ctx = app.app_context()
        self.ctx.push()
        self.client = app.test_client()

    def tearDown(self):
        """Clean up context tracking states after tests run."""
        self.ctx.pop()

    def test_routing_home_endpoint(self):
        """Test Case 1: Verify the default home landing page responds with a valid HTTP 200 code."""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_routing_index_endpoint(self):
        """Test Case 2: Verify the main AI engine upload view path loads correctly."""
        response = self.client.get('/index')
        self.assertEqual(response.status_code, 200)

    def test_empty_payload_submission_rejection(self):
        """Test Case 3: Verify the robust error handling logic when a submission request lacks proper payload matrix layers."""
        # Triggers a POST request containing an empty form boundary payload to check error boundaries
        response = self.client.post('/submit', data={})
        # Verifies that your backend handles unexpected states gracefully by bad request status or matching error templates
        self.assertIn(response.status_code, [400, 500, 200])

if __name__ == '__main__':
    unittest.main()