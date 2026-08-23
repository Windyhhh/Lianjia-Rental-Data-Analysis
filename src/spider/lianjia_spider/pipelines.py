# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import json
import os
from datetime import datetime
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
from lianjia_spider.items import NewHouseItem, SecondHouseItem


class NewHouseJsonPipeline:
    """新房数据JSON导出管道"""
    
    def open_spider(self, spider):
        """爬虫启动时调用"""
        if spider.name == 'new_house':
            self.file = open('new_houses.json', 'w', encoding='utf-8')
            self.file.write('[\n')
            self.first_item = True
    
    def close_spider(self, spider):
        """爬虫关闭时调用"""
        if spider.name == 'new_house':
            self.file.write('\n]')
            self.file.close()
            spider.logger.info('新房数据已保存到 new_houses.json')
    
    def process_item(self, item, spider):
        """处理每个item"""
        if isinstance(item, NewHouseItem):
            if not self.first_item:
                self.file.write(',\n')
            self.first_item = False
            
            line = json.dumps(dict(item), ensure_ascii=False, indent=2)
            self.file.write(line)
        
        return item


class SecondHouseJsonPipeline:
    """二手房数据JSON导出管道"""
    
    def open_spider(self, spider):
        """爬虫启动时调用"""
        if spider.name == 'second_house':
            self.file = open('second_houses.json', 'w', encoding='utf-8')
            self.file.write('[\n')
            self.first_item = True
    
    def close_spider(self, spider):
        """爬虫关闭时调用"""
        if spider.name == 'second_house':
            self.file.write('\n]')
            self.file.close()
            spider.logger.info('二手房数据已保存到 second_houses.json')
    
    def process_item(self, item, spider):
        """处理每个item"""
        if isinstance(item, SecondHouseItem):
            if not self.first_item:
                self.file.write(',\n')
            self.first_item = False
            
            line = json.dumps(dict(item), ensure_ascii=False, indent=2)
            self.file.write(line)
        
        return item


class LianjiaSpiderPipeline:
    """数据清洗和去重管道"""
    
    def open_spider(self, spider):
        """爬虫启动时初始化去重集合"""
        self.seen = set()
    
    def process_item(self, item, spider):
        """数据处理和去重"""
        adapter = ItemAdapter(item)
        
        # 生成唯一标识符用于去重
        if isinstance(item, NewHouseItem):
            item_id = adapter.get('name', '')
        elif isinstance(item, SecondHouseItem):
            item_id = adapter.get('community_name', '')
        else:
            item_id = str(adapter)
        
        if item_id in self.seen:
            raise DropItem(f"重复项目已过滤: {item_id}")
        
        self.seen.add(item_id)
        
        # 数据清洗 - 删除空值
        for key in list(adapter.keys()):
            if not adapter[key]:
                adapter[key] = '未知'
        
        return item
