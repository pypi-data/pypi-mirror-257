import os
import requests
import json
import base64
import logging
import re
from .exceptions import APIError

class Music:
    musiclm_url = "https://content-aisandbox-pa.googleapis.com/v1:soundDemo?alt=json"

    @staticmethod
    def sanitize_directory_name(directory_name):
        return re.sub(r'[\\/:*?"<>|]', '_', directory_name)[:255]

    def get_tracks(self, input, generationCount, token):
        if not isinstance(generationCount, int):
            generationCount = 2
        generationCount = min(8, max(1, generationCount))

        payload = json.dumps({
            "generationCount": generationCount,
            "input": {
                "textInput": input
            },
            "soundLengthSeconds": 30  # this doesn't change anything 
        })

        headers = {
            'Authorization': f'Bearer {token}'
        }

        try:
            response = requests.post(self.musiclm_url, headers=headers, data=payload)
            response.raise_for_status()  # Raise HTTPError for bad responses
        except requests.exceptions.ConnectionError:
            logging.error("Can't connect to the server.")
            raise APIError("Network error: Can't connect to the server.") from None
        except requests.exceptions.HTTPError as e:
            logging.error(f"Unexpected status code: {e.response.status_code}")
            raise APIError(f"Network error: Unexpected status code {e.response.status_code}.") from None

        if response.status_code == 400:
            logging.error("Oops, can't generate audio for that.")
            raise APIError("Bad Request: Can't generate audio for the given input.")

        tracks = [sound["data"] for sound in response.json().get('sounds', [])]
        return tracks

    def b64toMP3(self, tracks_list, filename):
        count = 0
        new_filename = self.sanitize_directory_name(filename)
        while os.path.exists(new_filename):
            count += 1
            new_filename = f'{filename} ({count})'

        os.makedirs(new_filename, exist_ok=True)

        for i, track in enumerate(tracks_list):
            with open(f"{new_filename}/track{i+1}.mp3", "wb") as f:
                f.write(base64.b64decode(track))

        logging.info("Tracks successfully generated!")
        return 200
