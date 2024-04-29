import pymysql
import csv
import pandas as pd
import matplotlib.pyplot as plt
# 引入 Python 內建網址解析套件
from urllib.parse import urlsplit, parse_qs

# 建立和資料庫連線，參數為資料庫系統位址(localhost 為本機電腦別名), 帳號(預設為 root，實務上不建議直接使用), 密碼(預設為空), 資料庫名稱
# charset 為使用編碼，cursorclass 則使用 dict 取代 tuple 當作回傳資料格式
connection = pymysql.connect(host='localhost',
                             user='root',
                             password='',
                             # 資料庫預設為 3306 若自己有更改不同 port 請依照需求更改
                             port=3307,
                             db='demo_shop_logs',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
# 使用 try...finally 錯誤處理，可以讓程式即便錯誤最後會關閉資料庫連線避免浪費資源
try:
    # 使用　with...as 可以讓我們程式正確執行下自動關閉資料庫連線
    with connection.cursor() as cursor:
        # 執行 SQL 敘述查詢資料
        sql = 'SELECT * FROM user_purchase_logs'
        cursor.execute(sql)
        # 取出所有結果
        items = cursor.fetchall()
        #print(items)
        file_name = '數位行銷流量分析-1.csv'

        with open(file_name, 'w', newline='', encoding='utf-8') as csv_file:
            #參數 fieldnames 是一個字串列表，包含了 CSV 檔案中每一列的欄位名稱
            #來獲取第一筆資料的欄位名稱作為 CSV 檔案的欄位名稱
            csv_writer = csv.DictWriter(csv_file, fieldnames=items[0].keys())
            csv_writer.writeheader()
            csv_writer.writerows(items)
        with open(file_name, 'r', newline='', encoding='utf-8') as file:
            line_read = file.read()
            print(f"檔案內容:  \n{line_read.strip()}")
            """
            2.
            #這裡就會變成以list的型態呈現
            rows = csv.reader(file)
            # 以迴圈輸出每一列，每一列是一個 list
            for row in rows:
                print(row)
            """
            """
            3.
            #這裡就跟第一行類似 的輸出方式 也可以這樣寫~~
            for line_item in file.readlines():
            # 去除空行符號
              print(line_item.strip())
            """

finally:
    # 即便程式錯誤也會執行到這行關閉資料庫連線
    connection.close()

# 建立 dict 儲存 UTM 統計資料
utm_stats = {
    'utm_source': {},
    'utm_medium': {},
    'utm_campaign': {}
}

# 將 SQL 查詢資料一一取出
for item in items:
    # 取出 referrer 欄位資料
    referrer = item['referrer']
    # 使用 urlsplit 將 referrer 網址分解成網址物件，取出屬性 query
    query_str = urlsplit(referrer).query
    # 將網址後面所接的參數轉為 dict：{}
    query_dict = parse_qs(query_str)

    # 將 query string 一一取出 {'utm_source': ['newsletter-weekly'], 'utm_medium': ['email'], 'utm_campaign': ['spring-summer']}
    for query_key, query_value in query_dict.items():
        # 取第 0 個 index 取出內容值
        utm_value = query_value[0]
        # 若參數值曾經出現過在 dict 的 key 中則累加 1
        if utm_value in utm_stats[query_key]:
            utm_stats[query_key][utm_value] += 1
        # 否則初始化成 1
        else:
            utm_stats[query_key][utm_value] = 1

# utm_stats: {'utm_source': {'newsletter-weekly': 3, 'google-search': 2, 'facebook-demo-fans-page': 1, 'demo-website': 4}, 'utm_medium': {'email': 3, 'CPC': 2, 'facebook': 1, 'banner': 4}, 'utm_campaign': {'spring-summer': 3, 'campaign-1': 2, 'daily-posts': 1, 'campaign-2': 4}}

# 將 utm_source 資料轉為 pandas Series
df_utm_source = pd.Series(utm_stats['utm_source'])

# 將 utm_medium 資料轉為 pandas Series
df_utm_medium = pd.Series(utm_stats['utm_medium'])

# 將 utm_campaign 資料轉為 pandas Series
df_utm_campaign = pd.Series(utm_stats['utm_campaign'])

# 使用 matplotlib 建立圖表
plt.title('UTM Stats')
# 建立單一圖表
df_utm_source.plot(kind='bar')

# 若希望建立多個子圖表 subplots 於同一個畫面中，可以使用 subplots
# nrows 代表列，代表 ncols 行
fig, axes = plt.subplots(nrows=1, ncols=3)
# 建立子圖表 axes[0] 第一個
df_utm_source.plot(ax=axes[0], kind='bar')
# 建立子圖表 axes[0] 第二個
df_utm_medium.plot(ax=axes[1], kind='bar')
# 建立子圖表 axes[0] 第三個
df_utm_campaign.plot(ax=axes[2], kind='bar')
plt.savefig("數位行銷流量-1.png")
plt.show()