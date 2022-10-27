import datetime
# getDateStrByStr, getDateObjByStr, getDateObjByDatetimeObj, getAPIDateStrByStr, getNextDateStrByObj, getPrevDateStrByObj
def lpad(i, width, fillchar='0'):
    """입력된 숫자 또는 문자열 왼쪽에 fillchar 문자로 패딩"""
    return str(i).rjust(width, fillchar)

def getDateObjByStr(date_string):
    """ YYYY-MM-DD format str to datetime.datetime object """
    year = int(date_string[0:4])
    month = int(date_string[5:7])
    day = int(date_string[8:10])
    return datetime.datetime(year=year, month=month, day=day)

def getDateStrByObj(datetime_obj):
    """ datetime.datetime object to YYYY-MM-DD format str"""
    return lpad(datetime_obj.year, 4) + "-" + lpad(datetime_obj.month, 2) + "-" + lpad(datetime_obj.day, 2)

def getDateStrByStr(date_string): 
    """ YYYYMMDD format str to YYYY-MM-DD format str """
    return date_string[0:4] + "-" + date_string[4:6] + "-" + date_string[6:8]

def getAPIDateStrByStr(date_string):
    """ YYYY-MM-DD format str to YYYYMMDD format str """
    return date_string[0:4] + date_string[5:7] + date_string[8:10]

def getDateStrToday():
    now = datetime.datetime.now()
    return getDateStrByObj(now)

def getDateObjByDatetimeObj(datetime_obj):
    return datetime.date(datetime_obj.year, datetime_obj.month, datetime_obj.day)

def getDateObjByStr(date_string):
    """ YYYY-MM-DD format str to Date obj """
    return datetime.date(int(date_string[0:4]), int(date_string[5:7]), int(date_string[8:10]))

def getNextDateAPIByObj(date_obj):
    date_obj = date_obj + datetime.timedelta(days=1)
    return getAPIDateStrByStr(getDateStrByObj(date_obj))
    
def getPrevDateAPIByObj(date_obj):
    date_obj = date_obj + datetime.timedelta(days=-1)
    return getAPIDateStrByStr(getDateStrByObj(date_obj))
