import requests
from bs4 import BeautifulSoup

def get_menu():
  url = 'https://dise.udec.cl/node/171'
  dom = requests.get(url).text

  soup = BeautifulSoup(dom, 'html.parser')
  table = soup.find('table')
  rows = table.find_all('tr')
  rows = rows[1:6]

  raw_data = []
  for row in rows:
    col = row.get_text().strip()
    col = col.replace('\n', '').replace('      ', '')
    col = col.split(':')[-1]
    col = col.lower().capitalize()
    raw_data.append(col)

  data = {
    'Sopa/Ensalada': raw_data[0],
    'Alternativa I': raw_data[1],
    'Alternativa II': raw_data[2],
    'Postre I': raw_data[3],
    'Postre II': raw_data[4]
  }

  return data
