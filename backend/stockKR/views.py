import os, requests
from django.shortcuts import HttpResponse, render

kRX_KEY = os.environ.get("KRX_DATA_KEY")
baseURL = f"https://apis.data.go.kr/1160100/service/GetStockSecuritiesInfoService/getStockPriceInfo?serviceKey={kRX_KEY}&resultType=json"
headers = {
    'content-type': "application/json",
}

# Create your views here.
def index(request):
    print(baseURL)
    response = requests.get(baseURL, headers=headers, verify=False)
    print(response.json())
    return HttpResponse(response.content)

def stockInfoByName(request, name):
    url = baseURL + f"&itmsNm={name}"
    response = requests.get(url, headers=headers, verify=False)
    print(response.json())
    return HttpResponse(str(response.json()))