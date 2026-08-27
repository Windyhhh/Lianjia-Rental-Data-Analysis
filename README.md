<div align="center">

# 🏠 Lianjia-Rental-Data-Analysis

### Complete rental data analysis across 5 Chinese cities.

Scrapy + Selenium collection with multi-dimensional analysis and reusable visualization.

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Scrapy](https://img.shields.io/badge/Scrapy-2-60A839?logo=scrapy&logoColor=white)](https://scrapy.org/)
[![Selenium](https://img.shields.io/badge/Selenium-4-43B02A?logo=selenium&logoColor=white)](https://www.selenium.dev/)

</div>

---

**Lianjia-Rental-Data-Analysis** analyzes rental data collected from Lianjia across **5 Chinese cities** — a Scrapy + Selenium pipeline followed by multi-dimensional analysis and reusable visualization.

> [!NOTE]
> 中文项目：链家租房数据分析——Scrapy + Selenium 采集 5 个中国城市，多维分析，可复用可视化。

---

## Quickstart

```bash
git clone https://github.com/Windyhhh/Lianjia-Rental-Data-Analysis.git
cd Lianjia-Rental-Data-Analysis

pip install -r requirements.txt

# Run the analysis over the raw JSON data
python src/analysis/data_analysis.py
```

Raw data (per-city rental JSON) ships in `data/raw/`.

---

## Features

- **5-city collection** — Beijing, Shanghai, Guangzhou, Shenzhen, Nanjing.
- **Scrapy + Selenium** — spider-based collection pipeline.
- **Multi-dimensional analysis** — reusable analysis + visualization.

---

## Project Structure

```
Lianjia-Rental-Data-Analysis/
├── src/analysis/data_analysis.py
├── data/raw/                  # per-city rental JSON + house data
├── docs/reports/              # task reports
└── requirements.txt
```

---

## License

MIT — free to use, modify and distribute.
