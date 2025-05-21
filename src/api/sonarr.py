import requests
import math
from config import SONARR_BASE_URL, SONARR_API_KEY


class Sonarr:
    def __init__(self):
        self.api_url = f"{SONARR_BASE_URL}/api/v3"
        self.headers = {"X-Api-Key": SONARR_API_KEY}

    def get_sonarr_series(self, torrent_id):
        page = 1
        query_string = (
            "includeUnknownSeriesItems=false&includeSeries=false&includeEpisode=false"
        )
        response = requests.get(
            f"{self.api_url}/queue?page={page}&pageSize=10&{query_string}",
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
                    f"{self.api_url}/series?page={page}", headers=self.headers
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
