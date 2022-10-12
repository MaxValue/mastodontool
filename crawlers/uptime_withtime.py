# -*- coding: utf-8 -*-
"""
Created on Sun Aug 14 17:42:15 2022

@author: Lenovo
"""

import pickle
import psycopg2
import requests
import time



with open("allinstances", "rb") as fp:   # Unpickling
    a = pickle.load(fp)

a = a[546::]

conn = psycopg2.connect("dbname=dorina user=postgres password=1234")
cur = conn.cursor()


for i in a:
    #print(i)
    start = time.time()
    try:
        web_response = requests.get("https://" + i)
        status = web_response.status_code
        roundtrip = time.time() - start
        #print(status)
 
    except:
        status = web_response.status_code
        roundtrip = time.time() - start
        #print(status)
        
        
        #status = urllib.request.urlopen("https://" + i).getcode()
    #except OSError:
        #print("OSError")
    cur.execute("""INSERT INTO "uptime2" ("instance", "status", "date", "rtime") VALUES (%s, %s, current_timestamp, %s); """, (i, status, roundtrip))
    conn.commit()
