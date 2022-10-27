import os
import requests
from django.shortcuts import HttpResponse, render
from . import models

kRX_KEY = os.environ.get("KRX_DATA_KEY")
baseURL = f"https://apis.data.go.kr/1160100/service/GetStockSecuritiesInfoService/getStockPriceInfo?serviceKey={kRX_KEY}&resultType=json"
headers = {
    "content-type": "application/json",
}


# Create your views here.
def index(request):
    print(baseURL)
    response = requests.get(baseURL, headers=headers, verify=False)
    print(response.json())
    return HttpResponse(response.content)


# YYYYMMDD format to YYYY-MM-DD format
def getDateString(date_string): 
    return date_string[0:4] + "-" + date_string[4:6] + "-" + date_string[6:8]


def stockInfoByName(request, name):
    url = baseURL + f"&itmsNm={name}"
    
    try:
        stock = models.stockKR.objects.get(name=name)
        # There is a stock record.
        response = requests.get(url, headers=headers, verify=False)
        print("Yes!")
        print(response.json())
        return HttpResponse(str(response.json()))
    except models.stockKR.DoesNotExist: # There is not a stock record. New try.
        response = requests.get(url, headers=headers, verify=False)
        resJSON  = response.json()
        print("No!")
        if resJSON['response']['body']['totalCount'] == 0:
            print("Invalid Name")
        else:
            items       = resJSON['response']['body']['items']['item']
            category    = items[0]['mrktCtg'] # marketCategory
            short_code  = items[0]['srtnCd']  # shortCode
            isin_code   = items[0]['isinCd']  # ISIN code
            first_date  = getDateString(items[0]['basDt'])   # pivot Date

            stock_target = models.stockKR.objects.create(name=name, category=category, short_code=short_code, isin_code=isin_code, first_date=first_date, last_date=first_date)

            for i, item in enumerate(items):
                # basDt, clpr, vs, fltRt, mkp, hipr, lopr, trqu, trPrc, lstgStCnt, mrktTotAmt, 
                # 기준일자, 종가, 대비, 등락률, 시가, 고가, 저가, 거래량, 거래금액, 상장주식수, 시가총액.
                dateString = getDateString(item['basDt'])
                models.krStockElementModel.objects.create(stock_type=stock_target,  date=dateString, 
                                                                                    start_price=item['mkp'],
                                                                                    end_price=item['clpr'],
                                                                                    high_price=item['hipr'],
                                                                                    low_price=item['lopr'],
                                                                                    trade_quant=item['trqu'],
                                                                                    trade_money=item['trPrc'],
                                                                                    total_stock_count=item['lstgStCnt'],
                                                                                    total_comp_price=item['mrktTotAmt']
                                                        )

        
    # stockType = models.ForeignKey("stockKR.stockKR", on_delete=models.CASCADE, related_name="daily_element")

    # date = models.DateField()

    # # Price Info.
    # start_price = models.IntegerField()
    # end_price = models.IntegerField()
    # high_price = models.IntegerField()
    # low_price = models.IntegerField()

    # # Trade quantity.
    # trade_quant = models.IntegerField()
    # trade_money = models.IntegerField()

    # # Macro Info.
    # total_stock_count = models.IntegerField()
    # total_comp_price = models.IntegerField()
                print(i, item)
            print("New Item!")
        return HttpResponse(str(response.json()))
