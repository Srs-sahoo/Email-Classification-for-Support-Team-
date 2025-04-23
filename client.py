import json
import requests

data = {
    "email_text": "Unvorhergesehener Absturz der Datenanalyse-Plattform Die Datenanalyse-Plattform brach unerwartet ab, da die SpeicheroberflÃ¤che zu gering war My name is Sophia Rossi.. Ich habe versucht, Laravel 8 und meinen MacBook Pro neu zu starten, aber das Problem behÃ¤lt sich bei. Ich benÃ¶tige Ihre UnterstÃ¼tzung, um diesen Fehler zu beheben. You can reach me at janesmith@company.com."
    }

url = 'http://127.0.0.1:8000/process_email/'

data = json.dumps(data)
responce = requests.post(url,data)
print(responce.json())