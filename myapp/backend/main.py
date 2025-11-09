from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
 
from myapp.database.connect_db import get_db, engine, Base
from myapp.crud.test import fetch_data
from myapp.models.user import User

from fastapi.responses import HTMLResponse
import redis
import time 
import random

app = FastAPI()

Base.metadata.create_all(bind = engine)

# connect to redis

r = redis.Redis(host = "localhost", port=6379, db = 0, decode_responses = True)

# simulate expensive db call

def get_dashboard_data_from_db():
    print(" simulating  expensive db calls")
    time.sleep(3) # simulate delay (eg.. slow query)
    data = {
        "total_user" : random.randint(1000,2000),
        "total_sales" : random.randint(500, 1000),
        "conversion_rate": round(random.uniform(1.2, 2.5),2)
    }
    return data

# endpoint using redis cache

@app.get("/dashboard", response_class = HTMLResponse)
def get_dashboard():
    start = time.time()
    cache_key = "dashboarg_page_v1"
    cached_html = r.get(cache_key)

    if cached_html:
        duration = time.time() -start
        print(f"cache hit - returning cache dashboard in {duration: .3f}s ")
        return cached_html

    print("cache miss - fetching fresh data")
    data = get_dashboard_data_from_db()
     
    html = f"""
     <html>
     <head>
     <title>Dashboard</title>
     </head>
     <body>
     <h1> Business dashboard</h1>
     <p><b> Total users: </b> {data['total_user']}</p>

     <p><b> Total sales: </b> {data['total_sales']}</p>

     <p><b> Conversion rate : </b> {data['conversion_rate']}</p>
     <p style='color':gray;'> Generated at {time.strftime("%H:%M:%S")}</p>
     </body>
     </html>

     """

     # cache for 120 sec

    r.setex(cache_key, 120, html)
    duration = time.time() -start
    print(f"cache miss - returning non cache dashboard in {duration: .3f}s ")
    return html

@app.get('/details')
def get_data(db: Session = Depends(get_db)):
    data = db.query(User).all()  # simple query
    print(data)
    return data