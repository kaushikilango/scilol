from keys import config
from servers import server as sr
import requests
from utils import exception
import sys
API_KEY = config.API_KEY

class Player:
    def __init__(self,summoner_name,server):
        self.summoner_name = summoner_name
        self.server = server
        self.shard = sr.get_shard(server)
        self.puuid = self.playerinfo()['puuid']
        self.rank = self.playerleague()['tier'] + ' ' + self.playerleague()['rank'] + ' ' + self.playerleague()['leaguePoints'] + 'LP'
        self.accountId = self.playerinfo()['accountId']
        
    def playerinfo(self):
        url = f'https://{self.server}.api.riotgames.com/lol/summoner/v4/summoners/by-name/Miman?api_key={API_KEY}'
        d = requests.get(url)
        data = d.json()
        return data
    
    def playermatch(self,queue,type='ranked',count = 10):
        '''type = ['ranked','normal','tourney','tutorial'] 
            count = range[0.100]
            queue = ['RANKED_SOLO_5x5','RANKED_FLEX_SR','NORMAL_5v5_BLIND','NORMAL_5v5_DRAFT','ARAM_5v5_RANDOM']'''
        print(f'Queue: {queue} and Type: {type}')
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
                url = url = f'https://{self.shard}.api.riotgames.com/lol/match/v5/matches/by-puuid/{self.puuid}/ids?start=0&api_key={API_KEY}&count={count}&type={type}'
                data = requests.get(url).json()
                return data
            else:
                print('Invalid queue or type')
                return None
        url = f'https://{self.shard}.api.riotgames.com/lol/match/v5/matches/by-puuid/{self.puuid}/ids?start=0&api_key={API_KEY}&count={count}&type={type}&queue={queueID}'
        data = requests.get(url).json()
        return data
 
    def playermatchinfo(self,data):
        i = data['metadata']['participants'].index(self.puuid)
        data = data['info']['participants'][i]
        kills,deaths,assists = data['kills'],data['deaths'],data['assists']
        if deaths == 0:
            deaths = 1
        kda = (kills+assists)/deaths
        gpm = data['goldEarned']/(data['timePlayed'] / 60)
        cspm = data['totalMinionsKilled']/(data['timePlayed'] / 60)
        dps  = data['totalDamageDealtToChampions']
        role = data['individualPosition']
        lane = data['lane']
        multikill = data['largestMultiKill']
        return {'kda':kda,'gpm':gpm,'cspm':cspm,'dps':dps,'role':role,'lane':lane,'multikill':multikill}

    def playerstats(self,queue = 'RANKED_SOLO_5x5',type = 'ranked'):
        matches = self.playermatch(queue,type,count=40)
        print(matches)
        print(f'Trying to retrieve {len(matches)} matches')
        kda,gpm,cspm,dps,multikill = 0,0,0,0,0
        lane = {'TOP':0,'JUNGLE':0,'MIDDLE':0,'BOTTOM':0,'NONE':0}
        multikill = {1:0,2:0,3:0,4:0,5:0}
        for i in matches:
            url = f'https://{self.shard}.api.riotgames.com/lol/match/v5/matches/{i}?api_key={API_KEY}'
            match_data = self.playermatchinfo(requests.get(url).json())
            kda = kda + match_data['kda']
            gpm = gpm + match_data['gpm']
            cspm = cspm + match_data['cspm']
            dps = dps + match_data['dps']
            multikill[match_data['multikill']] = multikill[match_data['multikill']] + 1
            lane[match_data['lane']] = lane[match_data['lane']] + 1
        most_multikill = max(multikill,key=multikill.get)
        frequent_lane = max(lane,key=lane.get)
        kda = kda/len(matches)
        gpm = gpm/len(matches)
        cspm = cspm/len(matches)
        dps = dps/len(matches)
        multikill = multikill/len(matches)
        return {'kda':kda,'gpm':gpm,'cspm':cspm,'dps':dps,'frequent_lane':frequent_lane,'multikill':multikill}

    def getencrypteddetails(self):
        url = f'https://{self.server}.api.riotgames.com/lol/summoner/v4/summoners/by-puuid/{self.puuid}?api_key={API_KEY}'
        data = requests.get(url).json()
        return data

    def playerleague(self):
        _id = self.getencrypteddetails()['id']
        url = f'https://{self.server}.api.riotgames.com/lol/league/v4/entries/by-summoner/{_id}?api_key={API_KEY}'
        data = requests.get(url).json()
        return data
    
    def playerperformance():
        pass



pl = Player('Miman','NA1')
print(pl.playerleague())