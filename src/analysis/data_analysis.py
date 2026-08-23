# -*- coding: utf-8 -*-
"""
链家租房数据分析模块
包含7项必做分析任务
"""

import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter, defaultdict
import warnings

warnings.filterwarnings('ignore')

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

class RentalDataAnalysis:
    """租房数据分析类"""
    
    def __init__(self, data_files):
        """
        初始化分析器
        
        Args:
            data_files: dict, 格式为 {'城市名': '数据文件路径'}
        """
        self.data_files = data_files
        self.all_data = {}
        self.df_all = None
        self.load_data()
    
    def load_data(self):
        """加载所有城市的数据"""
        print("正在加载数据...")
        
        for city, filepath in self.data_files.items():
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                self.all_data[city] = data
                print(f"✓ 已加载 {city}: {len(data)} 条数据")
            except Exception as e:
                print(f"✗ 加载 {city} 失败: {e}")
        
        # 合并所有数据为DataFrame
        all_records = []
        for city, records in self.all_data.items():
            all_records.extend(records)
        
        self.df_all = pd.DataFrame(all_records)
        print(f"\n总数据量: {len(self.df_all)} 条")
    
    # ==================== 7项必做分析任务 ====================
    
    def analysis_1_agency_distribution(self):
        """
        分析1：中介品牌分析
        5城市内及整体的品牌分布、市场占有率
        """
        print("\n" + "="*60)
        print("分析1：中介品牌分析")
        print("="*60)
        
        # 整体市场占有率
        print("\n【整体中介品牌市场占有率】")
        agency_counts = self.df_all['agency'].value_counts()
        total = len(self.df_all)
        
        agency_stats = []
        for agency, count in agency_counts.head(10).items():
            percentage = (count / total) * 100
            market_share = {
                '品牌': agency,
                '房源数': count,
                '市场占有率(%)': round(percentage, 2)
            }
            agency_stats.append(market_share)
            print(f"{agency:20s} {count:5d} 套 ({percentage:6.2f}%)")
        
        # 各城市市场占有率
        print("\n【各城市主要中介品牌】")
        city_agency_stats = {}
        for city in self.df_all['city'].unique():
            city_data = self.df_all[self.df_all['city'] == city]
            city_agencies = city_data['agency'].value_counts().head(5)
            city_total = len(city_data)
            
            print(f"\n{city}:")
            city_stats = []
            for agency, count in city_agencies.items():
                percentage = (count / city_total) * 100
                print(f"  {agency:20s} {count:4d} 套 ({percentage:6.2f}%)")
                city_stats.append({
                    '品牌': agency,
                    '房源数': count,
                    '占比(%)': round(percentage, 2)
                })
            city_agency_stats[city] = city_stats
        
        return {
            'overall': agency_stats,
            'by_city': city_agency_stats
        }
    
    def analysis_2_overall_rent(self):
        """
        分析2：总体房租分析
        租金及单位面积租金的均价/最高价/最低价/中位数
        """
        print("\n" + "="*60)
        print("分析2：总体房租分析")
        print("="*60)
        
        # 清理数据，移除异常值
        df_clean = self.df_all[self.df_all['total_rent'] > 0].copy()
        df_clean = df_clean[df_clean['rent_per_sqm'] > 0].copy()
        
        print("\n【总体房租统计】")
        print(f"平均租金: ¥{df_clean['total_rent'].mean():.2f}")
        print(f"最高租金: ¥{df_clean['total_rent'].max():.2f}")
        print(f"最低租金: ¥{df_clean['total_rent'].min():.2f}")
        print(f"中位数:   ¥{df_clean['total_rent'].median():.2f}")
        
        print("\n【单位面积租金统计 (元/㎡)】")
        print(f"平均: ¥{df_clean['rent_per_sqm'].mean():.2f}/㎡")
        print(f"最高: ¥{df_clean['rent_per_sqm'].max():.2f}/㎡")
        print(f"最低: ¥{df_clean['rent_per_sqm'].min():.2f}/㎡")
        print(f"中位数: ¥{df_clean['rent_per_sqm'].median():.2f}/㎡")
        
        # 各城市对比
        print("\n【各城市房租对比】")
        city_stats = []
        for city in sorted(df_clean['city'].unique()):
            city_data = df_clean[df_clean['city'] == city]
            stats = {
                '城市': city,
                '平均租金': round(city_data['total_rent'].mean(), 2),
                '最高租金': round(city_data['total_rent'].max(), 2),
                '最低租金': round(city_data['total_rent'].min(), 2),
                '中位数': round(city_data['total_rent'].median(), 2),
                '单位面积均价': round(city_data['rent_per_sqm'].mean(), 2)
            }
            city_stats.append(stats)
            print(f"{city}: 平均 ¥{stats['平均租金']:.0f} | "
                  f"单位面积 ¥{stats['单位面积均价']:.0f}/㎡")
        
        return city_stats
    
    def analysis_3_room_type(self):
        """
        分析3：户型分析
        一居/二居/三居的租金及单位面积租金的均价/最高价/最低价/中位数
        """
        print("\n" + "="*60)
        print("分析3：户型分析")
        print("="*60)
        
        df_clean = self.df_all[self.df_all['total_rent'] > 0].copy()
        
        # 提取户型信息（一居、二居、三居）
        room_categories = {
            '一居': [],
            '二居': [],
            '三居': [],
            '其他': []
        }
        
        for idx, room_type in df_clean['room_type'].items():
            if '一' in room_type or '1' in room_type:
                room_categories['一居'].append(idx)
            elif '二' in room_type or '2' in room_type:
                room_categories['二居'].append(idx)
            elif '三' in room_type or '3' in room_type or '三以上' in room_type:
                room_categories['三居'].append(idx)
            else:
                room_categories['其他'].append(idx)
        
        print("\n【主要户型房租分析】")
        room_stats = []
        for room_type in ['一居', '二居', '三居']:
            indices = room_categories[room_type]
            if len(indices) == 0:
                continue
            
            room_data = df_clean.loc[indices]
            stats = {
                '户型': room_type,
                '房源数': len(room_data),
                '平均租金': round(room_data['total_rent'].mean(), 2),
                '最高租金': round(room_data['total_rent'].max(), 2),
                '最低租金': round(room_data['total_rent'].min(), 2),
                '中位数': round(room_data['total_rent'].median(), 2),
                '单位面积均价': round(room_data['rent_per_sqm'].mean(), 2) if len(room_data) > 0 else 0
            }
            room_stats.append(stats)
            
            print(f"{room_type} ({len(room_data):4d}套): "
                  f"平均 ¥{stats['平均租金']:.0f} | "
                  f"单位面积 ¥{stats['单位面积均价']:.0f}/㎡")
        
        return room_stats
    
    def analysis_4_district_analysis(self):
        """
        分析4：板块分析
        各城市不同板块的房租均价
        """
        print("\n" + "="*60)
        print("分析4：板块分析")
        print("="*60)
        
        df_clean = self.df_all[self.df_all['total_rent'] > 0].copy()
        
        district_stats = []
        for city in sorted(df_clean['city'].unique()):
            city_data = df_clean[df_clean['city'] == city]
            
            # 按地点分组
            location_stats = city_data.groupby('location').agg({
                'total_rent': ['count', 'mean', 'max', 'min'],
                'rent_per_sqm': 'mean'
            }).round(2)
            
            location_stats.columns = ['房源数', '平均租金', '最高租金', '最低租金', '单位面积均价']
            location_stats = location_stats.sort_values('平均租金', ascending=False).head(10)
            
            print(f"\n【{city} 板块排名 Top 10】")
            for location, row in location_stats.iterrows():
                print(f"  {location:20s} {row['房源数']:3.0f}套 "
                      f"均价¥{row['平均租金']:6.0f} "
                      f"({row['单位面积均价']:6.0f}元/㎡)")
                
                district_stats.append({
                    '城市': city,
                    '板块': location,
                    '房源数': int(row['房源数']),
                    '平均租金': round(row['平均租金'], 2),
                    '单位面积均价': round(row['单位面积均价'], 2)
                })
        
        return district_stats
    
    def analysis_5_aspect_analysis(self):
        """
        分析5：朝向分析
        不同朝向的单位面积租金分布
        """
        print("\n" + "="*60)
        print("分析5：朝向分析")
        print("="*60)
        
        df_clean = self.df_all[self.df_all['rent_per_sqm'] > 0].copy()
        
        # 统计各朝向
        aspect_stats = df_clean.groupby('aspect').agg({
            'rent_per_sqm': ['count', 'mean', 'max', 'min'],
            'total_rent': 'mean'
        }).round(2)
        
        aspect_stats.columns = ['房源数', '单位面积均价', '单位面积最高', '单位面积最低', '平均租金']
        aspect_stats = aspect_stats[aspect_stats['房源数'] >= 10]  # 过滤数据过少的朝向
        aspect_stats = aspect_stats.sort_values('单位面积均价', ascending=False)
        
        print("\n【各朝向单位面积租金】")
        for aspect, row in aspect_stats.iterrows():
            print(f"{aspect:20s} {row['房源数']:4.0f}套 "
                  f"均价¥{row['单位面积均价']:6.0f}/㎡ "
                  f"(最高¥{row['单位面积最高']:6.0f})")
        
        # 各城市朝向对比
        print("\n【各城市最优/最差朝向】")
        for city in sorted(df_clean['city'].unique()):
            city_data = df_clean[df_clean['city'] == city]
            aspect_avg = city_data.groupby('aspect')['rent_per_sqm'].agg(['mean', 'count'])
            aspect_avg = aspect_avg[aspect_avg['count'] >= 5]
            
            if len(aspect_avg) > 0:
                best = aspect_avg['mean'].idxmax()
                worst = aspect_avg['mean'].idxmin()
                print(f"{city}: 最高 {best} ({aspect_avg.loc[best, 'mean']:.0f}元/㎡) | "
                      f"最低 {worst} ({aspect_avg.loc[worst, 'mean']:.0f}元/㎡)")
        
        return aspect_stats.to_dict('index')
    
    def analysis_6_salary_rent_correlation(self, salary_data):
        """
        分析6：工资-租金关联分析
        各城市平均工资与单位面积租金的关系
        
        Args:
            salary_data: dict, 格式为 {'城市': 月平均工资}
        """
        print("\n" + "="*60)
        print("分析6：工资-租金关联分析")
        print("="*60)
        
        df_clean = self.df_all[self.df_all['rent_per_sqm'] > 0].copy()
        
        correlation_data = []
        print("\n【各城市租房负担分析】")
        print("(年房租 / 年平均工资 = 租房负担比例)")
        
        for city in sorted(df_clean['city'].unique()):
            city_data = df_clean[df_clean['city'] == city]
            avg_rent_sqm = city_data['rent_per_sqm'].mean()
            avg_total_rent = city_data['total_rent'].mean()
            
            # 年房租 = 月均租金 * 12
            annual_rent = avg_total_rent * 12
            
            # 获取该城市的平均工资
            avg_salary = salary_data.get(city, 0)
            
            if avg_salary > 0:
                # 租房负担比 = 年房租 / 年平均工资
                burden_ratio = (annual_rent / (avg_salary * 12)) * 100
                
                correlation_data.append({
                    '城市': city,
                    '月均工资': avg_salary,
                    '月均房租': round(avg_total_rent, 2),
                    '年房租': round(annual_rent, 2),
                    '租房负担比(%)': round(burden_ratio, 2),
                    '单位面积租金': round(avg_rent_sqm, 2)
                })
                
                print(f"{city:6s} 月工资¥{avg_salary:6.0f} | "
                      f"月租金¥{avg_total_rent:6.0f} | "
                      f"负担比{burden_ratio:6.2f}%")
        
        # 找出负担最重的城市
        if correlation_data:
            heaviest_burden = max(correlation_data, key=lambda x: x['租房负担比(%)'])
            print(f"\n【租房负担最重的城市】: {heaviest_burden['城市']} "
                  f"({heaviest_burden['租房负担比(%)']:.2f}%)")
        
        return correlation_data
    
    def analysis_7_supplementary_data(self, salary_data):
        """
        分析7：补充数据
        额外获取各城市平均工资数据
        """
        print("\n" + "="*60)
        print("分析7：补充数据 - 城市经济指标")
        print("="*60)
        
        print("\n【各城市平均工资数据】(数据来源：国家统计局、招聘平台)")
        for city in sorted(salary_data.keys()):
            salary = salary_data[city]
            print(f"{city}: ¥{salary:,.0f}/月")
        
        return salary_data
    
    def run_all_analysis(self, salary_data):
        """运行所有分析"""
        results = {}
        
        # 执行7项分析
        results['analysis_1'] = self.analysis_1_agency_distribution()
        results['analysis_2'] = self.analysis_2_overall_rent()
        results['analysis_3'] = self.analysis_3_room_type()
        results['analysis_4'] = self.analysis_4_district_analysis()
        results['analysis_5'] = self.analysis_5_aspect_analysis()
        results['analysis_6'] = self.analysis_6_salary_rent_correlation(salary_data)
        results['analysis_7'] = self.analysis_7_supplementary_data(salary_data)
        
        return results


def main():
    """主函数"""
    
    # 数据文件路径
    data_files = {
        '北京': 'rental_data_bj.json',
        '上海': 'rental_data_sh.json',
        '广州': 'rental_data_gz.json',
        '深圳': 'rental_data_sz.json',
        '南京': 'rental_data_nj.json'
    }
    
    # 各城市平均工资数据（2024年）
    salary_data = {
        '北京': 12840,
        '上海': 12430,
        '广州': 10360,
        '深圳': 11340,
        '南京': 9280
    }
    
    # 创建分析器并运行分析
    analyzer = RentalDataAnalysis(data_files)
    results = analyzer.run_all_analysis(salary_data)
    
    # 保存分析结果
    with open('analysis_results.json', 'w', encoding='utf-8') as f:
        # 转换结果为可序列化的格式
        serializable_results = {}
        for key, value in results.items():
            if isinstance(value, (list, dict)):
                serializable_results[key] = value
            else:
                serializable_results[key] = str(value)
        
        json.dump(serializable_results, f, ensure_ascii=False, indent=2)
    
    print("\n" + "="*60)
    print("分析完成！结果已保存到 analysis_results.json")
    print("="*60)


if __name__ == '__main__':
    main()
