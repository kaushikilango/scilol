from keys import config
import json
import pandas as pd
import requests
import numpy as np


def serverinfo():
    servers = config.SERVERS
    data = []
    for i in servers:
        url = f'https://{i}.api.riotgames.com/lol/status/v4/platform-data?api_key={config.API_KEY}'
        d = requests.get(url)
        text = d.json()
        if d.status_code == 200:
            row = {'id':text['id'],'name':text['name'],'locales':text['locales']}
            data.append(row)
        for j in data:
            if j['id'] in ['BR1','LA1','LA2','NA1','OC1']:
                j['shard'] = 'AMERICAS'
            if j['id'] in ['JP1','KR','PBE1','TW2','TH2','VN2','SG2','PH2']:
                j['shard'] = 'ASIA'
            if j['id'] in ['EUN1','EUW1','TR1','RU']:
                j['shard'] = 'EUROPE'
    
    return pd.DataFrame.from_dict(data)

def get_shard(server):
    d = serverinfo()
    d = d[d['id'] == server]
    return d['shard'].values[0]
