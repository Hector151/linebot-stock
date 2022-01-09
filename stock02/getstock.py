from urllib.request import urlopen
import pandas as pd
import requests
import json
from bs4 import BeautifulSoup
#from getdata import name2code
def detail(stock):
    result = list()  #最終結果
    #chang2code
    #stockcode = str(name2code(stock))  not all_stock
    #爬取
    url = "https://tw.stock.yahoo.com/q/q?s=" + stock
    response = requests.get(url)
    soup = BeautifulSoup(response.text.replace("加到投資組合", ""), "lxml")
    stock_date = soup.find("font", {"class":"tt"}).getText().strip()[-9:]  #資料日期
    tables = soup.find_all("table")[2]  #取得網頁中第三個表格(索引從0開始計算)
    tds = tables.find_all("td")[0:11]  #取得表格中0-10格 +11->6/8
    result.append((stock_date,) + tuple(td.getText().strip() for td in tds))
    scope = str(round((float(result[0][5]) - float(result[0][8])) / float(result[0][8]) * 100,2)) + '%'
    result[0] += (scope,)
    #json
    buyprice = '$' + result[0][4]
    sellprice = '$' + result[0][5]
    yesterdayprice = '$' + result[0][8]
    highestprice = '$' + result[0][10]
    lowestprice = '$' + result[0][11]
    time = result[0][0] + " " + result[0][2]
    targetjson = json.load(open('json/detail/alldetail.json', 'r', encoding='utf-8'))
    targetjson['body']['contents'][1]['text'] = result[0][1]
    targetjson['body']['contents'][2]['text'] = time
    targetjson['body']['contents'][4]['contents'][0]['contents'][1]['text'] = buyprice
    targetjson['body']['contents'][4]['contents'][1]['contents'][1]['text'] = sellprice
    targetjson['body']['contents'][4]['contents'][2]['contents'][1]['text'] = result[0][12]  #scope
    targetjson['body']['contents'][4]['contents'][3]['contents'][1]['text'] = yesterdayprice
    targetjson['body']['contents'][4]['contents'][4]['contents'][1]['text'] = highestprice
    targetjson['body']['contents'][4]['contents'][5]['contents'][1]['text'] = lowestprice
    targetjson['body']['contents'][6]['action']['uri'] = url
    
    return targetjson

detail('0050')