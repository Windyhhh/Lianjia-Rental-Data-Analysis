# 链家新房与二手房爬虫项目

## 项目概述
本项目使用Scrapy框架爬取链家官网的新房和二手房数据，包括两个独立爬虫，整合在同一个Scrapy项目中。爬取北京地区新房和二手房第3-7页数据。

## 项目结构
```
lianjia_spider/
├── lianjia_spider/
│   ├── __init__.py
│   ├── items.py              # 数据模型定义
│   ├── pipelines.py          # 数据处理管道
│   ├── settings.py           # 项目配置
│   ├── middlewares.py        # 中间件
│   └── spiders/
│       ├── new_house.py      # 新房爬虫
│       └── second_house.py   # 二手房爬虫
├── scrapy.cfg                # Scrapy配置文件
├── run_spider.py             # 运行脚本
└── README.md                 # 本文件
```

## 爬虫功能

### 新房爬虫 (new_house.py)
- **爬取范围**: 第3-7页（共5页）
- **爬取字段**: 
  - 楼盘名称 (name)
  - 房产类型 (house_type)
  - 地点 (location)
  - 房型 (room_type)
  - 面积 (area)
  - 单价 (unit_price)
  - 总价 (total_price)
- **数据输出**: new_houses.json

### 二手房爬虫 (second_house.py)
- **爬取范围**: 第3-7页（共5页）
- **爬取字段**:
  - 小区名称 (community_name)
  - 地点 (location)
  - 房型 (room_type)
  - 单价 (unit_price)
  - 总价 (total_price)
- **数据输出**: second_houses.json

## 反爬虫措施

### 1. User-Agent伪装
```python
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36..."
```

### 2. 请求延迟
- `DOWNLOAD_DELAY = 2`: 每个请求之间延迟2秒
- `CONCURRENT_REQUESTS_PER_DOMAIN = 2`: 每个域最多2个并发请求

### 3. Cookies支持
- `COOKIES_ENABLED = True`: 启用Cookie支持，保持会话

### 4. robots.txt规则
- `ROBOTSTXT_OBEY = False`: 跳过robots.txt检查（适度爬虫）

### 5. 数据去重
- 在Pipeline中实现去重机制，过滤重复数据

## 使用方法

### 安装依赖
```bash
pip install scrapy
```

### 运行爬虫

#### 方法1: 使用运行脚本
```bash
cd lianjia_spider
python run_spider.py
```

#### 方法2: 使用scrapy命令行
```bash
cd lianjia_spider

# 运行新房爬虫
scrapy crawl new_house -o new_houses.json

# 运行二手房爬虫
scrapy crawl second_house -o second_houses.json
```

## 数据流程

1. **数据提取**: Spiders通过XPath从HTML页面提取数据
2. **数据处理**: Pipeline进行数据清洗、去重、验证
3. **数据存储**: JSON格式导出到文件

## 关键技术点

### Scrapy框架应用
- ✅ 项目配置管理 (settings.py)
- ✅ 数据模型定义 (items.py)
- ✅ Spider实现 (spiders/)
- ✅ Pipeline处理 (pipelines.py)
- ✅ 数据导出

### 单项目双爬虫集成
- 两个爬虫共享同一个Scrapy项目
- 通过spider.name标识不同爬虫
- 各爬虫独立的Pipeline处理
- 统一的配置管理

## 数据格式示例

### 新房数据 (new_houses.json)
```json
[
  {
    "name": "楼盘名称",
    "house_type": "商品房",
    "location": "朝阳区 CBD",
    "room_type": "2居",
    "area": "88㎡",
    "unit_price": "120000元/㎡",
    "total_price": "1000万"
  }
]
```

### 二手房数据 (second_houses.json)
```json
[
  {
    "community_name": "小区名称",
    "location": "朝阳区 建国路",
    "room_type": "2居 1厅 1卫",
    "unit_price": "95000元/㎡",
    "total_price": "800万"
  }
]
```

## 爬虫配置说明

| 配置项 | 值 | 说明 |
|--------|-----|------|
| USER_AGENT | Chrome浏览器标识 | 模拟真实浏览器访问 |
| ROBOTSTXT_OBEY | False | 不遵守robots.txt |
| DOWNLOAD_DELAY | 2 | 请求延迟（秒） |
| CONCURRENT_REQUESTS_PER_DOMAIN | 2 | 单域并发数 |
| COOKIES_ENABLED | True | 启用Cookie |
| FEED_EXPORT_ENCODING | utf-8 | 输出编码 |

## 注意事项

1. **合法性**: 爬虫仅用于学习和研究，请遵守网站的服务条款
2. **频率控制**: 设置了适当的延迟，避免过度请求
3. **数据隐私**: 爬取的数据仅用于学习分析
4. **错误处理**: 异常数据会被标记为"未知"

## 故障排除

### 问题1: 爬虫无法连接到网站
- 检查网络连接
- 检查User-Agent是否被阻止
- 增加DOWNLOAD_DELAY值

### 问题2: 解析失败
- XPath选择器可能已过期
- 需要检查网站HTML结构是否变化
- 更新对应的XPath表达式

### 问题3: 数据为空
- 检查网页是否使用JavaScript动态渲染
- 考虑使用Selenium配合爬虫

## 扩展功能

1. **多城市支持**: 修改start_requests中的base_url即可支持其他城市
2. **分页扩展**: 修改range(3, 8)支持更多页数
3. **反爬增强**: 加入代理池、随机延迟等
4. **JavaScript处理**: 集成Splash或Selenium处理动态内容

## 许可证
教学用途

## 作者
Scrapy爬虫开发示例

---
**最后更新**: 2025年12月18日
