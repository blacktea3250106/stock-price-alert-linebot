import requests
from bs4 import BeautifulSoup

# command ex: 2330 > 350
def price_alert(alert):

    code = alert.split()[0]
    operator = alert.split()[1]
    alert_price = float(alert.split()[2])

    url= 'https://pchome.megatime.com.tw/stock/sid' + code + '.html'

    headers = {
        'cookie': 'ECC=GoogleBot'
    }

    res = requests.post(url, headers=headers, data = {"is_check": "1"})
    soup = BeautifulSoup(res.text,'html.parser')
    price = float(soup.find('span', class_='data_close').text)
    change = soup.find('span', class_='data_diff').text
    percentage = soup.find_all('span', class_='data_diff')[1].text

    message = ""
    if operator == '>':
        if price > alert_price:
            message = alert + "\n" + str(price) + "(" + change + percentage + ")"
    elif operator == '<':
        if price < alert_price:
            message = alert + "\n" + str(price) + "(" + change + percentage + ")"

    return message
    
    

