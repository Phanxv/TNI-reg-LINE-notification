import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import schedule as sch
import time

html_text = requests.get('https://reg.tni.ac.th/registrar/calendar.asp')
html_text.encoding = 'TIS-620'
soup = BeautifulSoup(html_text.text, 'html.parser')
dataTable = soup.find_all('table')[4]

headers = ['','event','start','end']

calendarDataframe = pd.DataFrame(columns=headers)

for row in dataTable.find_all('tr')[1:]:
    data = row.find_all('td')
    row_data = [td.text for td in data]
    if len(row_data) != 4:
        row_data.append(row_data[2])
    lenght = len(calendarDataframe)
    calendarDataframe.loc[lenght] = row_data

#datetime(year, month, day, hour=0, minute=0, second=0, microsecond=0, tzinfo=None, *, fold=0)
now = datetime.today()

thaiMonth = {
    "ม.ค. " : 1,
    "ก.พ. " : 2,
    "มี.ค." : 3,
    "เม.ย." : 4,
    "พ.ค. " : 5,
    "มิ.ย." : 6,
    "ก.ค. " : 7,
    "ส.ค. " : 8,
    "ก.ย. " : 9,
    "ต.ค. " : 10,
    "พ.ย. " : 11,
    "ธ.ค. " : 12
}

notificationDates = []

for i in range(0,calendarDataframe.shape[0]):
    day = calendarDataframe.start[i][0:2]
    year = calendarDataframe.start[i][8:13]
    if int(year) < 1000 :
        year = calendarDataframe.start[i][7:12]
    try :
        month = calendarDataframe.start[i][3:8]
        notificationDates.append(datetime(int(year)-543,thaiMonth[month],int(day)))
    except KeyError:
        month = calendarDataframe.start[i][2:7]
        notificationDates.append(datetime(int(year)-543,thaiMonth[month],int(day)))

testNow = datetime(2022,5,19)

def notify() :
    for i in range(0,len(notificationDates)):
        if now.date() == notificationDates[i].date() :
            print(calendarDataframe.event[i])
        else :
            print("No event found today")
            break

sch.every().day.at("06:00").do(notify)

while True :
    sch.run_pending()
    time.sleep(3600)