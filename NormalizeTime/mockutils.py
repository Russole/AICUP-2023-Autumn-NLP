import datetime
import random

def print_sample(seq : list, sample_k : int = 2, title = False):
    for data in random.sample(seq, sample_k):
        if title:
            data = data.title()
        print(data)

def mockTimeSeries(phi : str , year : int, month : int, day : int, hour : int, minute : int, second : int, template : dict[str, list]):
    '''
        生成時間系列(日期、時間)等虛擬資料

            Parameters:

                phi(str) : 控制生成的phi(DATE | TIME)
                year : 指定年份
                month : 指定月份(1-12)
                day : 指定日期(1-31)
                hour : 指定時間
                minute : 指定分鐘
                second : 指定秒數
                template : 模板 規範格式 {"TIME" : [...], "DATE" : [...]}

            Return:

                mockResult, mockNormalize : 時間資料, 時間正規化資料
    '''
    while(True):
            try:
                datetime.date(year=year, month=month, day=day)
                break
            except:             
                if day > 1:
                    day = day - 1
                else:
                    break
    
    if phi == 'DATE':
        return mockDate(year = year, month = month, day = day, dateTemplate = template[phi])

    if phi == 'TIME':
        if month == 0:
            month += 1
        if day == 0:
            day += 1
        return mockDateTime(year = year, month = month, day = day, hour = hour, minute = minute, second = second, timeTemplates = template[phi])
    
    return None, None

def mockDate(year : int, month : int, day : int, dateTemplate : list[str] = None) -> (str, str):
    '''
        生成指定日期
            Parameters:
                    year : 指定年份
                    month : 指定月份(1-12)
                    day : 指定日期(1-31)
                    dateTemplate : 時間模板 [...]

            Return:
                mockResult, mockNormalize : 時間資料, 時間正規化資料
    '''
    
    if dateTemplate == None:
        return
    date : datetime.date = None
    # if month and day exist use common normalized
    # else use year
    selectTemplate = ""

    if day == 0:
        day = day + 1
    if month == 0:
        month = month + 1
    
    date = datetime.date(year=year, month=month, day=day)

    if day >= 3:
        selectTemplate = random.choice(dateTemplate)
    else:
        selectTemplate = random.choice(dateTemplate[:-1])

    if selectTemplate == 'today':
        dateNormalized = "%Y-%m-%d"
        date = datetime.date(year=2063, month=8, day=21)
        mockResult = date.strftime(selectTemplate)
        mockNormalize = date.strftime(dateNormalized)
        return mockResult, mockNormalize

    if '_th_' in selectTemplate:

        if day % 10 == 1:
            selectTemplate = selectTemplate.replace('_th_', 'st')
        elif day % 10 == 2:
            selectTemplate = selectTemplate.replace('_th_', 'nd')
        elif day % 10 == 3:
            selectTemplate = selectTemplate.replace('_th_', 'rd')
        else:
            selectTemplate = selectTemplate.replace('_th_', 'th')

    if ("%d" in selectTemplate or "%#d" in selectTemplate):
        dateNormalized = "%Y-%m-%d"
    elif ("%m" in selectTemplate or 
          "%b" in selectTemplate or 
          "%B" in selectTemplate or
          "%#m" in selectTemplate):
        dateNormalized = "%Y-%m"
    else:
        dateNormalized = "%Y"

    if "%y" in selectTemplate and (year / 100) == 19:
        selectTemplate.replace("%y", "%Y")
        
    mockResult = date.strftime(selectTemplate)
    mockNormalize = date.strftime(dateNormalized)
    return mockResult, mockNormalize

