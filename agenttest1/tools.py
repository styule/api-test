import datetime
import requests
import numexpr

# --- Original tools ---


def get_time():
    return {"time": datetime.datetime.now().isoformat()}


def reverse_text(text: str):
    return {"reversed": text[::-1]}


# --- Calculator ---


def calculator(expression: str):
    print("Calculator received:", repr(expression))
    try:
        result = numexpr.evaluate(expression)
        return {"result": float(result)}
    except Exception as e:
        return {"error": f"Could not evaluate: {str(e)}"}


# --- Weather (Open-Meteo API) ---


def get_weather(city: str):
    geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}"
    geo_resp = requests.get(geo_url).json()
    if "results" not in geo_resp or not geo_resp["results"]:
        return {"error": "City not found"}
    lat = geo_resp["results"][0]["latitude"]
    lon = geo_resp["results"][0]["longitude"]

    weather_url = (
        "https://api.open-meteo.com/v1/forecast?"
        f"latitude={lat}&longitude={lon}&current_weather=true"
    )
    weather_resp = requests.get(weather_url).json()
    if "current_weather" not in weather_resp:
        return {"error": "Weather data unavailable"}
    weather = weather_resp["current_weather"]
    return {
        "city": city,
        "temperature": weather["temperature"],
        "windspeed": weather["windspeed"],
        "weathercode": weather["weathercode"],
    }


# --- File Summarizer ---


def summarize_file(filepath: str):
    if not filepath.endswith(".txt"):
        return {"error": "Only .txt files supported"}
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read(2000)
        # (Just returns text, let LLM summarize. LLM will see the first 2000 chars.)
        return {"content": content}
    except Exception as e:
        return {"error": str(e)}


# --- Dictionary Lookup (DictionaryAPI.dev) ---


def define_word(word: str):
    url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
    resp = requests.get(url)
    if resp.status_code != 200:
        return {"error": "Word not found"}
    data = resp.json()
    definitions = []
    for meaning in data[0].get("meanings", []):
        defs = meaning.get("definitions", [])
        if defs:
            definitions.append(defs[0].get("definition", ""))
    return {"word": word, "definitions": definitions}
