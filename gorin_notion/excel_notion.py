import pandas as pd
import numpy as np
import requests
import csv
import matplotlib.pyplot as plt
##########################

filename = ("Tokyo2020_SW_Entry_List.xlsx")
df=pd.read_excel(filename,header=None)
#print(df.head())
#print(df[1:])
Gender=df.iloc[2:,2].tolist()
Country=df.iloc[2:,3].tolist()
Event=df.iloc[2:,4].tolist()
ETime=df.iloc[2:,5].tolist()#Pandas の DataFrame 列をリストに変換
#print(ETime)
FName=df.iloc[2:,0].tolist()
#print(FName)
LName=df.iloc[2:,1].tolist()
#print(LName)
FullName=[]
N=len(LName)
for i in range(N):
    name=LName[i].lower().capitalize()+" "+FName[i].lower().capitalize()
    FullName.append(name)
#print(type(ETime[0]))
aFullName=np.array(FullName)
aFullName.sort()
#FullName[1]
mostName=''
mostNum=0
tmpNum=0
tmpName=""
for i in range(N-1):
    #print(i)
    if tmpNum>mostNum:
        mostNum=tmpNum
        mostName=tmpName
    if aFullName[i]==aFullName[i+1]:
        #print(mostName)
        tmpName=aFullName[i]
        tmpNum+=1
    else:
        tmpNum=0
print(mostName)
print(mostNum+1)

for i in range(N-1):
    #print(i)
    if tmpNum>mostNum:
        mostNum=tmpNum
        mostName=tmpName
    if aFullName[i]==aFullName[i+1]:
        #print(mostName)
        tmpName=FullName[i]
        tmpNum+=1
    else:
        tmpNum=0
    if tmpNum==5:
        print(tmpName)
uName=list(set(aFullName))
#print(Event)
simpEvent=[s.replace('Men\'s ','').replace('Women\'s ','').replace('Butterfly','Fly').replace('Breaststroke','Br').replace('Freestyle','Fr').replace('Backstroke','Ba').replace('Individual Medley','IM')
           for s in Event]
#print(simpEvent)

#print([idx for idx,v in enumerate(FullName) if v=='WATANABE KANAKO'])
myinfo=[]
maxevent=0
for j,name in enumerate(uName):  
    idxlist=[idx for idx,v in enumerate(FullName) if v==name]
    genderlist=[idx for idx,v in enumerate(FullName) if v==name]
    countrylist=[idx for idx,v in enumerate(FullName) if v==name]
    #print(name)
    eventlist=[]
    for i in idxlist:
        eventlist.append(simpEvent[i])
    tmp=len(eventlist)
    if maxevent<tmp:
        maxevent=tmp
    myinfo.append([Gender[genderlist[0]],name,Country[countrylist[0]],eventlist])
#print(myinfo)
#print(maxevent)

men1fly=[]
for i in range(N):
    if Event[i]=="Men's 100m Butterfly":
        men1fly.append([FullName[i],Gender[i],Country[i],ETime[i]])

men1fly=np.array(men1fly)
col_num = 3
#print(men1fly[np.argsort(men1fly[:,col_num])])

import requests
from pprint import pprint
import json


def get_request_url(end_point):
    return f'https://api.notion.com/v1/{end_point}'
notion_api_key = 'secret_3Cb6K5W7LhSnV8PWcnoMn2z2hn8HWgEB7QRc2kzBuTi'
headers = {"Authorization": f"Bearer {notion_api_key}",
           "Content-Type": "application/json",
           "Notion-Version": "2021-05-13"}

databases_ids=[
    'https://www.notion.so/025a1e7920a74350b236c07431ff2f99?v=495ee339c05644a8bc92d4a7425deea4',
    'https://www.notion.so/b5e5f172b2e246ea9b8b36a59ed41dd6?v=d7995e019e8346f2a17067e63be36e85',
]

databases_ids=[
    'https://www.notion.so/025a1e7920a74350b236c07431ff2f99?v=495ee339c05644a8bc92d4a7425deea4',
    'https://www.notion.so/b5e5f172b2e246ea9b8b36a59ed41dd6?v=d7995e019e8346f2a17067e63be36e85',
    'https://www.notion.so/4197741ce5954d4f9c2365814ef6e454?v=dcc032b6877041a0bfb763923dc1b07e',
    'https://www.notion.so/c63dfc741e1d4fe588c2dc2ba8a85679?v=3cb7d2a77e964a059aa8f877c85afc7a',
]
filenames=['RecordsExport_LCM.xlsx','RecordsExport_LCM_WW.xlsx','RecordsExport_LCM_O.xlsx','RecordsExport_LCM_OW.xlsx']

