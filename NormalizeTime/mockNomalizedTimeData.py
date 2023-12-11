import random
import pickle
import os
from tqdm import tqdm
from mockutils import *

ROOT = '.\\NormalizeTime\\TrainingData'

if not os.path.exists(ROOT):
    os.makedirs(ROOT)

special_token_dict : dict = {
    "bos_token" : "<|endoftext|>",
    "sep_token" : "<|SEP|>", 
    "eos_token" : "<|END|>",
    "pad_token" : "<|PAD|>"
    }

MOCK_TIME = 500000
# 定義日期相關欄位模板
DATE_TEMPLATE = ["%d/%m/%Y",
                "%#d/%#m/%Y",
                "%d/%m/%y",
                "%#d/%#m/%y",
                "%d.%m.%y",
                "%#d.%#m.%y",
                "%Y%m%d",
                "%d %B %Y",
                "%#d %B %Y",
                "%d-%b-%Y",
                "%#d-%b-%Y",
                "%Y",
                "%Y-%m",
                "%Y-%#m",
                "%B %Y",
                "%b %Y",
                'today',
                "%#d_th_ of %B %Y"]
# 定義時間相關欄位模板
TIME_TEMPLATE = [
    "%d/%m/%Y at %#H:%M",
    "%d/%m/%Y at %#I:%M%p",
    "%d/%m/%Y at %#I:%M %p",
    "%d/%m/%Y at %#I%p",
    "%d/%m/%Y at %#H:%M",
    "%d/%m/%Y at %H:%M", #14/02/2014 at 13:58
    "%#d/%#m/%Y at %#H:%M",
    "%Y-%m-%d %H:%M:%S",
    "%d.%m.%y on %#I:%M%p",
    "%#d.%#m.%y on %#I:%M%p",
    "%d.%m.%y on %#H:%Mhrs", 
    "%#d.%#m.%y on %#H:%Mhrs",
    "%#H.%M on %#d.%#m.%y", # 10.15 on 14.03.13
    "%#H%Mhrs on %d.%m.%y", 
    "%#H%Mhrs on %#d.%#m.%y", 
    "%#H:%Mhrs on %d.%m.%Y", # 11:43hrs on 29.08.2016
    "%#I:%M%p on %d/%m/%y",
    "%#I:%M%p on %#d/%#m/%y",
    "%#I:%M%p on %d.%m.%y",
    "%#I:%M %p on %d.%m.%y",
    "%#I:%M%p on %#d.%#m.%y",
    "%#I%M%p on %d.%m.%y", # 1010am on 26.12.18
    "%#I%p on %d.%m.%y",
    "%#I%p on %#d.%#m.%y",
    "%#H:%M on %d/%m/%y", 
    "%#H:%M on %#d/%#m/%y", 
    "%#I:%M%p on %d/%m/%Y",
    "%#I:%M%p on %#d/%#m/%Y",
    "%#I:%M%p on %d.%m.%Y",
    "%#I:%M%p on %#d.%#m.%Y",
    "%#I:%M%p %d.%m.%y", 
    "%#I:%M%p %#d.%#m.%y", 
    "%#I:%M%p on the %#d_th_ %B %Y",
    "%#I:%M%p onthe %#d_th_ %B %Y",
    "%#dth of %B %Y at %#I:%M%p"]

TEMPLATE = {'DATE' : DATE_TEMPLATE, 'TIME' : TIME_TEMPLATE}

candidatePHIList = ['DATE', "TIME"]
timeNormalizedDatas = []

for _ in tqdm(range(MOCK_TIME), desc="Mocking TimeNomarlizedDatas..."):
    PHI = random.choice(candidatePHIList)
    mockResult, mockNormalize = mockTimeSeries(
                                                phi = PHI, 
                                                year=random.randint(1970, 2070), 
                                                month=random.randint(1, 12), 
                                                day= random.randint(1, 31),
                                                hour = random.randint(0, 23),
                                                minute = random.randint(0, 59),
                                                second = random.randint(0, 59),
                                                template=TEMPLATE
                                                )
    resStr = f"{special_token_dict['bos_token']}{mockResult}{special_token_dict['sep_token']}{mockNormalize}{special_token_dict['eos_token']}"
    timeNormalizedDatas.append(resStr)

timeNormalizedDatas = list(set(timeNormalizedDatas))
print(f"The number of mockdata => {len(timeNormalizedDatas)}")
print(f"Sample 5 data to show")
print_sample(timeNormalizedDatas, sample_k = 5)
targetPath = os.path.join(ROOT, "timeNormalizedDatas.data")
print(f"Output data to {targetPath}")
with open(targetPath, 'wb') as f:
    pickle.dump(timeNormalizedDatas, f)

# specialTimeTemplate
specialNomarlizedDatas = []
for _ in tqdm(range(100000), desc="Mocking SpecialNomarlizedDatas..."):
    PHI = "TIME"
    mockResult, mockNormalize = mockTimeSeries(
                                                phi = PHI, 
                                                year=random.randint(1970, 3000), 
                                                month=random.randint(1, 12), 
                                                day= random.randint(1, 31),
                                                hour = 0,
                                                minute = 0,
                                                second = 0,
                                                template={"TIME" : ["%Y-%m-%d %H:%M:%S"]}
                                                )
    resStr = f"{special_token_dict['bos_token']}{mockResult}{special_token_dict['sep_token']}{mockNormalize}{special_token_dict['eos_token']}"
    specialNomarlizedDatas.append(resStr)
specialNomarlizedDatas = list(set(specialNomarlizedDatas))

print(f"The number of mockdata => {len(specialNomarlizedDatas)}")
print(f"Sample 5 data to show")
print_sample(specialNomarlizedDatas, sample_k = 5)
targetPath = os.path.join(ROOT, "specialNomarlizedDatas.data")
print(f"Output data to {targetPath}")
with open(targetPath, 'wb') as f:
    pickle.dump(specialNomarlizedDatas, f)

durationNormalizedDatas = list()
for _ in tqdm(range(MOCK_TIME), desc="Mocking DurationNormalizedDatas..."):
    PHI = "DURATION"
    mockResult, mockNormalize = generation_mock_duration()
    resStr = f"{special_token_dict['bos_token']}{mockResult}{special_token_dict['sep_token']}{mockNormalize}{special_token_dict['eos_token']}"
    durationNormalizedDatas.append(resStr)
durationNormalizedDatas = list(set(durationNormalizedDatas))

print(f"The number of mockdata => {len(durationNormalizedDatas)}")
print(f"Sample 5 data to show")
print_sample(durationNormalizedDatas, sample_k = 5)
targetPath = os.path.join(ROOT, "durationNormalizedDatas.data")
print(f"Output data to {targetPath}")
with open(targetPath, 'wb') as f:
    pickle.dump(durationNormalizedDatas, f)