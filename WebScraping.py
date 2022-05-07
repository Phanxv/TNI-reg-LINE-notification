import requests
from bs4 import BeautifulSoup
import pandas as pd

html_text = requests.get('https://reg.tni.ac.th/registrar/calendar.asp')
html_text.encoding = 'TIS-620'
soup = BeautifulSoup(html_text.text, 'html.parser')
dataTable = soup.find_all('table')[4]

headers = ['','รายการ','วันเริ่ม','วันสุดท้าย']

df = pd.DataFrame(columns=headers)

for row in dataTable.find_all('tr')[1:]:
    data = row.find_all('td')
    row_data = [td.text.strip() for td in data]
    if len(row_data) != 4:
        row_data.append(row_data[2])
    lenght = len(df)
    df.loc[lenght] = row_data
    
print(df.รายการ[0] + " / " + df.วันเริ่ม[0] + " / " + df.วันสุดท้าย[0])
print(df.วันเริ่ม[0][0:2])