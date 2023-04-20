# needs `pip install locust`
import json
from random import random
from locust import HttpUser, task


class TestPredictor(HttpUser):
    def on_start(self):
        with open("app/tests/test_data_one.json", "r", encoding="utf-8") as f:
            self.json_data_one = json.loads(f.read())
        with open("app/tests/test_data_two.json", "r", encoding="utf-8") as f:
            self.json_data_two = json.loads(f.read())

    @task
    def ping(self):
        self.client.get("/ping")

    @task
    def predict(self):
        if random() > 0.5:
            request_obj = self.json_data_one
        else:
            request_obj = self.json_data_two
        resp = self.client.post("/predict", json=request_obj)
        resp.raise_for_status()
