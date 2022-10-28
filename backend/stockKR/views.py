import os
from django.http import JsonResponse
import requests
import datetime
from django.shortcuts import HttpResponse, render
from . import models
from .utils.date import getDateStrByStr, getDateObjByStr, getDateObjByDatetimeObj, getNextDateAPIByObj, getPrevDateAPIByObj
from .utils.logger import Logger

kRX_KEY = os.environ.get("KRX_DATA_KEY")
baseURL = f"https://apis.data.go.kr/1160100/service/GetStockSecuritiesInfoService/getStockPriceInfo?serviceKey={kRX_KEY}&resultType=json"
headers = {
    "content-type": "application/json",
}
res_headers = {
    "Access-Control-Allow-Origin": "http://localhost:8080"
}

# def index(request):
#     print(baseURL)
#     response = requests.get(baseURL, headers=headers, verify=False)
#     print(response.json())
#     return HttpResponse(response.content)

def index(request):
    return JsonResponse({"Hi" : "There?"})

def parseResponseAndCreate(stock_target, items, num):
    for i, item in enumerate(items, start=1):
        # basDt, clpr, vs, fltRt, mkp, hipr, lopr, trqu, trPrc, lstgStCnt, mrktTotAmt, 
        # 기준일자, 종가, 대비, 등락률, 시가, 고가, 저가, 거래량, 거래금액, 상장주식수, 시가총액.
        dateString = getDateStrByStr(item['basDt'])
        dateObj    = getDateObjByStr(dateString)
        try:
            models.krStockElementModel.objects.get(stock_type=stock_target, date=dateObj)
            # already exist.
        except models.krStockElementModel.DoesNotExist:
            models.krStockElementModel.objects.create(stock_type=stock_target,  date=dateObj, 
                                                                                start_price=item['mkp'], end_price=item['clpr'],
                                                                                high_price=item['hipr'], low_price=item['lopr'],
                                                                                trade_quant=item['trqu'], trade_money=item['trPrc'],
                                                                                total_stock_count=item['lstgStCnt'], total_comp_price=item['mrktTotAmt']
                                                    )
            if stock_target.last_date < dateObj:
                stock_target.last_date = dateObj
            if dateObj < stock_target.first_date:
                stock_target.first_date = dateObj
            stock_target.save()
        if i == num:
            return

def stockInfoByName(request, name, fetchNum):
    logger = Logger()
    if fetchNum <= 0:
        return HttpResponse("Wrong fetchNum", status=400)
    
    fetchedNum = 0
    url = baseURL + f"&itmsNm={name}&numOfRows={fetchNum}"
    
    try:
        stock_target = models.stockKR.objects.get(name=name)
        # There is a stock record.
        last_day = stock_target.last_date
        first_day = stock_target.first_date

        if getDateObjByDatetimeObj(datetime.datetime.now()) > last_day:
            url_later = url + f"&beginBasDt={getNextDateAPIByObj(last_day)}"
            response = requests.get(url_later, headers=headers, verify=False)
            resJSON  = response.json()
            resITEM  = resJSON['response']['body']['items']['item']
            logger.debug(f"-fechedNumAfterDay : {len(resITEM)}")
            parseResponseAndCreate(stock_target, resJSON['response']['body']['items']['item'], fetchNum)
            fetchedNum += len(resITEM)
        
        if fetchedNum < fetchNum:
            url_before = url + f"&endBasDt={getPrevDateAPIByObj(first_day)}"
            response = requests.get(url_before, headers=headers, verify=False)
            resJSON  = response.json()
            resITEM  = resJSON['response']['body']['items']['item']
            logger.debug(f"-fechedNumBeforeDay : {len(resITEM)}")
            parseResponseAndCreate(stock_target, resJSON['response']['body']['items']['item'], fetchNum - fetchedNum)  
            fetchedNum += len(resITEM)
        logger.debug(f"Successfully fetched {fetchedNum} elements of {name}")
        return HttpResponse(str(response.json()))
    except models.stockKR.DoesNotExist: # There is not a stock record. New try.
        response = requests.get(url, headers=headers, verify=False)
        resJSON  = response.json()
        if resJSON['response']['body']['totalCount'] == 0:
            logger.debug(f"Invalid Name! : {name}")
        else:
            items       = resJSON['response']['body']['items']['item']
            category    = items[0]['mrktCtg'] # marketCategory
            short_code  = items[0]['srtnCd']  # shortCode
            isin_code   = items[0]['isinCd']  # ISIN code
            first_date  = getDateObjByStr(getDateStrByStr(items[0]['basDt']))   # pivot Date

            stock_target = models.stockKR.objects.create(name=name, category=category, short_code=short_code, isin_code=isin_code, first_date=first_date, last_date=first_date)
            parseResponseAndCreate(stock_target, items, fetchNum)
            logger.debug(f"New Stock was Registered! : {name}")
        return HttpResponse(str(response.json()))

def api_stockInfo(request):
    response = requests.get(os.environ.get("SELF_ROOT") + "/stockKR/", headers=headers, verify=False)
    resJSON  = response.json()
    resJSON["Hi"] += str(datetime.datetime.now())
    return JsonResponse(resJSON, headers=res_headers)