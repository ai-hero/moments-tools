import os
import json
import numpy as np
from unittest import TestCase
from helpers.zero_shot_text_classification import ZeroShotTextClassifier


class ZeroShotTestCase(TestCase):
    def setUp(self):
        ZeroShotTextClassifier.load()

    def test_one(self):
        file_one = os.path.join(os.path.dirname(__file__), "test_data_one.json")
        with open(file_one, "r", encoding="utf-8") as f:
            data = json.loads(f.read())
            prediction = ZeroShotTextClassifier.predict(
                text=data["text"], candidate_labels=data["labels"]
            )
            self.assertEqual(data["labels"][np.argmax(prediction)], "happy")
            # Use actual probability as additional check if model/something changes
            self.assertGreaterEqual(prediction[np.argmax(prediction)], 0.97)

    def test_two(self):
        file_two = os.path.join(os.path.dirname(__file__), "test_data_two.json")
        with open(file_two, "r", encoding="utf-8") as f:
            data = json.loads(f.read())
            prediction = ZeroShotTextClassifier.predict(
                text=data["text"], candidate_labels=data["labels"]
            )
            self.assertEqual(data["labels"][np.argmax(prediction)], "sports")
            # Use actual probability as additional check if model/something changes
            self.assertGreaterEqual(prediction[np.argmax(prediction)], 0.97)
