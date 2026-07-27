from httpx import Client

BASE_URL = "https://api.open-meteo.com/v1/forecast"


class OpenMeteoClient:
    def __init__(self):
        self.client = Client(timeout=30)

    def get_forecast(
        self,
        latitude: float,
        longitude: float,
    ) -> dict:
        response = self.client.get(
            BASE_URL,
            params={
                "latitude": latitude,
                "longitude": longitude,
                "daily": ",".join(
                    [
                        "temperature_2m_max",
                        "temperature_2m_min",
                        "precipitation_sum",
                        "windspeed_10m_max",
                        "relative_humidity_2m_mean",
                        "weathercode",
                    ]
                ),
                "timezone": "auto",
            },
        )

        response.raise_for_status()

        return response.json()

    def close(self):
        self.client.close()
