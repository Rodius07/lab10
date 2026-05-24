import os
from typing import Any

import requests
from dotenv import load_dotenv


load_dotenv()
load_dotenv("keys.env")

CITY_NAME = os.getenv("CITY_NAME", "London")
OPENWEATHERMAP_API = os.getenv("OPENWEATHERMAP_API")
DICTIONARY_API = os.getenv("DICTIONARY_API")


def require_env(name: str, value: str | None) -> str:
    if not value:
        raise RuntimeError(f"Environment variable {name} is required")
    return value


def request_json(url: str, params: dict[str, str], timeout: int = 10) -> Any:
    response = requests.get(url=url, params=params, timeout=timeout)
    response.raise_for_status()
    return response.json()


def get_lat_and_lon() -> tuple[float, float]:
    url = "http://api.openweathermap.org/geo/1.0/direct"
    params = {
        "q": CITY_NAME,
        "appid": require_env("OPENWEATHERMAP_API", OPENWEATHERMAP_API),
    }

    data = request_json(url, params)
    if not data:
        raise RuntimeError(f"City not found: {CITY_NAME}")
    return data[0]["lat"], data[0]["lon"]


def get_city_data(lat: float, lon: float) -> dict[str, Any]:
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "lat": str(lat),
        "lon": str(lon),
        "appid": require_env("OPENWEATHERMAP_API", OPENWEATHERMAP_API),
        "lang": "ru",
        "units": "metric",
    }

    return request_json(url, params)


def get_word_info(word: str) -> Any:
    url = (
        f"https://www.dictionaryapi.com/api/v3/"
        f"references/collegiate/json/{word}"
    )
    params = {
        "key": require_env("DICTIONARY_API", DICTIONARY_API),
    }

    return request_json(url, params)


if __name__ == "__main__":
    lat, lon = get_lat_and_lon()
    data = get_city_data(lat, lon)

    weather = data["weather"][0]["description"]
    temp = data["main"]["temp"]
    pressure = data["main"]["pressure"]
    humidity = data["main"]["humidity"]

    print(f"погода: {weather} {temp}")
    print(f"влажность: {humidity}")
    print(f"давление: {pressure}")

    word = "kill"
    data = get_word_info(word)

    print(f"формы: {data[0]['meta']['stems']}")
    print(f"Агрессивное: {'Да' if data[0]['meta']['offensive'] else 'Нет'}")
    print(f"по слогам: {data[0]['hwi']['hw']}")
    print(f"часть речи: {data[0]['fl']}")
    print(f"определение: {data[0]['def'][0]['sseq'][0][0][1]['dt'][0][1]}")
