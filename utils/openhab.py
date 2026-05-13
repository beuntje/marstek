import requests


class OpenHAB:
    def __init__(self, url):
        self.base_url = url.rstrip("/")

    def get_item_state(self, item_name):
        url = f"{self.base_url}/rest/items/{item_name}/state"

        response = requests.get(
            url,
            timeout=1
        )

        response.raise_for_status()

        return response.text.strip()

    def set_item_state(self, item_name, value):
        url = f"{self.base_url}/rest/items/{item_name}"

        response = requests.post(
            url,
            data=str(value),
            headers={
                "Content-Type": "text/plain"
            },
            timeout=1
        )

        response.raise_for_status()

        return True