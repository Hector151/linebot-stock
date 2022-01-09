from urllib.request import urlopen
import pandas as pd
import requests
import json
import csv

def name2code(stock_number):
    with open('stockname.csv', 'r', newline='') as namefile:
        data = csv.DictReader(namefile)
        for row in data:
            if((stock_number == row['code']) | (stock_number == row['name'])):
                temp = row['code']
                print(temp)
                return temp
                break
        print("NOT DEFINED...")
        return 0

            

name2code('2330')