import json

# Tarkistetaan tiedoston sisältö
def tarkista_json(tiedosto):
    try:
        with open(tiedosto, "r", encoding="utf-8") as f:
            data = json.load(f)
        print("✅ JSON on validi!")
        return data
    except json.JSONDecodeError as e:
        print("❌ JSON-virhe:", e)
    except FileNotFoundError:
        print("❌ Tiedostoa ei löydy:", tiedosto)

# Käyttö:
data = tarkista_json("level1_data.json")