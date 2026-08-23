# -*- coding: utf-8 -*-
"""
链家租房数据分析项目 - 主入口
完整的爬虫 + 分析 + 可视化流程
"""

import os
import sys
import json
from rental_spider import LianjiaRentalSpider
from data_analysis import RentalDataAnalysis
from visualization import RentalDataVisualization


def print_header(title):
    """打印标题"""
    print("\n" + "="*70)
    print(f"  {title}")
    print("="*70)


def main():
    """主程序"""
    
    print_header("链家租房数据分析项目 - 5城市数据爬取与分析")
    
    # 配置
    CITIES = {
        'bj': '北京',
        'sh': '上海',
        'gz': '广州',
        'sz': '深圳',
        'nj': '南京'
    }
    
    # 各城市平均工资数据（2024年）
    salary_data = {
        '北京': 12840,
        '上海': 12430,
        '广州': 10360,
        '深圳': 11340,
        '南京': 9280
    }
    
    data_files = {
        '北京': 'rental_data_bj.json',
        '上海': 'rental_data_sh.json',
        '广州': 'rental_data_gz.json',
        '深圳': 'rental_data_sz.json',
        '南京': 'rental_data_nj.json'
    }
    
    # ==================== 步骤1：爬虫 ====================
    
    print_header("步骤1：数据爬取")
    
    input_msg = """
    是否执行数据爬虫？
    注意：爬虫耗时较长（每个城市5-10分钟）
    
    选择:
    1. 执行爬虫（推荐首次运行）
    2. 跳过爬虫，使用现有数据
    
    请输入 (1 或 2): """
    
    choice = input(input_msg).strip()
    
    if choice == '1':
        spider = LianjiaRentalSpider()
        print("\n正在爬取数据...")
        all_data = spider.scrape_all_cities(pages_per_city=50)
        
        print("\n数据爬取完成！")
        for city, data in all_data.items():
            print(f"  ✓ {city}: {len(data)} 条数据")
    else:
        print("\n跳过爬虫，使用现有数据...")
        # 检查数据文件是否存在
        missing_files = []
        for city, filepath in data_files.items():
            if not os.path.exists(filepath):
                missing_files.append(filepath)
        
        if missing_files:
            print(f"\n警告：以下文件不存在:")
            for f in missing_files:
                print(f"  ✗ {f}")
            print("\n请先运行爬虫获取数据！")
            return
    
    # ==================== 步骤2：数据分析 ====================
    
    print_header("步骤2：数据分析")
    
    print("正在加载数据...")
    analyzer = RentalDataAnalysis(data_files)
    
    print("\n正在执行7项分析...")
    results = analyzer.run_all_analysis(salary_data)
    
    print("\n数据分析完成！")
    
    # ==================== 步骤3：可视化 ====================
    
    print_header("步骤3：数据可视化")
    
    print("正在生成可视化图表...")
    visualizer = RentalDataVisualization(analyzer)
    visualizer.plot_all_visualizations(salary_data)
    
    # ==================== 总结 ====================
    
    print_header("项目完成！")
    
    print("""
    生成的文件说明：
    
    【数据文件】
    - rental_data_bj.json    : 北京房源数据
    - rental_data_sh.json    : 上海房源数据
    - rental_data_gz.json    : 广州房源数据
    - rental_data_sz.json    : 深圳房源数据
    - rental_data_nj.json    : 南京房源数据
    
    【分析结果】
    - analysis_results.json  : 7项分析结果
    
    【可视化图表】
    - chart_1_agency.png     : 中介品牌分析
    - chart_2_rent.png       : 总体房租分析
    - chart_3_room.png       : 户型分析
    - chart_4_district.png   : 板块分析
    - chart_5_aspect.png     : 朝向分析
    - chart_6_salary.png     : 工资-租金分析
    
    【文档】
    - REPORT.md              : 完整分析报告
    - README.md              : 项目说明文档
    
    所有文件已保存到当前目录！
    """)
    
    print("="*70)
    print("感谢使用链家租房数据分析项目！")
    print("="*70 + "\n")


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n用户中断执行")
        sys.exit(0)
    except Exception as e:
        print(f"\n\n发生错误：{e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
