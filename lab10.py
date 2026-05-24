import os
import time

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


def record_audio(path, duration, sample_rate):
    print("Говорите...")
    recording = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1)
    sd.wait()
    write(path, sample_rate, recording)


def transcribe(model, audio_path):
    segments, _ = model.transcribe(str(audio_path), language="ru")
    text = "".join(segment.text for segment in segments if segment.text)
    return text.strip().lower().replace(".", "").replace("!", "")


def load_weather():
    lat, lon = get_lat_and_lon()
    return get_city_data(lat, lon)


def answer_command(command):
    action = COMMANDS.get(command)

    if not command:
        print("Вы ничего не сказали.")
        return True
    if action == "stop":
        return False
    if not action:
        print("Неизвестная команда.")
        return True

    weather_data = load_weather()

    if action == "weather":
        print(weather_data["weather"][0]["description"])
    elif action == "temperature":
        print(weather_data["main"]["temp"])
    elif action == "pressure":
        print(weather_data["main"]["pressure"])
    elif action == "humidity":
        print(weather_data["main"]["humidity"])

    return True


def main():
    duration = 3
    sample_rate = 16000
    model_name = "small"
    pause = 1.5
    audio_path = "my_record.wav"
    model = WhisperModel(model_name, device="cpu", compute_type="int8")

    try:
        while True:
            record_audio(audio_path, duration, sample_rate)
            command = transcribe(model, audio_path)
            print(f"Распознано: {command or 'пусто'}")

            if not answer_command(command):
                break

            time.sleep(pause)
    finally:
        if os.path.exists(audio_path):
            os.remove(audio_path)


if __name__ == "__main__":
    main()