for j,filename in enumerate(filenames): 
    df=pd.read_excel(filename,header=None)
    databases_id=databases_ids[j][22:][:databases_ids[j][22:].find('?')]
    print(df.head())
    evs=df.iloc[2:,0].tolist()
    gender=evs[0][0].replace('W','F')
    #print(gender)
    cons=df.iloc[2:,6].tolist()
    evs=[s.replace('Men ','').replace('Women ','').replace('Butterfly','Fly').replace('Breaststroke','Br').replace('Freestyle','Fr').replace('Backstroke','Ba').replace('Individual Medley','IM')
           for s in evs]
    nams=df.iloc[2:,5].tolist()
    #print(nams)
    nams=[i[:i.find(' ')].lower().capitalize()+i[i.find(' '):] for i in nams]
    tims=df.iloc[2:,4].tolist()
    for i in range(0,len(evs))[::-1]:
        country=cons[i]
        event=evs[i]
        name=nams[i]
        time=tims[i]
        body = {
        "parent": {
            "database_id": databases_id},
        "properties": {
                "Name": {"rich_text": [{"text": {"content": name}}]},
                #"Gender": {"multi_select": {"name": gender}},
                "Country": {"rich_text": [{"text": {"content": country}}]},
                "Event": {"title": [{"text": {"content": event}}]},
                "Time": {"rich_text": [{"text": {"content": time}}]},
            }
        }
        #response = requests.request('POST', url=get_request_url('pages'), headers=headers, data=json.dumps(body))
        #pprint(response.json())

for infor in myinfo:
    gender=infor[0]
    name=infor[1]
    country=infor[2]
    events=infor[3]
    if len(events)==1:
        body = {
            "parent": {
                "database_id": databases_id},
            "properties": {
                    "Name": {"title": [{"text": {"content": name}}]},
                    "Gender": {"select": {"name": gender}},
                    "Country": {"rich_text": [{"text": {"content": country}}]},
                    "Event1": {"rich_text": [{"text": {"content": events[0]}}]},
                    #"Event2": {"rich_text": [{"text": {"content": events[1]}}]},
                    #"Event3": {"rich_text": [{"text": {"content": events[2]}}]},
                    #"Event4": {"rich_text": [{"text": {"content": events[3]}}]},
                    #"Event5": {"rich_text": [{"text": {"content": events[4]}}]},
                    #"Event6": {"rich_text": [{"text": {"content": events[5]}}]}
                }
            }
    elif len(events)==2:
        body = {
            "parent": {
                "database_id": databases_id},
            "properties": {
                    "Name": {"title": [{"text": {"content": name}}]},
                    "Gender": {"select": {"name": gender}},
                    "Country": {"rich_text": [{"text": {"content": country}}]},
                    "Event1": {"rich_text": [{"text": {"content": events[0]}}]},
                    "Event2": {"rich_text": [{"text": {"content": events[1]}}]},
                    #"Event3": {"rich_text": [{"text": {"content": events[2]}}]},
                    #"Event4": {"rich_text": [{"text": {"content": events[3]}}]},
                    #"Event5": {"rich_text": [{"text": {"content": events[4]}}]},
                    #"Event6": {"rich_text": [{"text": {"content": events[5]}}]}
                }
            }
    elif len(events)==3:
        body = {
            "parent": {
                "database_id": databases_id},
            "properties": {
                    "Name": {"title": [{"text": {"content": name}}]},
                    "Gender": {"select": {"name": gender}},
                    "Country": {"rich_text": [{"text": {"content": country}}]},
                    "Event1": {"rich_text": [{"text": {"content": events[0]}}]},
                    "Event2": {"rich_text": [{"text": {"content": events[1]}}]},
                    "Event3": {"rich_text": [{"text": {"content": events[2]}}]},
                    #"Event4": {"rich_text": [{"text": {"content": events[3]}}]},
                    #"Event5": {"rich_text": [{"text": {"content": events[4]}}]},
                    #"Event6": {"rich_text": [{"text": {"content": events[5]}}]}
                }
            }
    elif len(events)==4:
        body = {
            "parent": {
                "database_id": databases_id},
            "properties": {
                    "Name": {"title": [{"text": {"content": name}}]},
                    "Gender": {"select": {"name": gender}},
                    "Country": {"rich_text": [{"text": {"content": country}}]},
                    "Event1": {"rich_text": [{"text": {"content": events[0]}}]},
                    "Event2": {"rich_text": [{"text": {"content": events[1]}}]},
                    "Event3": {"rich_text": [{"text": {"content": events[2]}}]},
                    "Event4": {"rich_text": [{"text": {"content": events[3]}}]},
                    #"Event5": {"rich_text": [{"text": {"content": events[4]}}]},
                    #"Event6": {"rich_text": [{"text": {"content": events[5]}}]}
                }
            }
    elif len(events)==5:
        body = {
            "parent": {
                "database_id": databases_id},
            "properties": {
                    "Name": {"title": [{"text": {"content": name}}]},
                    "Gender": {"select": {"name": gender}},
                    "Country": {"rich_text": [{"text": {"content": country}}]},
                    "Event1": {"rich_text": [{"text": {"content": events[0]}}]},
                    "Event2": {"rich_text": [{"text": {"content": events[1]}}]},
                    "Event3": {"rich_text": [{"text": {"content": events[2]}}]},
                    "Event4": {"rich_text": [{"text": {"content": events[3]}}]},
                    "Event5": {"rich_text": [{"text": {"content": events[4]}}]},
                    #"Event6": {"rich_text": [{"text": {"content": events[5]}}]}
                }
            }
    elif len(events)==6:
        body = {
            "parent": {
                "database_id": databases_id},
            "properties": {
                    "Name": {"title": [{"text": {"content": name}}]},
                    "Gender": {"select": {"name": gender}},
                    "Country": {"rich_text": [{"text": {"content": country}}]},
                    "Event1": {"rich_text": [{"text": {"content": events[0]}}]},
                    "Event2": {"rich_text": [{"text": {"content": events[1]}}]},
                    "Event3": {"rich_text": [{"text": {"content": events[2]}}]},
                    "Event4": {"rich_text": [{"text": {"content": events[3]}}]},
                    "Event5": {"rich_text": [{"text": {"content": events[4]}}]},
                    "Event6": {"rich_text": [{"text": {"content": events[5]}}]}
                }
            }
    #response = requests.request('POST', url=get_request_url('pages'), headers=headers, data=json.dumps(body))

