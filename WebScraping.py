from selenium import webdriver
import requests
from bs4 import BeautifulSoup
import pandas as pd

html_text = requests.get('https://reg.tni.ac.th/registrar/calendar.asp')
html_text.encoding = 'TIS-620'
soup = BeautifulSoup(html_text.text, 'html.parser')
dataTable = soup.find('table')

headers = ['รายการ','วันเริ่ม','วันสุดท้าย']

df = pd.DataFrame(columns=headers)

for row in dataTable.find_all('tr')[1:]:
    data = row.find_all('td')
    row_data = [td.text.strip() for td in data]
    lenght = len(df)
    df.loc[lenght] = row_data