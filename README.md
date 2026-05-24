# Lab 10

Голосовой помощник на Python: записывает короткую фразу с микрофона, распознает команду через `faster-whisper` и выводит данные о погоде через OpenWeatherMap.

Поддерживаемые команды:

- `погода`
- `температура`
- `давление`
- `влажность`
- `стоп`

## Установка

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Настройка

Создайте файл `.env` по примеру:

```bash
cp .env.example .env
```

Заполните ключи:

```env
OPENWEATHERMAP_API=...
DICTIONARY_API=...
CITY_NAME=London
```

`DICTIONARY_API` используется в `lab7.py`; для голосового помощника нужен только `OPENWEATHERMAP_API`.

## Запуск

```bash
python lab10.py
```

Можно поменять длительность записи и частоту:

```bash
python lab10.py --duration 4 --sample-rate 16000
```
