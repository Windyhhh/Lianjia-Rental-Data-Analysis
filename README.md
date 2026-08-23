# 🏠 Lianjia Rental Data Analysis | 链家租房数据分析项目

> **Complete rental housing data analysis project: Scrapy + Selenium web crawlers for 5 Chinese cities (Beijing, Shanghai, Guangzhou, Shenzhen, Nanjing), multi-dimensional data analysis, and reusable visualization templates. Covers price distribution, area analysis, location heatmaps, and market comparison.**
>
> 完整租房数据分析项目：Scrapy + Selenium 爬虫覆盖 5 大城市（北京、上海、广州、深圳、南京），多维度数据分析，可复用可视化模板。涵盖价格分布、面积分析、位置热力图和市场对比。

---

## 🌟 Why This Project? | 项目亮点

Rental housing market analysis requires **scalable data collection, multi-dimensional analysis, and intuitive visualization**. This project provides a **complete end-to-end pipeline**: from **Scrapy + Selenium web crawlers** that collect new house, second-hand house, and rental data from Lianjia (China's leading real estate platform), to **multi-dimensional data analysis** (price, area, location, layout), and **reusable visualization templates** (matplotlib + seaborn). The dataset covers **5 major Chinese cities** with ~10MB of structured rental data.

租房市场分析需要**可扩展的数据采集、多维度分析和直观的可视化**。本项目提供**完整的端到端流水线**：从 **Scrapy + Selenium 网络爬虫** 采集链家（中国领先房产平台）的新房、二手房和租房数据，到**多维度数据分析**（价格、面积、位置、户型），再到**可复用可视化模板**（matplotlib + seaborn）。数据集覆盖 **5 个中国主要城市**，包含约 10MB 结构化租房数据。

| Feature | Details |
|---------|---------|
| **Crawlers** | Scrapy (new/second-hand houses) + Selenium (rental data) |
| **Cities** | Beijing, Shanghai, Guangzhou, Shenzhen, Nanjing (5 cities) |
| **Data Size** | ~10MB structured JSON rental data |
| **Analysis** | Price distribution, area analysis, location heatmap, layout stats |
| **Visualization** | Matplotlib + Seaborn, reusable chart templates |
| **Framework** | Python, Scrapy, Selenium, Pandas, Matplotlib, Seaborn |
| **Documentation** | Complete spider docs, analysis reports, task reports |
| **Reusable** | Modular design, easy to extend to new cities / data sources |

---

## 🏗️ Architecture | 架构设计

```
┌─────────────────────────────────────────────────────────────┐
│                   Lianjia Website (Source)                     │
│         https://lianjia.com  (new / second-hand / rental)     │
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│                   Web Crawler Layer                             │
│  ┌─────────────────────────┐  ┌─────────────────────────┐   │
│  │  Scrapy Spider          │  │  Selenium Spider         │   │
│  │  src/spider/            │  │  src/analysis/          │   │
│  │                         │  │                         │   │
│  │  • new_house.py         │  │  • rental_spider.py     │   │
│  │  • second_house.py      │  │  • selenium_spider.py   │   │
│  │  • items.py             │  │  • (dynamic page crawl) │   │
│  │  • pipelines.py         │  │                         │   │
│  │  • middlewares.py       │  │                         │   │
│  │  • settings.py          │  │                         │   │
│  └─────────────────────────┘  └─────────────────────────┘   │
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│                   Data Storage Layer                            │
│  ┌─────────────────────────────────────────────────────────┐  │
│  │  data/raw/                                               │  │
│  │  • rental_data_北京.json   (2.1MB)                      │  │
│  │  • rental_data_上海.json   (2.1MB)                      │  │
│  │  • rental_data_广州.json   (2.1MB)                      │  │
│  │  • rental_data_深圳.json   (2.1MB)                      │  │
│  │  • rental_data_南京.json   (2.1MB)                      │  │
│  │  • new_houses.json                                      │  │
│  │  • second_houses.json                                   │  │
│  └─────────────────────────────────────────────────────────┘  │
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│                   Data Analysis Layer                           │
│  ┌─────────────────────────────────────────────────────────┐  │
│  │  src/analysis/data_analysis.py (16KB)                   │  │
│  │                                                          │  │
│  │  • Data loading & cleaning                               │  │
│  │  • Price distribution analysis (per city)               │  │
│  │  • Area distribution analysis                            │  │
│  │  • Layout (room count) statistics                       │  │
│  │  • Location / district heatmap                           │  │
│  │  • Cross-city comparison                                 │  │
│  │  • Statistical summary (mean, median, percentile)       │  │
│  └─────────────────────────────────────────────────────────┘  │
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│                   Visualization Layer                           │
│  ┌─────────────────────────────────────────────────────────┐  │
│  │  src/analysis/visualization.py (17KB)                   │  │
│  │                                                          │  │
│  │  • Price distribution histogram + KDE                    │  │
│  │  • Area vs price scatter plot                            │  │
│  │  • City comparison bar chart                             │  │
│  │  • District heatmap                                      │  │
│  │  • Layout pie chart                                      │  │
│  │  • Time series trend (if available)                      │  │
│  │  • Reusable chart templates                              │  │
│  └─────────────────────────────────────────────────────────┘  │
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│                   Reports & Documentation                       │
│  ┌─────────────────────────────────────────────────────────┐  │
│  │  docs/reports/                                           │  │
│  │  • REPORT.md (complete analysis report)                  │  │
│  │  • Task 1: Spider completion report                      │  │
│  │  • Task 2: 5-city rental analysis report                 │  │
│  │  • Spider usage documentation                             │  │
│  └─────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

---

## 📁 Project Structure | 项目结构

```
Lianjia-Rental-Data-Analysis/
├── README.md
├── requirements.txt
├── .gitignore
├── 爆款博客.md                              # Technical blog (63KB)
├── data/
│   └── raw/
│       ├── rental_data_北京.json             # Beijing rental data (2.1MB)
│       ├── rental_data_上海.json             # Shanghai rental data (2.1MB)
│       ├── rental_data_广州.json             # Guangzhou rental data (2.1MB)
│       ├── rental_data_深圳.json             # Shenzhen rental data (2.1MB)
│       ├── rental_data_南京.json             # Nanjing rental data (2.1MB)
│       ├── new_houses.json                   # New house listings
│       └── second_houses.json                # Second-hand house listings
├── docs/
│   ├── spider_readme.md                      # Spider documentation
│   └── reports/
│       ├── README.md
│       ├── REPORT.md                         # Complete analysis report (18KB)
│       ├── 【任务1完成报告】链家新房二手房爬虫.md
│       ├── 【任务1详细报告】链家新房二手房爬虫完整版.md
│       ├── 【任务2完成报告】5城市租房数据分析大作业.md
│       ├── 【任务2详细报告】5城市租房数据分析完整版.md
│       ├── 完成情况总结.md
│       └── 爬虫使用说明.md
├── src/
│   ├── analysis/
│   │   ├── main.py                           # Analysis entry point
│   │   ├── data_analysis.py                  # Core analysis logic (16KB)
│   │   ├── visualization.py                  # Visualization templates (17KB)
│   │   ├── rental_spider.py                  # Rental data scraper
│   │   ├── selenium_spider.py                # Selenium dynamic scraper
│   │   └── requirements.txt
│   └── spider/
│       └── lianjia_spider/                   # Scrapy project
│           ├── scrapy.cfg
│           ├── settings.py
│           ├── items.py
│           ├── pipelines.py
│           ├── middlewares.py
│           ├── run_spider.py
│           ├── README.md
│           └── spiders/
│               ├── new_house.py              # New house spider
│               └── second_house.py           # Second-hand house spider
└── tests/
```

---

## 🚀 Quick Start | 快速开始

### 1. Installation | 安装

```bash
pip install -r requirements.txt
# Includes: scrapy, selenium, pandas, numpy, matplotlib, seaborn
```

### 2. Run Data Analysis | 运行数据分析

```bash
cd src/analysis
python main.py
```

This will:
- Load rental data for all 5 cities
- Clean and preprocess data
- Generate multi-dimensional analysis
- Save visualization charts

### 3. Run Scrapy Spider | 运行 Scrapy 爬虫

```bash
cd src/spider/lianjia_spider

# Crawl new houses
scrapy crawl new_house -o new_houses.json

# Crawl second-hand houses
scrapy crawl second_house -o second_houses.json

# Or use the runner script
python run_spider.py
```

### 4. Run Selenium Rental Spider | 运行 Selenium 租房爬虫

```bash
cd src/analysis
python rental_spider.py --city 北京
python selenium_spider.py --city 上海
```

### 5. Generate Visualizations | 生成可视化

```python
from visualization import RentalVisualizer

viz = RentalVisualizer(data_dir="data/raw")
viz.plot_price_distribution(city="北京")
viz.plot_area_vs_price(city="上海")
viz.plot_city_comparison()
viz.plot_district_heatmap(city="深圳")
```

---

## 📊 Data Fields | 数据字段

Each rental listing contains:

| Field | Type | Description |
|-------|------|-------------|
| `title` | string | Listing title |
| `price` | float | Monthly rent (CNY) |
| `area` | float | Floor area (m²) |
| `layout` | string | Room layout (e.g., "2室1厅") |
| `floor` | string | Floor information |
| `orientation` | string | House orientation |
| `district` | string | District / area name |
| `address` | string | Detailed address |
| `city` | string | City name |
| `url` | string | Original listing URL |
| `publish_time` | string | Listing publish time |

---

## 📈 Analysis Dimensions | 分析维度

### 1. Price Analysis | 价格分析

- Price distribution per city (histogram + KDE)
- Average / median / percentile rent
- Price per square meter (rent/m²)
- Price range segmentation (low / mid / high)

### 2. Area Analysis | 面积分析

- Area distribution (studio / 1BR / 2BR / 3BR+)
- Area vs price correlation (scatter plot)
- Average area per layout type

### 3. Location Analysis | 位置分析

- District-level price heatmap
- Most expensive / cheapest districts
- Price gradient from city center to suburbs

### 4. Layout Analysis | 户型分析

- Layout distribution (pie chart)
- Average price per layout
- Area range per layout type

### 5. Cross-City Comparison | 跨城市对比

- Average rent comparison (bar chart)
- Price distribution overlap
- Affordability index (rent / average income)
- Market size comparison (number of listings)

---

## 🔧 Crawler Details | 爬虫详情

### Scrapy Spider (New / Second-hand Houses) | Scrapy 爬虫

- **Framework**: Scrapy 2.x
- **Spiders**: `new_house`, `second_house`
- **Pipelines**: JSON export, data validation
- **Middlewares**: User agent rotation, retry logic
- **Settings**: Concurrent requests, download delay, robots.txt compliance

### Selenium Spider (Rental Data) | Selenium 爬虫

- **Framework**: Selenium WebDriver
- **Purpose**: Dynamic page crawling (JavaScript-rendered content)
- **Features**: Page scrolling, wait for elements, anti-detection
- **Cities**: Configurable city parameter

---

## 📚 References | 参考文献

1. **Lianjia.** (2024). *Lianjia.com - Real estate platform.* https://lianjia.com
2. **Scrapy.** (2024). *Scrapy documentation.* https://docs.scrapy.org
3. **Selenium.** (2024). *Selenium WebDriver documentation.* https://www.selenium.dev
4. **McKinney, W.** (2017). *Python for Data Analysis.* O'Reilly Media.
5. **VanderPlas, J.** (2016). *Python Data Science Handbook.* O'Reilly Media.
6. **Waskom, M.** (2021). *Seaborn: statistical data visualization.* Journal of Open Source Software.

---

## ⚠️ Disclaimer | 免责声明

This project is for **educational and research purposes only**. Data is collected from publicly available information on Lianjia.com. Please respect the website's robots.txt and terms of service. Do not use this crawler for commercial purposes without permission.

本项目**仅供教育和研究目的**。数据采集自链家网公开信息。请遵守网站的 robots.txt 和服务条款。未经许可，请勿将此爬虫用于商业目的。

---

## 📄 License | 许可证

MIT License — free to use, modify, and distribute for research purposes.

---

<div align="center">

**Built with 🏠 for rental market data research**

[Report Bug](https://github.com/Windyhhh/Lianjia-Rental-Data-Analysis/issues) · [Request Feature](https://github.com/Windyhhh/Lianjia-Rental-Data-Analysis/issues)

</div>
