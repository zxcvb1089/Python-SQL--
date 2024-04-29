import pymysql
import csv
import pandas as pd
import matplotlib.pyplot as plt
# 引入 Python 內建網址解析套件
from urllib.parse import urlsplit, parse_qs

connection = pymysql.connect(host='localhost',
                             user='root',
                             password='',
                             port=3306,
                             db='demo_shop_logs',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
try:
    with connection.cursor() as cursor:
        sql = 'SELECT * FROM user_purchase_logs'
        cursor.execute(sql)
        items = cursor.fetchall()
finally:
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

df_utm_source = pd.Series(utm_stats['utm_source'])
df_utm_medium = pd.Series(utm_stats['utm_medium'])
df_utm_campaign = pd.Series(utm_stats['utm_campaign'])
"""
# 使用 matplotlib 建立餅圖
plt.figure(figsize=(15, 5))

# 建立第一個子圖表，顯示 utm_source 資料
plt.subplot(1, 3, 1)
plt.title('UTM Source')
df_utm_source.plot(kind='pie', autopct='%1.1f%%')

# 建立第二個子圖表，顯示 utm_medium 資料
plt.subplot(1, 3, 2)
plt.title('UTM Medium')
df_utm_medium.plot(kind='pie', autopct='%1.1f%%')

# 建立第三個子圖表，顯示 utm_campaign 資料
plt.subplot(1, 3, 3)
plt.title('UTM Campaign')
df_utm_campaign.plot(kind='pie', autopct='%1.1f%%')

plt.show()
"""
"""
# 使用 matplotlib 建立一個餅圖，包含所有的 UTM 統計資料
plt.figure(figsize=(15, 5))

# 建立第一個子圖表，顯示 utm_source 資料
plt.subplot(1, 1, 1)
plt.title('UTM Stats')
df_utm_source.plot(kind='pie', autopct='%1.1f%%', labels=None)

# 添加圖例，顯示 utm_source 資料的標籤
plt.legend(labels=df_utm_source.index, loc='upper left')

plt.show()
"""
# 建立三個子圖表，共享 y 軸，建立 figure 和 axes，設置子圖表的尺寸，sharey=True 是在使用 函數時的一個參數設置。 它用於指定創建的子圖共用y軸刻度。
fig, axes = plt.subplots(1, 3, figsize=(20, 10), sharey=True)

# 第一個子圖表，顯示 utm_source 資料，autopct='%1.1f%%'，表示顯示百分比。ax=axes[0]，表示將這個餅圖放在第一個子圖表上。
df_utm_source.plot(kind='pie', autopct='%1.1f%%', ax=axes[0])
axes[0].set_title('UTM Source')

# 第二個子圖表，顯示 utm_medium 資料
df_utm_medium.plot(kind='pie', autopct='%1.1f%%', ax=axes[1])
axes[1].set_title('UTM Medium')

# 第三個子圖表，顯示 utm_campaign 資料
df_utm_campaign.plot(kind='pie', autopct='%1.1f%%', ax=axes[2])
axes[2].set_title('UTM Campaign')

plt.savefig("數位行銷流量分析.png")

plt.show()