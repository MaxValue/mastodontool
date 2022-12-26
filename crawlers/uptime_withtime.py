# -*- coding: utf-8 -*-
"""
Created on Sun Aug 14 17:42:15 2022

@author: Lenovo
"""

import pickle
import psycopg2
import requests
import time
import sys
import logging

logging.basicConfig(encoding="utf-8", level=logging.INFO)
logger = logging.getLogger(__name__)

sys.path.append('../mastodontool/mastodontool')
import settings

logger.info("Getting instances list")
with open("allinstances", "rb") as fp:   # Unpickling
    a = pickle.load(fp)

a = a[546::]

logger.info("Connecting to DB")
conn = psycopg2.connect(
    dbname=settings.DATABASES.get("default",{})["NAME"],
    user=settings.DATABASES.get("default",{})["USER"],
    password=settings.DATABASES.get("default",{})["PASSWORD"],
    host=settings.DATABASES.get("default",{})["HOST"],
)
cur = conn.cursor()

logger.info("Checking each server")
for i in a:
    #print(i)
    start = time.time()
    try:
        targetURL = f"https://{i}"
        logger.info(f"Checking server {targetURL!r}")
        web_response = requests.get(targetURL, timeout=20)
        status = web_response.status_code
        roundtrip = time.time() - start
        #print(status)
 
    except:
        logger.info(f"Check failed for server {targetURL!r}")
        status = web_response.status_code
        roundtrip = time.time() - start
        #print(status)
        
        
        #status = urllib.request.urlopen("https://" + i).getcode()
    #except OSError:
        #print("OSError")
    logger.debug("Adding result to DB")
    cur.execute("""INSERT INTO "uptime2" ("instance", "status", "date", "rtime") VALUES (%s, %s, current_timestamp, %s); """, (i, status, roundtrip))
    conn.commit()
