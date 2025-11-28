#positions over all games
#heatmap
import requests
import cv2
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np


#get data from riot api
API_KEY = "RGAPI-5447478d-c666-4908-8c78-5245364a43a4"
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

#events timestamps
#for k in range(0,30):
    #print(timeline["info"]["frames"][k]['timestamp']/60000)
    #(timeline["info"]["frames"][10]['events'][0])
#for i in range(1,11):
    #print(timeline["info"]["frames"][11]['participantFrames'][str(i)]['position']) - all positions of champs on frame 11

#get map
map_img = cv2.imread("map.jpg")
map_img = cv2.cvtColor(map_img, cv2.COLOR_BGR2RGB)
height, width, _ = map_img.shape

#riot map measures
RIOT_MAX_X = 14820
RIOT_MAX_Y = 14881

#print("Map size:", width, height)

#TODO: add padding to the map to get 0,0 to correct position and check how the 
# data points are mapped, perfect x y axis? is the og map crooked whats happening

#map riot onto the map size
def to_pixel(x, y, img_width=width, img_height=height):
    px = int((x / RIOT_MAX_X) * img_width)
    py = img_height - int((y / RIOT_MAX_Y) * img_height)  # invert Y-axis
    return px, py

#build map
xs = []
ys = []

positions = []

frames = timeline['info']['frames']
total_frames = len(frames)

for k in range(0,total_frames):
    positions.append(timeline["info"]["frames"][k]['participantFrames'][str(1)]['position']) #champ 1
    #print(timeline["info"]["frames"][11]['participantFrames'][str(i)]['position'])

print(positions)



#plot according to positions
def plot(positions):
    xs, ys = [], []

    for pos in positions:
        px, py = to_pixel(pos["x"], pos["y"])
        xs.append(px)
        ys.append(py)
        
    plt.figure(figsize=(8, 8))

    # show the map image
    plt.imshow(map_img, extent=[0, width, height, 0])

    # draw heatmap
    sns.kdeplot(
        x=xs,
        y=ys,
        cmap="hot",
        fill=True,
        alpha=0.5,
        bw_adjust=0.6,
        thresh=0.05,
    )

    #plt.axis("off")
    plt.show()

plot(positions)