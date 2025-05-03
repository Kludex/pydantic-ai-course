import os
from pydantic_ai import Agent
import httpx
from datetime import datetime
import logfire

logfire.configure()
logfire.instrument_pydantic_ai()
logfire.instrument_httpx(capture_all=True)

open_weather_api_key = os.getenv("OPEN_WEATHER_API_KEY")
assert open_weather_api_key is not None, "OPEN_WEATHER_API_KEY is not set"

agent = Agent("openai:gpt-4.1")
client = httpx.Client()


@agent.tool_plain
def get_current_date():
    return datetime.now().strftime("%Y-%m-%d")


@agent.tool_plain
def get_temperature(lat: float, lon: float) -> float:
    """Get the temperature in a given location.

    Args:
        lat: The latitude of the location.
        lon: The longitude of the location.
    """
    # ❯ http "https://api.openweathermap.org/data/2.5/weather?lat=23.5558&lon=46.6396&units=metric&appid=$OPEN_WEATHER_API_KEY"
    response = client.get(
        "https://api.openweathermap.org/data/2.5/weather",
        params={
            "lat": lat,
            "lon": lon,
            "units": "metric",
            "appid": open_weather_api_key,
        },
    )
    response.raise_for_status()
    data = response.json()
    return data["main"]["temp"]


result = agent.run_sync("Qual a temperatura em São Paulo?")
print(result.output)
