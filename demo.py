import requests
from bs4 import BeautifulSoup
import pandas as pd



baseUrl = 'https://www.etsy.com'

header = {
    'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:84.0) Gecko/20100101 Firefox/84.0'
}

productlink = []

for x in range(1 ,2):
    r = requests.get(f'https://www.etsy.com/c/clothing/womens-clothing/jackets-and-coats?ref=pagination&page={x}')
    soup = BeautifulSoup(r.content, 'lxml')

    productlist = soup.find_all('li', class_='wt-list-unstyled')

    for item in productlist:
        for link in item.find_all('a', href=True):
            productlink.append(link['href'])
etsylist = []
for link in productlink:
    r = requests.get(link, headers=header)
    soup = BeautifulSoup(r.content, 'lxml')

    name = soup.find('h1', class_='wt-text-body-03 wt-line-height-tight wt-break-word').text.strip()
    try:
        sales = soup.find('div', class_='wt-display-inline-flex-xs wt-align-items-center wt-flex-wrap wt-mb-xs-2').text.strip().split("\n")[0]
    except:
        sales = 'no sales'
    try:
        reviews = soup.find('h2', class_='wt-mr-xs-2 wt-text-body-03').text.strip()
    except:
        reviews = 'no reviews'
    try:
        ranting = soup.find('span', class_='wt-display-inline-block wt-mr-xs-1').text.strip()
    except:
        ranting = 'no ranting'
    description = soup.find('p', class_='wt-text-body-01 wt-break-word').text.strip()
    vintage  = soup.find('li', class_="wt-list-unstyled wt-display-flex-xs wt-align-items-flex-start").text.strip().split("Vintage")  
    materials  = soup.find('p', class_="wt-text-truncate").text.strip().split("Materials") 

    etsy = {
        'name': name,
        'sales': sales,
        'reviews': reviews,
        'ranting': ranting,
        'description': description,
        'materials': materials,
        'vintage': vintage
    }

    etsylist.append(etsy)
    print('Saving: ', etsy['name'])
df = pd.DataFrame(etsylist)
# print(df.head(15))