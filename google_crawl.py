from bs4 import BeautifulSoup
import requests
import datetime
import time
import random

def news_search(keyword, start_date, end_date, n_page):
  headers = {
      'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
  }
  nums = (n_page-1)*10

  # link = 'https://www.google.hr/search?q=' + keyword + '&hl=en&source=lnms&tbs=cdr:1,cd_min:'+ start_date +',cd_max:'+ end_date + '&tbm=nws&sa=X' + '&start=' + str(nums)
  # print(link)
  link = f'https://www.google.hr/search?q={keyword}&hl=en&source=lnms&tbs=sbd:1,cd_min:{start_date},cd_max:{end_date}&tbm=nws&sa=X&start={nums}'
  print(link)
  r = requests.get(link, headers=headers, timeout=3)
  soup = BeautifulSoup(r.text, 'html.parser')
  return soup

def crawler(link):
  headers = {
      'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
  }
  r = requests.get(link, headers=headers, timeout=3)
  soup = BeautifulSoup(r.text, 'html.parser')
  return soup

categories = [
    "政治", "經濟", "科技", "娛樂", "體育",
    "國際", "社會", "健康", "教育", "旅遊",
    "財經", "房地產", "環保", "文化", "軍事",
    "交通", "司法", "災難", "氣象", "美食"
]

selected = random.choice(categories)

links = []
my_data = []

cur_day = datetime.date.today()
one_day_ago = datetime.timedelta(days=1)
last_day = cur_day - one_day_ago

search = selected + "新聞"
start_date = cur_day.strftime("%m/%d/%Y")
end_date = last_day.strftime("%m/%d/%Y")
news_soup = news_search(search, start_date, end_date, 1)

for i in news_soup.select('.WlydOe')[1:]:
  ### 網址
  try:
    temp_soup = crawler(i['href'])
  except:
    print('error')

  ### 標題
  selection = 'p'
  temp_text = ''
  for j in temp_soup.select(selection):
    if (len(j.text) > 35) :
      temp_text += j.text
  links.append(i['href'])
  my_data.append(temp_text)


print(links)

with open('test.txt', 'w', encoding='cp950', errors='replace') as f:
    f.write(str(my_data))