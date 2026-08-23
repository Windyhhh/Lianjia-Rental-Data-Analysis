#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
运行爬虫脚本 - 链家新房和二手房爬虫
"""

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

def run_spiders():
    """运行所有爬虫"""
    settings = get_project_settings()
    process = CrawlerProcess(settings)
    
    # 运行新房爬虫
    print("=" * 50)
    print("开始爬取链家新房数据（第3-7页）...")
    print("=" * 50)
    process.crawl('new_house')
    
    # 运行二手房爬虫
    print("\n" + "=" * 50)
    print("开始爬取链家二手房数据（第3-7页）...")
    print("=" * 50)
    process.crawl('second_house')
    
    process.start()
    
    print("\n" + "=" * 50)
    print("爬虫运行完成！")
    print("新房数据已保存到: new_houses.json")
    print("二手房数据已保存到: second_houses.json")
    print("=" * 50)

if __name__ == '__main__':
    run_spiders()
