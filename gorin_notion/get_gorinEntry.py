from selenium import webdriver
driver_path = '/Users/kt/opt/anaconda3/lib/python3.8/site-packages/chromedriver_binary/chromedriver'
driver = webdriver.Chrome(driver_path)
driver.get('https://olympics.com/tokyo-2020/olympic-games/en/results/swimming/olympic-schedule-and-results.htm')
import requests
from pprint import pprint
import json


def get_request_url(end_point):
    return f'https://api.notion.com/v1/{end_point}'
notion_api_key = 'secret_3Cb6K5W7LhSnV8PWcnoMn2z2hn8HWgEB7QRc2kzBuTi'
headers = {"Authorization": f"Bearer {notion_api_key}",
           "Content-Type": "application/json",
           "Notion-Version": "2021-05-13"}
databases_ids=['https://www.notion.so/6db875c104084e0caa0d50671ecdca5f?v=d20e23e1c2d848e7b4acc0fa16de9752']
databases_id=databases_ids[0][22:][:databases_ids[0][22:].find('?')]
response = requests.request('GET', url=get_request_url(f'databases/{databases_id}'), headers=headers)
#pprint(response.json())

#driver.set_window_size(500,500)
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time
wait_time = 30
class_name="clickable-schedule-row"
# 全てのエレメントが現れるまで待機する
#WebDriverWait(driver, 15).until(EC.presence_of_all_elements_located)

class_elems=driver.find_elements_by_class_name(class_name)
links,time,event,kumi=[],[],[],[]
for elem in class_elems:
    s=elem.text
    u=s.split()
    #print(u)
    tim=u[0]
    tmp=u[4:17]
    #print(tmp)
    if "Heat" in tmp:
        po=tmp.index('-')
        par=' '.join(tmp[po+1:])
        eve=' '.join(tmp[:po])
    elif "Semifinal" in tmp:
        po=tmp.index('Semifinal')
        par=' '.join(tmp[po])
        eve=' '.join(tmp[:po])
    elif "Final" in tmp:
        po=tmp.index("Final")
        par=' '.join(tmp[po])
        eve=' '.join(tmp[:po])
    #print(tim,par,eve)
    links.append(elem.find_element_by_tag_name('a').get_attribute("href"))
    time.append(tim)
    event.append(eve)
    kumi.append(par)

# times=[elem.text[:elem.text.find(' ')] for elem in class_elems] 
# event=[elem.text[elem.text.find('\n')+1:elem.text.find('-')-1] for elem in class_elems] 
# kumi=[elem.text[elem.text.find('-')+2:] for elem in class_elems] 
#print(links)
# print(times)
# print(event)
# print(kumi)

elem=links[33]
driver.implicitly_wait(wait_time) # 秒
print(elem)
#driver.get(elem)
driver.get(elem)
#elem.click()
info=[]
k=driver.find_element_by_class_name("table-result").find_element_by_tag_name("tbody").find_elements_by_tag_name('tr')#.find_element_by_class_name(i).find_element_by_class_name("align-middle").get_attribute('innerText')
print(event[33][-5:].split())
if event[33][-5:]!='Relay':
    for ta in k:
        o=ta.find_elements_by_class_name("align-middle")#.get_attribute('innerText')
        for j in range(len(o)):
            if j==1:
                info.append(o[j].find_element_by_class_name('box').find_element_by_class_name('noc').get_attribute('innerText'))
                info.append(o[j].find_element_by_class_name('box').find_element_by_class_name('name').find_element_by_class_name('d-md-inline').get_attribute('innerText'))
                continue
            info.append(o[j].get_attribute('innerText'))
    body = {
                "parent": {
                    "database_id": databases_id},
                "properties": {
                        "Event": {"title": [{"text": {"content": event[i]}}]},
                        #"Gender": {"multi_select": {"name": gender}},
                        "Party": {"rich_text": [{"text": {"content": kumi[i]}}]},
                        "Time": {"rich_text": [{"text": {"content": time[i]}}]},
                }}
else:
    k=driver.find_element_by_class_name("table-result")
    #print(k.get_attribute('innerText'))
    k=k.find_element_by_tag_name("tbody").find_elements_by_tag_name("tr")#
    for i in range(len(k)):
        tao=k[i].get_attribute('innerText').split()
        print(i,tao)
        #print("\n\n")
        #info.append(tao[0])
        #print(k[i].get_attribute('innerText').split())
        if i%7==0:
            #tao=k[i].get_attribute('innerText').split()
            print(tao[0])
            print(tao[1][:3])
            print(tao[-1])
            info.append(tao[0])
            info.append(tao[1][:3])
            info.append(tao[-1])
        if i%7==3 or i%7==6 or i%7==5 or i%7==4:
            print(i,tao)
            info.append(tao[0]+' '+tao[-1])
            
