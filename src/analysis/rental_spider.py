# -*- coding: utf-8 -*-
"""
链家租房数据爬虫 - 爬取5个城市的租房数据
城市：北京、上海、广州、深圳、南京
"""

import requests
import json
import time
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import random
import re

class LianjiaRentalSpider:
    """链家租房数据爬虫"""
    
    # 城市与域名映射
    CITIES = {
        'beijing': {'code': 'bj', 'name': '北京'},
        'shanghai': {'code': 'sh', 'name': '上海'},
        'guangzhou': {'code': 'gz', 'name': '广州'},
        'shenzhen': {'code': 'sz', 'name': '深圳'},
        'nanjing': {'code': 'nj', 'name': '南京'}
    }
    
    def __init__(self):
        """初始化爬虫"""
        self.session = requests.Session()
        # 更完整的headers，参考成功案例
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Cache-Control': 'max-age=0'
        }
        self.all_data = {}
        
    def get_rental_data(self, city_code, pages=50):
        """
        爬取指定城市的租房数据
        
        Args:
            city_code: 城市代码 (bj, sh, gz, sz, nj)
            pages: 爬取页数
            
        Returns:
            list: 租房数据列表
        """
        data = []
        base_url = f'https://{city_code}.lianjia.com/zufang/'
        
        print(f"\n开始爬取 {city_code} 租房数据...")
        
        for page in range(1, pages + 1):
            try:
                url = f'{base_url}pg{page}/'
                print(f"正在爬取第 {page} 页...")
                
                # 发送请求
                response = self.session.get(url, headers=self.headers, timeout=10)
                response.encoding = 'utf-8'
                
                if response.status_code != 200:
                    print(f"页面请求失败: {response.status_code}")
                    continue
                
                # 解析页面 - 使用lxml解析器（更快更稳定）
                soup = BeautifulSoup(response.content, 'lxml')

                # 查找所有房源 - 新版页面使用 content__list--item
                houses = soup.find_all('div', class_='content__list--item')

                print(f"  找到 {len(houses)} 个房源")

                if not houses:
                    print(f"  页面 {page} 未找到房源，可能已到最后一页")
                    break

                # 提取每个房源的信息
                for house in houses:
                    try:
                        item = self._parse_house_item(house, city_code)
                        if item:
                            data.append(item)
                    except Exception as e:
                        print(f"解析房源失败: {e}")
                        continue
                
                # 请求延迟（增加延迟时间，避免被封）
                delay = random.uniform(3, 8)
                print(f"  等待 {delay:.1f} 秒...")
                time.sleep(delay)
                
                print(f"第 {page} 页已爬取 {len(houses)} 个房源")
                
            except Exception as e:
                print(f"爬取第 {page} 页时出错: {e}")
                continue
        
        print(f"完成！共爬取 {city_code} 房源 {len(data)} 个")
        return data
    
    def _parse_house_item(self, house_elem, city_code):
        """
        解析单个房源元素
        
        Args:
            house_elem: BeautifulSoup元素
            city_code: 城市代码
            
        Returns:
            dict: 房源信息
        """
        try:
            item = {}

            # 小区名称 - 新版页面结构
            title_elem = house_elem.find('p', class_='content__list--item--title')
            if title_elem:
                title_link = title_elem.find('a')
                if title_link:
                    item['community_name'] = title_link.get_text(strip=True)
                else:
                    item['community_name'] = title_elem.get_text(strip=True)
            else:
                item['community_name'] = '未知'

            # 地点/区域和房型信息 - 从 content__list--item--des 提取
            des_elem = house_elem.find('p', class_='content__list--item--des')
            if des_elem:
                des_text = des_elem.get_text(strip=True)
                item['location'] = des_text

                # 提取面积
                area_match = re.search(r'(\d+\.?\d*)\s*㎡', des_text)
                if area_match:
                    item['area'] = float(area_match.group(1))
                else:
                    item['area'] = 0

                # 提取房型（如：3室2厅1卫）
                room_match = re.search(r'(\d+室\d+厅\d*卫?)', des_text)
                if room_match:
                    item['room_type'] = room_match.group(1)
                else:
                    item['room_type'] = '未知'

                # 提取朝向
                aspect_match = re.search(r'[东南西北]{1,2}(?:\s*[东南西北]{1,2})*', des_text)
                if aspect_match:
                    item['aspect'] = aspect_match.group(0)
                else:
                    item['aspect'] = '未知'
            else:
                item['location'] = '未知'
                item['area'] = 0
                item['room_type'] = '未知'
                item['aspect'] = '未知'

            # 租金信息 - 从 content__list--item-price 提取
            price_elem = house_elem.find('span', class_='content__list--item-price')
            if price_elem:
                em_elem = price_elem.find('em')
                if em_elem:
                    price_text = em_elem.get_text(strip=True)
                    # 提取数字（可能是范围，取第一个数字）
                    price_match = re.search(r'(\d+\.?\d*)', price_text)
                    if price_match:
                        item['total_rent'] = float(price_match.group(1))
                    else:
                        item['total_rent'] = 0
                else:
                    item['total_rent'] = 0

                # 单位面积租金 = 总租金 / 面积
                if item['area'] > 0:
                    item['rent_per_sqm'] = item['total_rent'] / item['area']
                else:
                    item['rent_per_sqm'] = 0
            else:
                item['total_rent'] = 0
                item['rent_per_sqm'] = 0

            # 中介品牌 - 从 content__list--item--brand 提取
            brand_elem = house_elem.find('p', class_='content__list--item--brand')
            if brand_elem:
                brand_span = brand_elem.find('span', class_='brand')
                if brand_span:
                    item['agency'] = brand_span.get_text(strip=True)
                else:
                    item['agency'] = '其他'
            else:
                item['agency'] = '其他'

            # 城市
            item['city'] = self.CITIES.get(city_code, {}).get('name', '未知')
            item['city_code'] = city_code

            # 发布时间 - 从 content__list--item--time 提取
            time_elem = house_elem.find('span', class_='content__list--item--time')
            if time_elem:
                item['publish_time'] = time_elem.get_text(strip=True)
            else:
                item['publish_time'] = '未知'

            return item
            
        except Exception as e:
            print(f"解析房源失败: {e}")
            return None
    
    def scrape_all_cities(self, pages_per_city=50):
        """
        爬取所有城市的数据
        
        Args:
            pages_per_city: 每个城市爬取的页数
        """
        all_data = {}
        
        for city_en, city_info in self.CITIES.items():
            city_code = city_info['code']
            city_name = city_info['name']
            
            print(f"\n{'='*60}")
            print(f"开始爬取 {city_name} ({city_code}) 数据")
            print(f"{'='*60}")
            
            # 爬取数据
            city_data = self.get_rental_data(city_code, pages_per_city)
            all_data[city_name] = city_data
            
            # 保存到JSON文件
            self._save_to_json(city_data, f'rental_data_{city_code}.json')
            
            print(f"{city_name} 数据已保存")
        
        return all_data
    
    def _save_to_json(self, data, filename):
        """保存数据到JSON文件"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"数据已保存到 {filename}")
        except Exception as e:
            print(f"保存失败: {e}")
    
    def load_from_json(self, filename):
        """从JSON文件加载数据"""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
            print(f"已从 {filename} 加载 {len(data)} 条数据")
            return data
        except Exception as e:
            print(f"加载失败: {e}")
            return []


def main():
    """主函数"""
    spider = LianjiaRentalSpider()
    
    # 爬取所有城市数据（可根据需求调整页数）
    # 每个城市爬取50页，约每页10-15条房源，共500-750条数据
    # 如需8000条数据，需要爬取约500-600页
    all_data = spider.scrape_all_cities(pages_per_city=50)
    
    print(f"\n{'='*60}")
    print("所有数据爬取完成！")
    print(f"{'='*60}")
    
    # 打印数据统计
    for city, data in all_data.items():
        print(f"{city}: {len(data)} 条数据")


if __name__ == '__main__':
    main()
