"""Exercise the API's JSON contract with Flask's in-process client."""

import unittest

from app import app
from bias_detector import EXAMPLES


class PricingApiTests(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_analyze_rejects_non_object_or_non_string_pricing(self):
        for body in [None, [], ["pricing_text"], "pricing_text", 42,
                     {}, {"pricing_text": None}, {"pricing_text": 42},
                     {"pricing_text": []}, {"pricing_text": {}},
                     {"pricing_text": "   "}]:
            with self.subTest(body=body):
                response = self.client.post("/api/analyze", json=body)
                self.assertEqual(response.status_code, 400)
                self.assertIn("error", response.get_json())

    def test_example_rejects_non_object_or_non_string_name(self):
        for body in [None, [], "Netflix", 42, {},
                     {"example_name": None}, {"example_name": []},
                     {"example_name": {}}, {"example_name": 42}]:
            with self.subTest(body=body):
                response = self.client.post("/api/example", json=body)
                self.assertEqual(response.status_code, 400)
                self.assertIn("error", response.get_json())

    def test_malformed_json_has_a_json_error(self):
        for endpoint in ["/api/analyze", "/api/example"]:
            with self.subTest(endpoint=endpoint):
                response = self.client.post(endpoint, data="{", content_type="application/json")
                self.assertEqual(response.status_code, 400)
                self.assertIn("error", response.get_json())

    def test_all_examples_can_be_loaded_and_analyzed(self):
        for name, example in EXAMPLES.items():
            with self.subTest(name=name):
                response = self.client.post("/api/example", json={"example_name": name})
                self.assertEqual(response.status_code, 200)
                self.assertEqual(response.get_json()["text"], example["text"])
                response = self.client.post("/api/analyze", json={
                    "product_name": name, "pricing_text": example["text"],
                })
                self.assertEqual(response.status_code, 200)
                result = response.get_json()
                self.assertEqual(result["product_name"], name)
                self.assertGreaterEqual(result["overall_score"], 0)
                self.assertLessEqual(result["overall_score"], 100)
                self.assertTrue(result["biases"])

    def test_unknown_example_is_not_found(self):
        response = self.client.post("/api/example", json={"example_name": "not an example"})
        self.assertEqual(response.status_code, 404)


if __name__ == "__main__":
    unittest.main()