#         body = {
#                     "parent": {
#                         "database_id": databases_id},
#                     "properties": {
#                             "Event": {"title": [{"text": {"content": event[i]}}]},
#                             #"Gender": {"multi_select": {"name": gender}},
#                             "Party": {"rich_text": [{"text": {"content": kumi[i]}}]},
#                             "Time": {"rich_text": [{"text": {"content": time[i]}}]},
#                     }}
#     print(info)
#     for i in range(0,len(info),7):
#         now=i
#         print(info[now])
#         lane=int(info[now].replace('\n',''))
#         if lane==1:
#             #lanedict={"properties":{"Lane1":{"rich_text": [{"text": {"content": info[now+2]+'('+info[now+1]+')'}}]}}}
#             lanedict={"Lane1":{"rich_text": [{"text": {"content": info[now+1]+'\n'+info[now+2]+'\n'+info[now+3]+'\n'+info[now+4]+'\n'+info[now+5]}}]}}
#             body["properties"].update(lanedict)

#         elif lane==2:
#             lanedict={"Lane2":{"rich_text": [{"text": {"content": info[now+1]+'\n'+info[now+2]+'\n'+info[now+3]+'\n'+info[now+4]+'\n'+info[now+5]}}]}}
#             body["properties"].update(lanedict)

#         elif lane==3:
#             lanedict={"Lane3":{"rich_text": [{"text": {"content":info[now+1]+'\n'+info[now+2]+'\n'+info[now+3]+'\n'+info[now+4]+'\n'+info[now+5]}}]}}
#             body["properties"].update(lanedict)
#         elif lane==4:
#             lanedict={"Lane4":{"rich_text": [{"text": {"content": info[now+1]+'\n'+info[now+2]+'\n'+info[now+3]+'\n'+info[now+4]+'\n'+info[now+5]}}]}}
#             body["properties"].update(lanedict)
#         elif lane==5:
#             lanedict={"Lane5":{"rich_text": [{"text": {"content": info[now+1]+'\n'+info[now+2]+'\n'+info[now+3]+'\n'+info[now+4]+'\n'+info[now+5]}}]}}
#             body["properties"].update(lanedict)
#         elif lane==6:
#             lanedict={"Lane6":{"rich_text": [{"text": {"content": info[now+1]+'\n'+info[now+2]+'\n'+info[now+3]+'\n'+info[now+4]+'\n'+info[now+5]}}]}}
#             body["properties"].update(lanedict)
#         elif lane==7:
#             lanedict={"Lane7":{"rich_text": [{"text": {"content": info[now+1]+'\n'+info[now+2]+'\n'+info[now+3]+'\n'+info[now+4]+'\n'+info[now+5]}}]}}
#             body["properties"].update(lanedict)
#         elif lane==8:
#             lanedict={"Lane8":{"rich_text": [{"text": {"content": info[now+1]+'\n'+info[now+2]+'\n'+info[now+3]+'\n'+info[now+4]+'\n'+info[now+5]}}]}}
#             body["properties"].update(lanedict)
#     #print(body)
# print(info)

