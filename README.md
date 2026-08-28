<div align="center">

# 🏠 Lianjia-Rental-Data-Analysis

### Lianjia rental-market scraping, analysis & visualization.

Crawl rentals across 5 cities, run multi-dimensional analysis, and produce professional charts.

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Scrapy](https://img.shields.io/badge/Scrapy-2-60A839?logo=scrapy&logoColor=white)](https://scrapy.org/)
[![Pandas](https://img.shields.io/badge/Pandas-1.5-150458?logo=pandas&logoColor=white)](https://pandas.pydata.org/)

</div>

---

**Lianjia-Rental-Data-Analysis** scrapes **Lianjia rental data across 5 cities** (Beijing, Shanghai, Guangzhou, Shenzhen, Nanjing), runs multi-dimensional market analysis, and renders professional visualizations — a complete data-science pipeline from crawl to insight.

> [!NOTE]
> 中文项目：链家租房数据分析——5 城市爬虫（北上广深+南京）+ 多维度分析 + 专业可视化；2830 套房源，有效率 94%。

---

## Features

- **Crawler** — complete anti-scraping strategy; 2,830 listings, 94% effective rate.
- **Multi-dimensional analysis** — 7 deep-analysis tasks across cities / regions / prices.
- **Visualization** — 6 professional charts.
- **Modular** — maintainable, reusable pipeline.

---

## Quickstart

```bash
git clone https://github.com/Windyhhh/Lianjia-Rental-Data-Analysis.git
cd Lianjia-Rental-Data-Analysis

pip install -r requirements.txt

scrapy crawl lianjia            # scrape rental data
python src/analyze.py           # run analysis
python src/visualize.py         # generate charts
```

---

## Project Structure

```
Lianjia-Rental-Data-Analysis/
├── src/spider/                 # scrapy spider
├── src/                        # analysis + visualization
├── data/                       # scraped listings
├── reports/                    # analysis reports
└── docs/                       # spider readme, blog
```

---

## License

MIT — free to use, modify and distribute.
