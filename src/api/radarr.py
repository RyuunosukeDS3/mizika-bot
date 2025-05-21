import requests
import math
from config import RADARR_BASE_URL, RADARR_API_KEY


class Radarr:
    def __init__(self):
        self.api_url = f"{RADARR_BASE_URL}/api/v3"
        self.headers = {"X-Api-Key": RADARR_API_KEY}

    def get_radarr_queue_by_torrent_id(self, torrent_id):
        page = 1

        response = requests.get(
            f"{self.api_url}/queue?page={page}&pageSize=10&includeMovie=true",
            headers=self.headers,
        )

        if response.status_code == 200:
            data = response.json()
            total_pages = math.ceil(data["totalRecords"] / data["pageSize"])

            while page <= total_pages:
                if response.status_code == 200:
                    for queue in data["records"]:
                        if queue["downloadId"].upper() == torrent_id.upper():
                            return queue

                response = requests.get(
                    f"{self.api_url}/queue?page={page}", headers=self.headers
                )
                data = response.json()

        return None

    def refresh_monitored_downloads_command(self):
        response = requests.post(
            f"{self.api_url}/command",
            headers=self.headers,
            json={"name": "RefreshMonitoredDownloads"},
        )
        if response.status_code == 201:
            return True
        return False
