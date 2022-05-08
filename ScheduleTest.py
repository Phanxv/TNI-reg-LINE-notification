import schedule as sch
import time
from datetime import datetime

today = datetime.now()

def check_date():
    if(today.date() == datetime(2022, 5, 8).date()) :
        print("Today is May 8th")

sch.every().day.at("19:48").do(check_date)

while True :
    sch.run_pending()
    time.sleep(3600)