def mockDateTime(year : int, month : int, day : int, hour : int, minute : int, second : int, timeTemplates : list[str] = None) -> (str, str):
    '''
        生成指定時間
            Parameters:
                year : 指定年份
                month : 指定月份(1-12)
                day : 指定日期(1-31)
                hour : 指定時間
                minute : 指定分鐘
                second : 指定秒數
                dateTemplate : 時間模板 [...]

            Return:
                mockResult, mockNormalize : 時間資料, 時間正規化資料
    '''
    if timeTemplates == None:
        return
    selectTemplate = random.choice(timeTemplates)

    if day == 0:
        day = day + 1
    if month == 0:
        month = month + 1

    if '_th_' in selectTemplate:
        if day % 10 == 1:
            selectTemplate = selectTemplate.replace('_th_', 'st')
        elif day % 10 == 2:
            selectTemplate = selectTemplate.replace('_th_', 'nd')
        elif day % 10 == 3:
            selectTemplate = selectTemplate.replace('_th_', 'rd')
        else:
            selectTemplate = selectTemplate.replace('_th_', 'th')

    # if(random.random() > 0.5) and "%Y-%m-%d" in selectTemplate:
    #     hour = 0
    #     minute = 0
    #     second = 0
        
    if "%S" in selectTemplate or "%#S" in selectTemplate:
        normalizeTemplate = "%Y-%m-%dT%H:%M:%S"
    elif "%M" in selectTemplate or "%#M" in selectTemplate:
        normalizeTemplate = "%Y-%m-%dT%H:%M"
    else:
        normalizeTemplate = "%Y-%m-%dT%H"
    dateTime : datetime.datetime = datetime.datetime(year=year, month=month, day=day, hour=hour, minute=minute, second=second)
    
    if "%y" in selectTemplate and (year / 100) == 19:
        selectTemplate.replace("%y", "%Y")

    mockResult = ""
    mockNormalize = ""

    mockResult = dateTime.strftime(selectTemplate)
    mockNormalize = dateTime.strftime(normalizeTemplate)
    return mockResult.lower(), mockNormalize

def generation_mock_duration(
        candidate_units = ['year', 'week', 'day', 'month', 'years', 'weeks', 'days', 'months', 'yr', 'yrs', 'wk', 'wks'],
        duration_nums = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', 'one', 'two', 'three', 'four', 'five'],
        toDigits = {
        '1' : 1,
        '2' : 2,
        '3' : 3,
        '4' : 4,
        '5' : 5,
        '6' : 6,
        '7' : 7,
        '8' : 8,
        '9' : 9,
        '10' : 10,
        '11' : 11,
        '12' : 12,
        '13' : 13,
        '14' : 14,
        '15' : 15,
        '16' : 16,
        'one' : 1,
        'two' : 2,
        'three' : 3,
        'four' : 4,
        'five' : 5
        }
        ):
    
    num : str = random.choice(duration_nums)

    unit : str = random.choice(candidate_units)
    toFlag = random.randint(0, 1)

    if num.isdigit():
        sep = random.choice(['', ' '])
    else :
        sep = ''
    if toFlag == 0:
        duration_t = f"{num}{sep}{unit}"
    else:
        duration_t = f"{toDigits[num]}-{toDigits[num] + 1}{sep}{unit}"
    if toFlag == 0:
        if 'year' in unit or 'yr' in unit:
            duration_nt = f"P{toDigits[num]}Y"
        elif 'month' in unit:
            duration_nt = f"P{toDigits[num]}M"
        elif 'week' in unit:
            duration_nt = f"P{toDigits[num]}W"
        else:
            duration_nt = f"P{toDigits[num]}D"
    else:
        if 'year' in unit or 'yr' in unit:
            duration_nt = f"P{(toDigits[num] + toDigits[num] + 1)/ 2.}Y"
        elif 'month' in unit:
            duration_nt = f"P{(toDigits[num] + toDigits[num] + 1)/ 2.}M"
        elif 'week' in unit:
            duration_nt = f"P{(toDigits[num] + toDigits[num] + 1)/ 2.}W"
        else:
            duration_nt = f"P{(toDigits[num] + toDigits[num] + 1)/ 2.}D"

    return duration_t, duration_nt