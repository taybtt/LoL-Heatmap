import requests

API_KEY = "RGAPI-6f7e1eed-f2ba-431a-8ab6-97fba2064e56"
REGION = "europe"  # americas | asia | europe | sea
headers = {"X-Riot-Token": API_KEY}
gameName = "Sandalye1"  #username
tagLine = "EUW"  #usertag


#url = f"https://{REGION}.api.riotgames.com/lol/status/v4/platform-data"
url = f"https://europe.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{gameName}/{tagLine}"

response = requests.get(url, headers=headers)
data = response.json()

puuid = data["puuid"]

url = f"https://{REGION}.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids"
matches = requests.get(url, headers={"X-Riot-Token": API_KEY}).json()

match_id = matches[1]

#timeline
url = f"https://{REGION}.api.riotgames.com/lol/match/v5/matches/{match_id}/timeline"
timeline = requests.get(url, headers={"X-Riot-Token": API_KEY}).json()


#for i in range(1,11):
#    print(i, timeline["info"]["frames"][11]['participantFrames'][str(i)]['position'])
for k in range(0,30):
    #print(timeline["info"]["frames"][k]['timestamp']/60000)
    print(timeline["info"]["frames"][10]['events'][0])

