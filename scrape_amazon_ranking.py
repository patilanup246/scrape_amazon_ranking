# -*- coding: utf-8 -*-

import urllib2
from bs4 import BeautifulSoup
import re
from datetime import datetime
import sqlite3

#URL = "https://www.amazon.co.jp/dp/B0759RX47Q" # アニメガタリズ
URL = "https://www.amazon.co.jp/Dies-irae-Blu-ray-BOX-vol-1/dp/B075YZ9J3G/" # ディエスイレ
USERAGENT = 'Mozilla/5.0'

req = urllib2.Request(URL)
req.add_header("User-agent", USERAGENT)
soup = BeautifulSoup(urllib2.urlopen(req), "html.parser")

# get:タイトル
product_title = soup.find("span", id="productTitle").string.strip()

# get:DVD
sales_rank = soup.find("li", id="SalesRank")
dvd_rank = re.search(r'DVD - (.+)位', str(sales_rank)).group(1)
dvd_rank = dvd_rank.replace(",", "")

# get:DVD > ブルーレイ > アニメ, DVD > アニメ
zg_hrsr_rank = soup.find_all("span", class_="zg_hrsr_rank")
dvd_bd_anime_rank = re.search(r'>(.+)位', str(zg_hrsr_rank[0])).group(1)
dvd_bd_anime_rank = dvd_bd_anime_rank.replace(",", "")

dvd_anime_rank = re.search(r'>(.+)位', str(zg_hrsr_rank[1])).group(1)
dvd_anime_rank = dvd_anime_rank.replace(",", "")

# sqliteで保存
db = 'soup.db'
table = 'ranking'

conn = sqlite3.connect(db)
conn.row_factory = sqlite3.Row # カラム名でアクセスできるようにする
c = conn.cursor()

# テーブル存在チェック
cur = c.execute("SELECT * FROM sqlite_master WHERE type='table' and name='%s'" % table)
if cur.fetchone() == None: # 存在してない時は作る
	c.execute('''
		create table %s (
			id INTEGER PRIMARY KEY AUTOINCREMENT,
			product_title VARCHAR(255),
			dvd_rank INTEGER,
			dvd_bd_anime_rank INTEGER,
			dvd_anime_rank INTEGER,
			scrape_date TIMESTAMP,
			created_at TIMESTAMP DEFAULT (DATETIME('now','localtime'))
		)
	'''
	% table)
	conn.commit()

# データ挿入
sql = '''
	insert into ranking
		(product_title, dvd_rank, dvd_bd_anime_rank, dvd_anime_rank, scrape_date)
	values
		(?,?,?,?,?)
'''
ranking = (
	product_title,
	int(dvd_rank),
	int(dvd_bd_anime_rank),
	int(dvd_anime_rank),
	datetime.now().strftime("%Y-%m-%d %H:%M:%S")
)
c.execute(sql, ranking)
conn.commit()

# 挿入されたデータの確認
select_sql = '''
	select
		id,
		product_title,
		dvd_rank,
		dvd_bd_anime_rank,
		dvd_anime_rank,
		scrape_date
	from
		ranking
	order by
		id desc
	limit
		1
'''
for row in c.execute(select_sql):
	print(row['product_title'].encode('utf-8') + ' (' + row['scrape_date'].encode('utf-8') + ')')
	print(' - DVD ' + str(row['dvd_rank']) + '位')
	print(' - DVD > ブルーレイ > アニメ ' + str(row['dvd_bd_anime_rank']) + '位')
	print(' - DVD > アニメ' + str(row['dvd_anime_rank']) + '位')

conn.close()