#pprint(response.json())

import requests
from pprint import pprint
import json


def get_request_url(end_point):
    return f'https://api.notion.com/v1/{end_point}'


notion_api_key = 'secret_3Cb6K5W7LhSnV8PWcnoMn2z2hn8HWgEB7QRc2kzBuTi'
#databases_id='fe569bf2d5cf47f89f69f3e755fb08fe'
headers = {"Authorization": f"Bearer {notion_api_key}",
           "Content-Type": "application/json",
           "Notion-Version": "2021-05-13"}

# #GET
# response = requests.request('GET', url=get_request_url(f'databases/{databases_id}'), headers=headers)
# pprint(response.json())
# pprint(response.json()['title'][0]['plain_text'])

databases_ids=[]
ken=[
#     'https://www.notion.so/fe569bf2d5cf47f89f69f3e755fb08fe?v=c752f4bc84d9467bbb267c06dccad52f',
#      'https://www.notion.so/87e32571d160491da161362c767eeba9?v=9c6ec4bcdeb8478bbf150edcbb59c9bf',
#     'https://www.notion.so/6793de134bef472994cf76d3c4f1f505?v=3b9c96bf2ec24b29992d7dd72dd95298',
#      'https://www.notion.so/0a848818dc6746bc9a9bcd9ca0fdaf76?v=c316c9193123445180b0109f072c6dec',
#      'https://www.notion.so/919277e2672042249eb2131686f30698?v=333d41f7101b496cbe0578c012ab6fe2',
#      'https://www.notion.so/4351cbbcaa4c4223a7b931c47ea7cb9a?v=4f55365f3bf64a0ea59423cd2ce5af61',
#      'https://www.notion.so/b95dc891559641a98278800608e08af9?v=35a508a4a8b34070849e6f1c82b46e12',
#      'https://www.notion.so/9858784f2b8f4e7bbf5df33270b4b05f?v=225ddbef898f4e8dbf9bbaacc92a5958',
#      'https://www.notion.so/4d3d6738f0024593ab90473e4d0d8d69?v=0ca1623db59f4edd99ce9288133461a0',
#      'https://www.notion.so/39de65a3b19e46a6b430fa1f0f6c7262?v=a9395c1de5b545bf8269a87296d1b270',
#      'https://www.notion.so/8dd3d16c6a0b430eae8e76a0be04959b?v=6d06ab8b632e4ccd9a7d25f230da3672',
#      'https://www.notion.so/52d3a94e3b96414f83996f073c321ec8?v=19b262a00d814cb0b1b1156fe27aa704',
# #      '',
#      'https://www.notion.so/825b480f5b3249a09564eeb234fe7555?v=1dd91584965e4bcfbcaa46c37883ee3c',
#      'https://www.notion.so/ec0f9e336aeb47d199dab22b176171dd?v=b1652a5e1abb4cf1834c4f3e41d9a371',
#      'https://www.notion.so/00587061c5aa45c980cb452d872f3dd9?v=48473edad8984b42ac85aba0936b09cd',
#      'https://www.notion.so/36e14f1488174d22a8c87460f09af9f9?v=9333c48f530540ed816c5c5afd7c23eb',
#      'https://www.notion.so/ee56f1e02ce6465c9f333146a6677f11?v=de5e80119ca149d7a4a483580ed298e6',
#      'https://www.notion.so/888523c2ea604f8e9a8d8c1c1a0353b1?v=7bc73bf51fee4433aad9c1b12cd40990',
#      'https://www.notion.so/c595da3ffe98446f8d1dd6833e6046d9?v=82559183c7a94d57ac1e4ac3612979dc',
#      'https://www.notion.so/8fc3a219f34c4303acb310ea53d833ec?v=46159d2fd1a54106b3a65e3014676165',
#      'https://www.notion.so/8cd28e3454064d269418369b89333789?v=5327259195e34d61a1248972c416b901',
#      'https://www.notion.so/746f6ac6099847718d24c6dc2dca2e28?v=b1be0699e8bb4779be1c47c37f1ae543',
#      'https://www.notion.so/4c4d4e28f9124a5bb4aea5c68e958335?v=fdbcd34cd4704beebb661afc5fc1d07e',
#      'https://www.notion.so/9ceead5b3ece423184443c198bff2287?v=818c6790dd834fd8995285ca68aa9b5e',
#      'https://www.notion.so/baa7bd720e45402db0954c0c8610e92c?v=336c6f66c6894f76881a34b7ccb8731e',
#      'https://www.notion.so/8725f00add29430ab0768efed62578ee?v=149bd6a0d0ed4b9b8750184455ddccd3',
#      'https://www.notion.so/611380f965c74639bfb994dd0f03d044?v=b894892261884aaf8ff7f0ab763dd7bb',
#     
    'https://www.notion.so/4e59b67954fd40daaf84205c6bc04a29?v=74763af04dda4b4aa30fba9c829f6379',
    'https://www.notion.so/404bad9a23114fde93209f838ba103a4?v=7f6b02363224474ea09d3bae7c53a302',
    'https://www.notion.so/39de65a3b19e46a6b430fa1f0f6c7262?v=a9395c1de5b545bf8269a87296d1b270',
    'https://www.notion.so/79b1727436684b898edd599f38454157?v=6effff534ffe455b8c0498b329da640a',
    'https://www.notion.so/8dd3d16c6a0b430eae8e76a0be04959b?v=6d06ab8b632e4ccd9a7d25f230da3672',
    'https://www.notion.so/52d3a94e3b96414f83996f073c321ec8?v=19b262a00d814cb0b1b1156fe27aa704',
]
point='?'
for i in range(len(ken)):
    ke=ken[i][22:].find(point)
    #print(ke)
    databases_ids.append(ken[i][22:][:ke])
databases_ids

for databases_id in databases_ids:
    response = requests.request('GET', url=get_request_url(f'databases/{databases_id}'), headers=headers)
    print(response.json()['title'][0]['plain_text'])
    tao=[]
    for i in range(N):
        if Event[i]==response.json()['title'][0]['plain_text']:
            tao.append([FullName[i],Country[i],ETime[i]])
    tao=np.array(tao)
    #print(len(tao))
    col_num = 2
    #print(tao[np.argsort(tao[:,col_num])])
    tao=tao[np.argsort(tao[:,col_num])]
    for i in range(0,len(tao))[::-1]:
        name=tao[i][0]
        country=tao[i][1]
        entrytime=tao[i][2]
        #print(name,country,entrytime)
        body = {
                    "parent": {
                        "database_id": databases_id},
                    "properties": {
                            "Name": {"title": [{"text": {"content": name}}]},
                            "Country": {"rich_text": [{"text": {"content": country}}]},
                            "Entry Time": {"rich_text": [{"text": {"content": entrytime}}]},

                        }
                    }
        #response = requests.request('POST', url=get_request_url('pages'), headers=headers, data=json.dumps(body))
        #pprint(response.json())
