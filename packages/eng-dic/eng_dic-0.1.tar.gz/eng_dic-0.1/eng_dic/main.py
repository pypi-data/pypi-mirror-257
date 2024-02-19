import requests

def Meaningof(query):
    try:
        res = requests.get(f"https://api.dictionaryapi.dev/api/v2/entries/en/{query}")
        data = res.json()
        lst = list()
        for entry in data:
            for meaning in entry["meanings"]:
                definitions = meaning["definitions"]
                for definition in definitions:
                    lst.append(definition["definition"])
    except Exception:
        return "Sorry not found"
    return lst

if __name__ == "__main__":
    print(Meaningof("hi"))
