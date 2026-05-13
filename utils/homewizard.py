import requests


class HomeWizard:
    def __init__(self, ip):
        self.base_url = f"http://{ip}/api/v1"

    def get_data(self):
        url = f"{self.base_url}/data"

        response = requests.get(
            url,
            timeout=1
        )

        response.raise_for_status()
        return response.json()

    def get_active_power(self):
        data = self.get_data()
        return data.get("active_power_w")