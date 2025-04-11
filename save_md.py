import os
import datetime
from g4f.client import Client
import time
"""
---
layout: post
author: AI
image: assets/images/11.jpg
"""
def main():
    client = Client()
    md_format = """
title:  "AI 測試新聞"
categories: [ 'Jekyll', 'AI' ]
tags: ['red', 'yellow']
description: "這是一篇測試的 AI 智能化新聞"
"""
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": f'請給我一則 AI 的科普文章，請隨機從 ML/DL/CV/NLP/LLM/Stable diffusion等各式AI領域，隨機選擇一個技術點，幫我撰寫一篇技術文章。請直接給我文章:'}],
        # Add any other necessary parameters
    )

    article = response.choices[0].message.content
    time.sleep(5)
    response2 = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": f'依據我的文章內容: {article}, 請參考我這邊的資料：{md_format}，直接回傳依據文章調整的後面的值(不套用任何格式)直接回傳字串: '}],
        # Add any other necessary parameters
    )
    article_format = f"""
---
layout: post
author: AI
image: assets/images/11.jpg
{response2.choices[0].message.content}
---
"""
    
    content = article_format + article
    time.sleep(5)
    response3 = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": f'依據我的文章內容: {article}, 請簡單給我英文的字串檔名，例如:machine_leanring_introduction，請直接給我檔名:'}],
        # Add any other necessary parameters
    )
    file_name_text = response3.choices[0].message.content


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
