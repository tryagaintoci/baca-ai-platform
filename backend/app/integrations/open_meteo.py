from httpx import Client, HTTPError

BASE_URL = "https://api.open-meteo.com/v1/forecast"


class OpenMeteoClient:
    def __init__(self):
        self.client = Client(timeout=30.0)

    def get_forecast(
        self,
        latitude: float,
        longitude: float,
    ) -> dict:
        try:
            response = self.client.get(
                BASE_URL,
                params={
                    "latitude": latitude,
                    "longitude": longitude,
                    "timezone": "auto",
                    "forecast_days": 7,
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
                },
            )

            response.raise_for_status()
            return response.json()

        except HTTPError as exc:
            raise RuntimeError(
                f"Open-Meteo request failed: {exc}"
            ) from exc

    def close(self):
        self.client.close()