import os
import datetime
from g4f.client import Client
import time

from bs4 import BeautifulSoup
import requests
import datetime
import time
import random

"""
---
layout: post
author: AI
image: assets/images/11.jpg
"""


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

import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen
import re

def image_search(keyword, headers):
    link = 'https://www.google.hr/search?q=' + keyword + '&hl=en&source=lnms&tbm=isch&sa=X'
    r = requests.get(link, headers=headers)
    soup = BeautifulSoup(r.text, 'html.parser')
    return soup
def save_img(save_folder, link):
  img = urlopen(link)
  with open(save_folder + '/' + link.split('/')[-1], 'wb') as f:
    f.write(img.read())
  return save_folder + '/' + link.split('/')[-1]
def extract_jpg_urls(text):
    pattern = r'https://[^"]+?\.jpg'
    return re.findall(pattern, text)


def main():
    categories = [
        "政治", "經濟", "科技", "娛樂", "體育",
        "國際", "社會", "健康", "教育", "旅遊",
        "財經", "房地產", "環保", "文化", "軍事",
        "交通", "司法", "災難", "氣象", "美食"
    ]
    
    selected = random.choice(categories)
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
        my_data.append(temp_text)

    index = random.randint(0, len(my_data) - 1)

    providers = [
        "Websim"]
    selected_provider = random.choice(providers)
    client = Client(provider = selected_provider)
    md_format = """
title:  "AI 測試新聞"
categories: [ 'Jekyll', 'AI' ]
tags: ['red', 'yellow']
description: "這是一篇測試的 AI 智能化新聞"
"""
    response = client.chat.completions.create(
        model="gemini-1.5-pro",
        # messages=[{"role": "user", "content": f'請給我一則 AI 的科普文章，請隨機從 ML/DL/CV/NLP/LLM/Stable diffusion等各式AI領域，隨機選擇一個技術點，幫我撰寫一篇技術文章。請直接給我文章:'}],
        messages=[{"role": "user", "content": f'請依據此文章: {my_data[index]}，幫我重新撰寫一篇新聞文章，文章長度約600字，並將原始新聞出處移除，不要顯示任何出處或是作者資訊，請用Markdown排版-不用特別提供```markdown的註記。請直接給我文章:'}],

        # Add any other necessary parameters
    )

    article = response.choices[0].message.content
    time.sleep(5)

    selected_provider = random.choice(providers)
    client = Client(provider = selected_provider)
    response2 = client.chat.completions.create(
        model="gemini-1.5-pro",
        messages=[{"role": "user", "content": f'依據我的文章內容: {article}, 請參考我這邊的資料格式：{md_format}，直接回傳依據文章調整的後面的值(不套用任何格式, 不要出現yaml)直接回傳資料格式字串: '}],
        # Add any other necessary parameters
    )
    title = response2.choices[0].message.content.split('"')[1]
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',}
    img_soup = image_search(title, headers)
    img_path = save_img('img', extract_jpg_urls(str(img_soup))[1])

    article_format = f"""---
layout: post
author: AI
image: {img_path}
{response2.choices[0].message.content}
---
"""
    
    content = article_format + article
    time.sleep(5)

    selected_provider = random.choice(providers)
    client = Client(provider = selected_provider)
    response3 = client.chat.completions.create(
        model="gemini-1.5-pro",
        messages=[{"role": "user", "content": f'依據我的文章內容: {article}, 請簡單給我英文的字串檔名，例如:machine_leanring_introduction，不用回覆我任何說明訊息，請直接給我檔名:'}],
        # Add any other necessary parameters
    )
    file_name_text = response3.choices[0].message.content.replace('/n','').replace(' ','').replace('\n','')


    # 先定義要寫入的資料夾名稱
    folder_name = "_posts"
    # 確保資料夾存在，若不存在就自動建立
    os.makedirs(folder_name, exist_ok=True)

    # 以當前時間做為檔名一部分，以避免重名
    now_str = datetime.datetime.now().strftime("%Y-%m-%d")
    filename = f"{now_str}-{file_name_text}.md"

    # 組出完整路徑：myfolder/auto-file-YYYYMMDD-HHMMSS.md
    file_path = os.path.join(folder_name, filename)

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"File saved to: {file_path}")

if __name__ == "__main__":
    main()
