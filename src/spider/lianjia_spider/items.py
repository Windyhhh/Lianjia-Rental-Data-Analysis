# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class NewHouseItem(scrapy.Item):
    """新房数据项"""
    name = scrapy.Field()  # 楼盘名称
    house_type = scrapy.Field()  # 类型
    location = scrapy.Field()  # 地点
    room_type = scrapy.Field()  # 房型
    area = scrapy.Field()  # 面积
    unit_price = scrapy.Field()  # 单价
    total_price = scrapy.Field()  # 总价


class SecondHouseItem(scrapy.Item):
    """二手房数据项"""
    community_name = scrapy.Field()  # 小区名称
    location = scrapy.Field()  # 地点
    room_type = scrapy.Field()  # 房型
    unit_price = scrapy.Field()  # 单价
    total_price = scrapy.Field()  # 总价
