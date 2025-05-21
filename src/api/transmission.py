import transmission_rpc
import os
from config import TRANSMISSION


class Transmission:
    def __init__(self):
        self.client = transmission_rpc.Client(
            host=TRANSMISSION["host"],
            port=TRANSMISSION["port"],
            username=TRANSMISSION["username"],
            password=TRANSMISSION["password"],
        )

    def add_torrent(self, torrent, label: str):
        download_dir = self.client.get_session().download_dir
        label_dir = os.path.join(download_dir, label)

        if (isinstance(torrent, str) and torrent.startswith("magnet:")) or isinstance(
            torrent, bytes
        ):
            return self.client.add_torrent(
                torrent, download_dir=label_dir, labels=[label]
            )
        else:
            return None

    def remove_torrent(self, torrent_id: int):
        self.client.remove_torrent(torrent_id, delete_data=True)
