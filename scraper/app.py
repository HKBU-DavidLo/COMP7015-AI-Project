import requests
from lxml import html
import json
import csv

base_url = "http://www.aastocks.com/tc/stocks/market/ipo/listedipo.aspx?s=3&o=0&page="
stock_list = []

def write_to_csv(filename, data):
    headers = ['ticker', 'list_date', 'market_cap', 'lower_offer_pr', 'upper_offer_pr', 'final_offer_price', 'over_sub_ratio', 'allot_odds', 'firstday_return']
    path_location = '..\\DATA\\' + filename
    with open(path_location, 'w', encoding="utf-8", newline='') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(data)

def get(list_elements):
    try:
        return list_elements.pop(0)
    except:
        return 'NaN'

for i in range(1, 27):
    url = base_url + str(i)
    resp = requests.get(url=url, headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36'})

    tree = html.fromstring(html=resp.content)

    stocks = tree.xpath("//div[@id='IPOListed']/table/tbody/tr")

    for stock in stocks:
        price_range = get(stock.xpath(".//td[contains(@class, 'cls')][4]/text()"))
        if (len(price_range.split('-')) > 1):
            op_low = price_range.split('-')[0]
            op_high = price_range.split('-')[1]
        else:
            op_low = price_range
            op_high = price_range
        s = []
        s.append(get(stock.xpath(".//td[contains(@class, 'txt_l')]/a[contains(@class,'cls')]/text()"))) #ticker
        s.append(get(stock.xpath(".//td[contains(@class, 'cls')][1]/text()"))) #listing date
        s.append(get(stock.xpath(".//td[contains(@class, 'cls')][3]/text()"))) #market cap.
        s.append(op_low) # lower offer price
        s.append(op_high) # upper offer price
        s.append(get(stock.xpath(".//td[contains(@class, 'cls')][5]/text()"))) #final offer price
        s.append(get(stock.xpath(".//td[contains(@class, 'cls')][6]/text()"))) #over subscription ratio
        s.append(get(stock.xpath(".//td[contains(@class, 'cls')][8]/text()"))) #allotmnet odds
        s.append(get(stock.xpath(".//td[contains(@class, 'cls')][10]/span/text()"))) #first day return
        # s = {
        #     'list_date': get(stock.xpath(".//td[contains(@class, 'cls')][1]/text()")),
        #     'mkt_cap': get(stock.xpath(".//td[contains(@class, 'cls')][3]/text()")),
        #     'op_low': op_low,
        #     'op_high': op_high,
        #     'offer_price': get(stock.xpath(".//td[contains(@class, 'cls')][5]/text()")),
        #     'over_subcribe': get(stock.xpath(".//td[contains(@class, 'cls')][6]/text()")),
        #     'odds': get(stock.xpath(".//td[contains(@class, 'cls')][8]/text()")),
        #     'firstday_ret': get(stock.xpath(".//td[contains(@class, 'cls')][10]/span/text()"))
        # }

        stock_list.append(s)

write_to_csv('stock_file.csv', stock_list)