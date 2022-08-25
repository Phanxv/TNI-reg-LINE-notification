import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import schedule as sch
import time

html_text = requests.get('https://reg.tni.ac.th/registrar/calendar.asp')
html_text.encoding = 'TIS-620'
soup = BeautifulSoup(html_text.text, 'html.parser')
data_table = soup.find_all('table')[4]

calendar_dataframe = pd.DataFrame(columns = ['','event','start','end'])

LINE_token = 'LINE_TOKEN'
LINE_headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'Authorization': 'Bearer ' + LINE_token
}

for row in data_table.find_all('tr')[1:]:
    data = row.find_all('td')
    row_data = [td.text for td in data]
    if len(row_data) != 4:
        row_data.append(row_data[2])
    lenght = len(calendar_dataframe)
    calendar_dataframe.loc[lenght] = row_data

now = datetime.today()

thai_months = {
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

notification_dates = []

for i in range(0,calendar_dataframe.shape[0]):
    day = calendar_dataframe.start[i][0:2]
    year = calendar_dataframe.start[i][8:13]
    if int(year) < 1000 :
        year = calendar_dataframe.start[i][7:12]
    try :
        month = calendar_dataframe.start[i][3:8]
        notification_dates.append(datetime(int(year)-543,thai_months[month],int(day)))
    except KeyError:
        month = calendar_dataframe.start[i][2:7]
        notification_dates.append(datetime(int(year)-543,thai_months[month],int(day)))

def notify() :
    for i in range(0,len(notification_dates)):
        if now.date() == notification_dates[i].date() :
            print(calendar_dataframe.event[i][5:])
            message = '\n' + calendar_dataframe.event[i][5:] + '\n' + calendar_dataframe.start[i] + '\n' + calendar_dataframe.end[i]
            requests.post(url = 'https://notify-api.line.me/api/notify', data={'message':message}, headers=LINE_headers)
        else :
            print("วันนี้ไม่มีกิจกรรม")
            requests.post(url = 'https://notify-api.line.me/api/notify', data={'message':"วันนี้ไม่มีกิจกรรม"}, headers=LINE_headers)
            break

sch.every().day.at("06:00").do(notify)

while True :
    sch.run_pending()
    time.sleep(3600)
