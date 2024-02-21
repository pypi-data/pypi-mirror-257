# main.py
import requests
import json


def jprint(obj):
    # create a formatted string of the Python JSON object
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)


def getPersonalInfo():
    response = requests.get(
        "https://oura-a8ioop.5sc6y6-4.usa-e2.cloudhub.io/private")
    return (response.json())


if __name__ == "__main__":
    value = getPersonalInfo()
    jprint(value)
