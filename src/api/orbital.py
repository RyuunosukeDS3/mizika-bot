import requests
from config import ORBITAL_BASE_URL

class Orbital:
    def __init__(self):
        self.api_url = f"{ORBITAL_BASE_URL}:8080"

    def increase_argo_app_replica_count(self, app_name):
        return self._post("increaseReplicaCount", {"appName": app_name})

    def _post(self, endpoint, data):
        return requests.post(f"{self.api_url}/{endpoint}", json=data, headers={"Content-Type": "application/json"})

