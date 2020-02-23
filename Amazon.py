from bs4 import BeautifulSoup as bs
from datetime import datetime
import time
import requests
from money_parser import price_dec as pd
from notify_run import Notify



def AmazonScraper(url,desired_price):

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    success=1
    now=datetime.now()
    current_time=now.strftime("%H:%M:%S")

    r=requests.get(url,headers=headers)
    soup=bs(r.content,'html5lib')
    test = soup.find('span', id ='priceblock_ourprice')
    if test is None:
	       test = soup.find('span', id ='priceblock_dealprice')

    price=int(pd((str(test))))
    print(price)

    if(price<desired_price):
        title=str(soup.find('span',id='productTitle').get_text().strip())
        message=title+" :::Price Decreased to :"+str(price)
        notify = Notify()
        notify.send(message)
        success=0

    return success






url=input("Enter the url:\n")
desired_price=int(input("Enter the desired price: \n"))

flag=1

while(flag):
    flag=AmazonScraper(url,desired_price)
    if(flag==1):
        print("Will fetch again after 10 minutes. To stop press ctl + c...")
        time.sleep(3600)
