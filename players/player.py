from keys import config
from servers import server
import requests
from utils import exception
import sys
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
        return data
    
    def playermatch(self,queue,type='ranked',count = 10):
        '''type = ['ranked','normal','tourney','tutorial'] 
            count = range[0.100]
            queue = ['RANKED_SOLO_5x5','RANKED_FLEX_SR','NORMAL_5v5_BLIND','NORMAL_5v5_DRAFT','ARAM_5v5_RANDOM']'''
        puuid = self.playerinfo()['puuid']

        if queue == 'RANKED_SOLO_5x5' and type == 'ranked':
            queueID = 420
        elif queue == 'NORMAL_5v5_BLIND' and type == 'normal':
            queueID = 430
        elif queue == 'RANKED_FLEX_SR' and type == 'ranked':
            queueID = 440
        elif queue == 'ARAM_5v5_RANDOM' and type == 'normal':
            queueID = 450
        elif queue == 'NORMAL_5v5_DRAFT' and type == 'normal':
            queueID = 400
        else:
            if queue is None:
                url = url = f'https://{self.shard}.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?start=0&count=20&api_key=RGAPI-eb31bc31-4878-4168-9c76-91cbe0efdf74&count={count}&type={type}'
                data = requests.get(url).json()
            else:
                raise exception.CException('Invalid queue or type',sys)
        url = f'https://{self.shard}.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?start=0&count=20&api_key=RGAPI-eb31bc31-4878-4168-9c76-91cbe0efdf74&count={count}&type={type}&queue={queue}'
        data = requests.get(url).json()
        return data

    def playerstats(self,type = 'ranked'):
        matches = self.playermatch(type)
        c = len(matches)
        for i in matches:
            url = f'https://{self.shard}.api.riotgames.com/lol/match/v5/matches/{i}?api_key={API_KEY}'
            data = requests.get(url).json()
        return data

        

    def playerleague():
        pass

    def playerperformance():
        pass