for i,elem in enumerate(links):
    #driver.implicitly_wait(wait_time) # 秒
    print(elem)
    #driver.get(elem)
    driver.get(elem)
    #elem.click()
    info=[]#info(lane,country,name,time)
    k=driver.find_element_by_class_name("table-result").find_element_by_tag_name("tbody").find_elements_by_tag_name('tr')#.find_element_by_class_name(i).find_element_by_class_name("align-middle").get_attribute('innerText')
    if event[i][-5:]!='Relay':
        for ta in k:
            o=ta.find_elements_by_class_name("align-middle")#.get_attribute('innerText')
            for j in range(len(o)):
                if j==1:
                    info.append(o[j].find_element_by_class_name('box').find_element_by_class_name('noc').get_attribute('innerText'))
                    info.append(o[j].find_element_by_class_name('box').find_element_by_class_name('name').find_element_by_class_name('d-md-inline').get_attribute('innerText'))
                    continue
                info.append(o[j].get_attribute('innerText'))
        body = {
                    "parent": {
                        "database_id": databases_id},
                    "properties": {
                            "Event": {"title": [{"text": {"content": event[i]}}]},
                            #"Gender": {"multi_select": {"name": gender}},
                            "Party": {"rich_text": [{"text": {"content": kumi[i]}}]},
                            "Time": {"rich_text": [{"text": {"content": time[i]}}]},
                    }}
        print(info)
        for i in range(0,len(info),4):
            now=i
            lane=int(info[now].replace('\n',''))
            if lane==1:
                #lanedict={"properties":{"Lane1":{"rich_text": [{"text": {"content": info[now+2]+'('+info[now+1]+')'}}]}}}
                lanedict={"Lane1":{"rich_text": [{"text": {"content": info[now+2]+'('+info[now+1]+')'}}]}}
                body["properties"].update(lanedict)

            elif lane==2:
                lanedict={"Lane2":{"rich_text": [{"text": {"content": info[now+2]+'('+info[now+1]+')'}}]}}
                body["properties"].update(lanedict)

            elif lane==3:
                lanedict={"Lane3":{"rich_text": [{"text": {"content": info[now+2]+'('+info[now+1]+')'}}]}}
                body["properties"].update(lanedict)
            elif lane==4:
                lanedict={"Lane4":{"rich_text": [{"text": {"content": info[now+2]+'('+info[now+1]+')'}}]}}
                body["properties"].update(lanedict)
            elif lane==5:
                lanedict={"Lane5":{"rich_text": [{"text": {"content": info[now+2]+'('+info[now+1]+')'}}]}}
                body["properties"].update(lanedict)
            elif lane==6:
                lanedict={"Lane6":{"rich_text": [{"text": {"content": info[now+2]+'('+info[now+1]+')'}}]}}
                body["properties"].update(lanedict)
            elif lane==7:
                lanedict={"Lane7":{"rich_text": [{"text": {"content": info[now+2]+'('+info[now+1]+')'}}]}}
                body["properties"].update(lanedict)
            elif lane==8:
                lanedict={"Lane8":{"rich_text": [{"text": {"content": info[now+2]+'('+info[now+1]+')'}}]}}
                body["properties"].update(lanedict)
        #print(body)
        response = requests.request('POST', url=get_request_url('pages'), headers=headers, data=json.dumps(body))
        #driver.back()
    else:
        #info(lane,country,time,name,name,name,name,)
        k=driver.find_element_by_class_name("table-result")
        #print(k.get_attribute('innerText'))
        k=k.find_element_by_tag_name("tbody").find_elements_by_tag_name("tr")#
        for j in range(len(k)):
            tao=k[j].get_attribute('innerText').split()
            #print(tao)
            #print("\n\n")
            #info.append(tao[0])
            #print(k[i].get_attribute('innerText').split())
            if j%7==0:
                #tao=k[i].get_attribute('innerText').split()
                info.append(tao[0])
                info.append(tao[1][:3])
            if j%7==3 or j%7==6 or j%7==5 or j%7==4:
                info.append(tao[0]+' '+tao[-1])
        
        body = {
                    "parent": {
                        "database_id": databases_id},
                    "properties": {
                            "Event": {"title": [{"text": {"content": event[i]}}]},
                            #"Gender": {"multi_select": {"name": gender}},
                            "Party": {"rich_text": [{"text": {"content": kumi[i]}}]},
                            "Time": {"rich_text": [{"text": {"content": time[i]}}]},
                    }}
        print(info)
        for i in range(0,len(info),6):
            now=i
            lane=int(info[now].replace('\n',''))
            if lane==1:
                #lanedict={"properties":{"Lane1":{"rich_text": [{"text": {"content": info[now+2]+'('+info[now+1]+')'}}]}}}
                lanedict={"Lane1":{"rich_text": [{"text": {"content": info[now+1]+'\n'+info[now+2]+'\n'+info[now+3]+'\n'+info[now+4]+'\n'+info[now+5]}}]}}
                body["properties"].update(lanedict)

            elif lane==2:
                lanedict={"Lane2":{"rich_text": [{"text": {"content": info[now+1]+'\n'+info[now+2]+'\n'+info[now+3]+'\n'+info[now+4]+'\n'+info[now+5]}}]}}
                body["properties"].update(lanedict)

            elif lane==3:
                lanedict={"Lane3":{"rich_text": [{"text": {"content":info[now+1]+'\n'+info[now+2]+'\n'+info[now+3]+'\n'+info[now+4]+'\n'+info[now+5]}}]}}
                body["properties"].update(lanedict)
            elif lane==4:
                lanedict={"Lane4":{"rich_text": [{"text": {"content": info[now+1]+'\n'+info[now+2]+'\n'+info[now+3]+'\n'+info[now+4]+'\n'+info[now+5]}}]}}
                body["properties"].update(lanedict)
            elif lane==5:
                lanedict={"Lane5":{"rich_text": [{"text": {"content": info[now+1]+'\n'+info[now+2]+'\n'+info[now+3]+'\n'+info[now+4]+'\n'+info[now+5]}}]}}
                body["properties"].update(lanedict)
            elif lane==6:
                lanedict={"Lane6":{"rich_text": [{"text": {"content": info[now+1]+'\n'+info[now+2]+'\n'+info[now+3]+'\n'+info[now+4]+'\n'+info[now+5]}}]}}
                body["properties"].update(lanedict)
            elif lane==7:
                lanedict={"Lane7":{"rich_text": [{"text": {"content": info[now+1]+'\n'+info[now+2]+'\n'+info[now+3]+'\n'+info[now+4]+'\n'+info[now+5]}}]}}
                body["properties"].update(lanedict)
            elif lane==8:
                lanedict={"Lane8":{"rich_text": [{"text": {"content": info[now+1]+'\n'+info[now+2]+'\n'+info[now+3]+'\n'+info[now+4]+'\n'+info[now+5]}}]}}
                body["properties"].update(lanedict)
        #print(body)
        response = requests.request('POST', url=get_request_url('pages'), headers=headers, data=json.dumps(body))
        #driver.back()
