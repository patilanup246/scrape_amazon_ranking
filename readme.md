Amazon商品ページよりランキング情報の取得とDB保存
====

## Description

URLに商品情報のリンクを設定
DVD、ブルーレイ、アニメのランキングを取得
取得したランキング情報はsqliteで保存する

※Amazonのスクレイピング対策強化により動作未確認

## Requirement
- urllib2
- beautifulsoup4
- sqlite3

## Usage

```python
python scrape_amazon_ranking.py
```
