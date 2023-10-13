from keys import config
from servers import server
import requests
API_KEY = config.API_KEY

class Player:
    def __init__(self,summoner_name,server):
        self.summoner_name = summoner_name
        self.server = server
        self.shard = server.get_shard(server)
    def playerinfo(self):
        url = f'https://{self.server}.api.riotgames.com/lol/summoner/v4/summoners/by-name/Miman?api_key={API_KEY}'
        d = requests.get(url)
        data = d.json()

    def playermatch():
        pass

    def playerstats():
        pass

    def playerleague():
        pass

    def playerperformance():
        pass

