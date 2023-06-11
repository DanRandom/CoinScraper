from bs4 import BeautifulSoup
import requests
import sys

def parse():
    url = "https://coinmarketcap.com/"

    result = requests.get(url)
    doc = BeautifulSoup(result.text, "html.parser")

    tbody = doc.tbody
    tableRows = tbody.contents

    prices = {}

    for tableRow in tableRows:
        name, price = tableRow.contents[2:4]
        if name.span:
            spans = name.find_all("span")
            fullName = spans[1].string
        else:
            fullName = name.p.string
        if price.a:
            fullPrice = price.a.string
        elif price.span:
            spanStr = str(price.span)
            if spanStr[18] == '.':
                fullPrice = spanStr[15:21]
            else:
                fullPrice = spanStr[15:19]
        
        prices[fullName] = fullPrice
    return prices

def search(*args):
    if len(args) == 1:
        name = args[0]
        prices = parse()
        coin = prices.get(name)
        if coin == None:
            print("ERROR: NO COIN FOUND")
        else:
            print(coin)
    elif len(args) == 2:
        prices = parse()
        coin1 = prices.get(args[0])
        if coin1 == None:
            print("ERROR: FIRST COIN NOT FOUND")
        coin2 = prices.get(args[1])
        if coin2 == None:
            print("ERROR: SECOND COIN NOT FOUND")
        if type(coin1) == str:
            coin1 = coin1[1:3] + coin1[4:]
            coin1 = float(coin1)
        if type(coin2) == str:
            coin2 = coin2[1:3] + coin2[4:]
            coin2 = float(coin2)
        if coin1 > coin2:
            print(args[0] + " $" + str(coin1))
        elif coin1 < coin2:
            print(args[1] + " $" + str(coin2))
        else:
            print("Coins are equally priced")

if len(sys.argv) == 1:
    print("ERROR: NO COIN NAME GIVEN")
elif len(sys.argv) == 2:
    search(sys.argv[1])
elif len(sys.argv) == 3:
    search(sys.argv[1], sys.argv[2])