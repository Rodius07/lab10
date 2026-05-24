from __future__ import annotations

import argparse
import os
import time
from pathlib import Path

import sounddevice as sd
from faster_whisper import WhisperModel
from scipy.io.wavfile import write

from lab7 import get_city_data, get_lat_and_lon


COMMANDS = {
    "погода": "weather",
    "температура": "temperature",
    "давление": "pressure",
    "влажность": "humidity",
    "стоп": "stop",
}


def record_audio(path: Path, duration: int, sample_rate: int) -> None:
    print("Говорите...")
    recording = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1)
    sd.wait()
    write(path, sample_rate, recording)


def transcribe(model: WhisperModel, audio_path: Path) -> str:
    segments, _ = model.transcribe(str(audio_path), language="ru")
    text = "".join(segment.text for segment in segments if segment.text)
    return text.strip().lower().replace(".", "").replace("!", "")


def load_weather() -> dict:
    lat, lon = get_lat_and_lon()
    return get_city_data(lat, lon)


def answer_command(command: str, weather_data: dict) -> bool:
    action = COMMANDS.get(command)

    if action == "weather":
        print(weather_data["weather"][0]["description"])
    elif action == "temperature":
        print(weather_data["main"]["temp"])
    elif action == "pressure":
        print(weather_data["main"]["pressure"])
    elif action == "humidity":
        print(weather_data["main"]["humidity"])
    elif action == "stop":
        return False
    elif not command:
        print("Вы ничего не сказали.")
    else:
        print("Неизвестная команда.")

    return True


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Голосовой помощник для запроса погоды.")
    parser.add_argument("--duration", type=int, default=3, help="Длительность записи в секундах.")
    parser.add_argument("--sample-rate", type=int, default=16000, help="Частота дискретизации аудио.")
    parser.add_argument("--model", default="small", help="Модель faster-whisper.")
    parser.add_argument("--pause", type=float, default=1.5, help="Пауза между командами.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    audio_path = Path("my_record.wav")
    model = WhisperModel(args.model, device="cpu", compute_type="int8")

    try:
        while True:
            record_audio(audio_path, args.duration, args.sample_rate)
            command = transcribe(model, audio_path)
            print(f"Распознано: {command or 'пусто'}")

            weather_data = load_weather()
            if not answer_command(command, weather_data):
                break

            time.sleep(args.pause)
    finally:
        if audio_path.exists():
            os.remove(audio_path)


if __name__ == "__main__":
    main()
