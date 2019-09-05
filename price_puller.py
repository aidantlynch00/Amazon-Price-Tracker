import mysql.connector
import requests
from lxml import html
from time import sleep
import datetime
import apt_connector



#Init User-Agent header to avoid Amazon detecting scraping
header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36"}

#Connect to database
apt_connecter = apt_connector.APT_Connector("amazon_price_tracker")

#Get list of tables in database
table_list = apt_connecter.list_tables()
#Store Amazon ASIN's taken from table names
ASIN_list = [table.split("_")[-1] for table in table_list]

#Loop through each product
for i in range(len(table_list)):
    page = requests.get("https://www.amazon.com/dp/" + ASIN_list[i], headers = header)

    #While to retry product page request if blocked by Amazon
    while True:
        try:
            #Pull data from HTML using XML paths
            doc = html.fromstring(page.content)
            xpath_price = '//span[contains(@id, "ourprice") or contains(@id, "saleprice")]/text()'
            xpath_available = '//div[@id="availability"]//text()'

            #Cut $ out of price and convert it into a floating point number
            price = float(doc.xpath(xpath_price)[0][1:])
            available = "in stock" in str(doc.xpath(xpath_available)).lower()

            print(price)
            print(available)

            #Break from retry loop if product details obtained
            break

        except Exception as e:
            print(e)
        
        sleep(5)

    sleep(15)

#Close connection
apt_connecter.close()















'''
THIS IS STUPID USE .strip() TO GET RID OF WHITESPACE
#Strips string of whitespace characters from returned xml strings
def clean_str(text):
    result = ""
    for i in range(len(text)):
        if not (text[i] == "\n" or text[i] == " "):
            result += text[i]

    return result
'''



r = requests.get('https://www.amazon.com/Sony-WF-1000XM3-Industry-Canceling-Wireless/dp/B07TD96LY2/ref=sr_1_5?crid=1TGZTV4ZO5W3O&keywords=sony+xm1000xm3&qid=1565461914&s=gateway&sprefix=sony+xm%2Caps%2C177&sr=8-5')
#print(r.content)