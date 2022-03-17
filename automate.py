import schedule
import time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import calendar
from matplotlib.lines import Line2D
import requests
import urllib3
import git

def job():
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    auth_url = "https://www.strava.com/oauth/token"
    activities_url = "https://www.strava.com/api/v3/athlete/activities"

    payload = {
        'client_id': "52225",
        'client_secret': 'b28faa026b0de1bd01196af43741764d0002925c',
        'refresh_token': '0fc931f79504e3a005c5d5065588435ab7daf681',
        'grant_type': "refresh_token",
        'f': 'json'
    }

    #print("Requesting Token...\n")
    res = requests.post(auth_url, data=payload, verify=False)
    access_token = res.json()['access_token']
    #print("Access Token = {}\n".format(access_token))

    header = {'Authorization': 'Bearer ' + access_token}
    param = {'per_page': 200, 'page': 1}
    data1 = requests.get(activities_url, headers=header, params=param).json()
    param = {'per_page': 200, 'page': 2}
    data2 = requests.get(activities_url, headers=header, params=param).json()
    param = {'per_page': 200, 'page': 3}
    data3 = requests.get(activities_url, headers=header, params=param).json()
    param = {'per_page': 200, 'page': 4}
    data4 = requests.get(activities_url, headers=header, params=param).json()
    param = {'per_page': 200, 'page': 5}
    data5 = requests.get(activities_url, headers=header, params=param).json()
    param = {'per_page': 200, 'page': 6}
    data6 = requests.get(activities_url, headers=header, params=param).json()
    param = {'per_page': 200, 'page': 7}
    data7 = requests.get(activities_url, headers=header, params=param).json()

    pd.set_option('display.max_rows', None)
    a = pd.DataFrame(data1)
    b = pd.DataFrame(data2)
    c = pd.DataFrame(data3)
    d = pd.DataFrame(data4)
    e = pd.DataFrame(data5)
    f = pd.DataFrame(data6)
    g = pd.DataFrame(data7)

    full = a.append(b, ignore_index=True)
    full = full.append(c, ignore_index=True)
    full = full.append(d, ignore_index=True)
    full = full.append(e, ignore_index=True)
    full = full.append(f, ignore_index=True)
    full = full.append(g, ignore_index=True)
    full = full.loc[::-1].reset_index().drop(columns = ['index'])
    full.to_csv("out.csv")

schedule.every().day.at("13:11").do(job)

while True:
    schedule.run_pending()
    time.sleep(60) # wait one minute














