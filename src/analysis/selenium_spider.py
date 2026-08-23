# -*- coding: utf-8 -*-
"""
使用Selenium爬取链家租房数据
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import json
import time
import random
import re

def init_driver():
    """初始化Chrome驱动"""
    chrome_options = Options()
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
    chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
    chrome_options.add_experimental_option('useAutomationExtension', False)

    driver = webdriver.Chrome(options=chrome_options)

    # 隐藏webdriver特征
    driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
        'source': 'Object.defineProperty(navigator, "webdriver", {get: () => undefined})'
    })

    return driver

def parse_house_data(html_content, city_name):
    """解析房源数据"""
    soup = BeautifulSoup(html_content, 'lxml')
    houses = soup.find_all('div', class_='content__list--item')

    data = []
    for house in houses:
        try:
            item = {}

            # 标题
            title_elem = house.find('p', class_='content__list--item--title')
            if title_elem:
                title_link = title_elem.find('a')
                if title_link:
                    item['community_name'] = title_link.get_text(strip=True)

            # 描述
            des_elem = house.find('p', class_='content__list--item--des')
            if des_elem:
                des_text = des_elem.get_text(strip=True)
                item['location'] = des_text

                # 提取面积
                area_match = re.search(r'(\d+\.?\d*)\s*㎡', des_text)
                if area_match:
                    item['area'] = float(area_match.group(1))

                # 提取户型
                room_match = re.search(r'(\d+室\d+厅\d*卫?)', des_text)
                if room_match:
                    item['room_type'] = room_match.group(1)

                # 提取朝向
                aspect_match = re.search(r'([东南西北]{1,2})', des_text)
                if aspect_match:
                    item['aspect'] = aspect_match.group(1)

            # 价格
            price_elem = house.find('span', class_='content__list--item-price')
            if price_elem:
                em_elem = price_elem.find('em')
                if em_elem:
                    price_text = em_elem.get_text(strip=True)
                    price_match = re.search(r'(\d+\.?\d*)', price_text)
                    if price_match:
                        item['total_rent'] = float(price_match.group(1))

                        # 计算单位面积租金
                        if 'area' in item and item['area'] > 0:
                            item['unit_rent'] = round(item['total_rent'] / item['area'], 2)

            # 品牌
            brand_elem = house.find('p', class_='content__list--item--brand')
            if brand_elem:
                brand_span = brand_elem.find('span', class_='brand')
                if brand_span:
                    item['agency'] = brand_span.get_text(strip=True)

            item['city'] = city_name
            data.append(item)

        except Exception as e:
            print(f"  解析房源失败: {e}")

    return data

def crawl_with_selenium():
    """使用Selenium爬取数据"""
    print("="*70, flush=True)
    print("  使用Selenium爬取链家租房数据", flush=True)
    print("="*70, flush=True)

    driver = None
    all_data = {}

    # 5个城市
    cities = {
        '北京': 'bj',
        '上海': 'sh',
        '广州': 'gz',
        '深圳': 'sz',
        '南京': 'nj'
    }

    try:
        print("\n正在初始化Chrome驱动...", flush=True)
        driver = init_driver()
        print("✅ Chrome驱动初始化成功", flush=True)

        # 首次访问，检查是否需要登录
        print("\n正在打开链家网站...")
        driver.get('https://bj.lianjia.com/zufang/')
        time.sleep(5)

        # 检查是否需要登录
        current_url = driver.current_url
        print(f"当前URL: {current_url}")

        if 'passport' in current_url or 'login' in current_url.lower():
            print("\n" + "="*70)
            print("  ⚠️  需要登录链家账号")
            print("="*70)
            print("\n请在打开的Chrome浏览器中完成以下操作：")
            print("1. 输入手机号和密码")
            print("2. 完成验证码（如果有）")
            print("3. 点击登录")
            print("4. 等待页面跳转到租房列表")
            print("\n程序将等待 60 秒（1分钟）供您登录...")
            print("登录成功后程序会自动继续爬取数据")
            print("="*70)

            # 等待用户登录
            wait_time = 0
            max_wait = 60  # 1分钟

            while wait_time < max_wait:
                time.sleep(5)
                wait_time += 5

                # 检查是否已登录（URL不再包含passport或login）
                current_url = driver.current_url
                if 'passport' not in current_url and 'login' not in current_url.lower():
                    print(f"\n✅ 检测到登录成功！当前URL: {current_url}")
                    time.sleep(2)  # 等待页面完全加载
                    break

                # 每10秒提示一次
                if wait_time % 10 == 0:
                    remaining = max_wait - wait_time
                    print(f"  等待登录中... 已等待 {wait_time} 秒，剩余 {remaining} 秒")

            if wait_time >= max_wait:
                print("\n❌ 登录超时（1分钟），程序退出")
                print("请重新运行程序并在1分钟内完成登录")
                return
        else:
            print("✅ 无需登录或已登录，直接开始爬取")

        # 开始爬取各城市数据
        for city_name, city_code in cities.items():
            print(f"\n{'='*70}")
            print(f"  开始爬取 {city_name} 的租房数据")
            print(f"{'='*70}")

            all_data[city_name] = []

            # 每个城市爬取足够的页数以获得≥8000条数据
            # 假设每页30条，需要约270页。为了保证数据量，爬取300页
            target_count = 8000
            max_pages = 300

            for page in range(1, max_pages + 1):
                # 检查是否已达到目标数据量
                if len(all_data[city_name]) >= target_count:
                    print(f"\n✅ 已达到目标数据量 {target_count} 条，停止爬取")
                    break

                url = f'https://{city_code}.lianjia.com/zufang/pg{page}/'
                print(f"\n正在爬取第 {page} 页: {url} (已爬取 {len(all_data[city_name])} 条)")

                retry_count = 0
                max_retries = 2
                page_data = []

                while retry_count < max_retries:
                    try:
                        driver.get(url)
                        time.sleep(random.uniform(3, 5))

                        # 获取页面源码
                        html_content = driver.page_source

                        # 解析数据
                        page_data = parse_house_data(html_content, city_name)

                        if len(page_data) > 0:
                            print(f"  ✅ 找到 {len(page_data)} 个房源")
                            break
                        else:
                            retry_count += 1
                            if retry_count < max_retries:
                                print(f"  ⚠️ 未找到房源，30秒后重试 (第 {retry_count}/{max_retries} 次)")
                                time.sleep(30)  # 等待30秒后重试
                            else:
                                print(f"  ⚠️ 重试 {max_retries} 次后仍未找到房源，可能已到最后一页，停止爬取此城市")
                                break

                    except Exception as e:
                        print(f"  ❌ 爬取出错: {e}")
                        retry_count += 1
                        if retry_count < max_retries:
                            print(f"  ⚠️ 30秒后重试 (第 {retry_count}/{max_retries} 次)")
                            time.sleep(30)
                        else:
                            print(f"  ❌ 重试 {max_retries} 次后仍失败，停止爬取此城市")
                            break

                all_data[city_name].extend(page_data)

                # 延迟
                delay = random.uniform(2, 4)
                print(f"  ⏳ 等待 {delay:.1f} 秒...")
                time.sleep(delay)

            print(f"\n{'='*70}")
            print(f"✅ {city_name} 共爬取 {len(all_data[city_name])} 个房源")
            print(f"{'='*70}")

            # 城市间延迟
            if city_name != '南京':
                delay = random.uniform(5, 10)
                print(f"\n⏳ 切换城市前等待 {delay:.1f} 秒...")
                time.sleep(delay)
        
        # 统计总数
        total_count = sum(len(all_data[city]) for city in all_data)

        print(f"\n\n{'='*70}")
        print(f"✅ 爬取完成！总共爬取 {total_count} 个房源")
        print(f"{'='*70}")

        if total_count > 0:
            # 保存每个城市的数据
            print(f"\n正在保存数据...")
            import os
            if not os.path.exists('data'):
                os.makedirs('data')

            for city_name in all_data:
                if all_data[city_name]:
                    filename = f'data/rental_data_{city_name}.json'
                    with open(filename, 'w', encoding='utf-8') as f:
                        json.dump(all_data[city_name], f, ensure_ascii=False, indent=2)
                    print(f"  ✅ {filename} ({len(all_data[city_name])} 条)")

            # 显示详细统计
            print(f"\n{'='*70}")
            print(f"数据统计详情:")
            print(f"{'='*70}")

            for city_name in all_data:
                city_data = all_data[city_name]
                if city_data:
                    has_area = len([d for d in city_data if 'area' in d and d['area']])
                    has_price = len([d for d in city_data if 'total_rent' in d and d['total_rent']])
                    has_room = len([d for d in city_data if 'room_type' in d and d['room_type']])
                    has_aspect = len([d for d in city_data if 'aspect' in d and d['aspect']])

                    print(f"\n{city_name}:")
                    print(f"  - 总房源数: {len(city_data)} 条")
                    print(f"  - 有面积信息: {has_area} 条 ({has_area/len(city_data)*100:.1f}%)")
                    print(f"  - 有价格信息: {has_price} 条 ({has_price/len(city_data)*100:.1f}%)")
                    print(f"  - 有户型信息: {has_room} 条 ({has_room/len(city_data)*100:.1f}%)")
                    print(f"  - 有朝向信息: {has_aspect} 条 ({has_aspect/len(city_data)*100:.1f}%)")

            # 显示示例
            print(f"\n示例数据（北京第1个房源）:")
            if all_data.get('北京') and len(all_data['北京']) > 0:
                item = all_data['北京'][0]
                print(f"  小区: {item.get('community_name', 'N/A')}")
                print(f"  面积: {item.get('area', 'N/A')} ㎡")
                print(f"  户型: {item.get('room_type', 'N/A')}")
                print(f"  租金: {item.get('total_rent', 'N/A')} 元/月")
                print(f"  单价: {item.get('unit_rent', 'N/A')} 元/㎡/月")
        else:
            print("\n❌ 未能爬取到任何数据")
        
    except Exception as e:
        print(f"\n❌ 错误: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        if driver:
            driver.quit()
            print("\n✅ 浏览器已关闭")

if __name__ == '__main__':
    crawl_with_selenium()

