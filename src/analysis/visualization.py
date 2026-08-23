# -*- coding: utf-8 -*-
"""
数据可视化模块
为7项分析任务生成图表
"""

import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from data_analysis import RentalDataAnalysis
import warnings

warnings.filterwarnings('ignore')

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['figure.figsize'] = (14, 10)

class RentalDataVisualization:
    """数据可视化类"""
    
    def __init__(self, analyzer):
        """
        初始化可视化器
        
        Args:
            analyzer: RentalDataAnalysis 实例
        """
        self.analyzer = analyzer
        self.df_all = analyzer.df_all
    
    def plot_agency_distribution(self, save_path='chart_1_agency.png'):
        """
        可视化1：中介品牌分析
        """
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle('中介品牌分析', fontsize=16, fontweight='bold')
        
        # 整体品牌分布
        ax1 = axes[0, 0]
        agency_counts = self.df_all['agency'].value_counts().head(10)
        agency_counts.plot(kind='barh', ax=ax1, color='steelblue')
        ax1.set_xlabel('房源数', fontsize=11)
        ax1.set_title('整体中介品牌分布 Top 10', fontsize=12)
        
        # 各城市品牌数量对比
        ax2 = axes[0, 1]
        city_agency_count = self.df_all.groupby('city')['agency'].nunique()
        city_agency_count.plot(kind='bar', ax=ax2, color='coral')
        ax2.set_ylabel('品牌数', fontsize=11)
        ax2.set_title('各城市中介品牌数量', fontsize=12)
        ax2.tick_params(axis='x', rotation=45)
        
        # 城市间主要品牌对比
        ax3 = axes[1, 0]
        top_agencies = self.df_all['agency'].value_counts().head(5).index
        city_agency_data = pd.crosstab(self.df_all['city'], self.df_all['agency'])[top_agencies]
        city_agency_data.plot(kind='bar', ax=ax3)
        ax3.set_ylabel('房源数', fontsize=11)
        ax3.set_title('主要品牌在各城市的房源分布', fontsize=12)
        ax3.tick_params(axis='x', rotation=45)
        ax3.legend(title='品牌', bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=9)
        
        # 市场占有率饼图
        ax4 = axes[1, 1]
        top_5_agencies = self.df_all['agency'].value_counts().head(5)
        other_count = len(self.df_all) - top_5_agencies.sum()
        data_for_pie = list(top_5_agencies.values) + [other_count]
        labels = list(top_5_agencies.index) + ['其他']
        ax4.pie(data_for_pie, labels=labels, autopct='%1.1f%%', startangle=90)
        ax4.set_title('整体市场占有率分布', fontsize=12)
        
        plt.tight_layout()
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"✓ 已保存图表: {save_path}")
        plt.close()
    
    def plot_overall_rent(self, save_path='chart_2_rent.png'):
        """
        可视化2：总体房租分析
        """
        df_clean = self.df_all[self.df_all['total_rent'] > 0].copy()
        
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle('总体房租分析', fontsize=16, fontweight='bold')
        
        # 各城市平均租金对比
        ax1 = axes[0, 0]
        city_rent = df_clean.groupby('city')['total_rent'].mean().sort_values(ascending=False)
        city_rent.plot(kind='bar', ax=ax1, color='teal')
        ax1.set_ylabel('平均租金(元)', fontsize=11)
        ax1.set_title('各城市平均月租金', fontsize=12)
        ax1.tick_params(axis='x', rotation=45)
        for i, v in enumerate(city_rent):
            ax1.text(i, v + 100, f'¥{v:.0f}', ha='center', fontsize=9)
        
        # 租金分布箱线图
        ax2 = axes[0, 1]
        city_order = sorted(df_clean['city'].unique())
        df_clean.boxplot(column='total_rent', by='city', ax=ax2)
        ax2.set_ylabel('租金(元)', fontsize=11)
        ax2.set_title('租金分布箱线图', fontsize=12)
        ax2.set_xlabel('城市', fontsize=11)
        plt.sca(ax2)
        plt.xticks(rotation=45)
        
        # 单位面积租金对比
        ax3 = axes[1, 0]
        city_rent_sqm = df_clean.groupby('city')['rent_per_sqm'].mean().sort_values(ascending=False)
        city_rent_sqm.plot(kind='bar', ax=ax3, color='mediumpurple')
        ax3.set_ylabel('单位面积租金(元/㎡)', fontsize=11)
        ax3.set_title('各城市单位面积平均租金', fontsize=12)
        ax3.tick_params(axis='x', rotation=45)
        for i, v in enumerate(city_rent_sqm):
            ax3.text(i, v + 1, f'{v:.0f}', ha='center', fontsize=9)
        
        # 租金直方图
        ax4 = axes[1, 1]
        for city in city_order:
            city_data = df_clean[df_clean['city'] == city]['total_rent']
            ax4.hist(city_data, bins=30, alpha=0.5, label=city)
        ax4.set_xlabel('租金(元)', fontsize=11)
        ax4.set_ylabel('频数', fontsize=11)
        ax4.set_title('各城市租金分布直方图', fontsize=12)
        ax4.legend()
        
        plt.tight_layout()
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"✓ 已保存图表: {save_path}")
        plt.close()
    
    def plot_room_type(self, save_path='chart_3_room.png'):
        """
        可视化3：户型分析
        """
        df_clean = self.df_all[self.df_all['total_rent'] > 0].copy()
        
        # 分类户型
        room_categories = {'一居': [], '二居': [], '三居': []}
        for idx, room_type in df_clean['room_type'].items():
            if '一' in room_type or '1' in room_type:
                room_categories['一居'].append(idx)
            elif '二' in room_type or '2' in room_type:
                room_categories['二居'].append(idx)
            elif '三' in room_type or '3' in room_type:
                room_categories['三居'].append(idx)
        
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle('户型分析', fontsize=16, fontweight='bold')
        
        # 户型房源数对比
        ax1 = axes[0, 0]
        room_counts = {k: len(v) for k, v in room_categories.items() if v}
        pd.Series(room_counts).plot(kind='bar', ax=ax1, color='lightcoral')
        ax1.set_ylabel('房源数', fontsize=11)
        ax1.set_title('各户型房源数量', fontsize=12)
        ax1.tick_params(axis='x', rotation=0)
        
        # 户型平均租金
        ax2 = axes[0, 1]
        room_rents = {}
        for room_type, indices in room_categories.items():
            if indices:
                room_rents[room_type] = df_clean.loc[indices, 'total_rent'].mean()
        pd.Series(room_rents).plot(kind='bar', ax=ax2, color='skyblue')
        ax2.set_ylabel('平均租金(元)', fontsize=11)
        ax2.set_title('各户型平均租金', fontsize=12)
        ax2.tick_params(axis='x', rotation=0)
        
        # 户型单位面积租金
        ax3 = axes[1, 0]
        room_rent_sqm = {}
        for room_type, indices in room_categories.items():
            if indices:
                room_rent_sqm[room_type] = df_clean.loc[indices, 'rent_per_sqm'].mean()
        pd.Series(room_rent_sqm).plot(kind='bar', ax=ax3, color='lightgreen')
        ax3.set_ylabel('单位面积租金(元/㎡)', fontsize=11)
        ax3.set_title('各户型单位面积平均租金', fontsize=12)
        ax3.tick_params(axis='x', rotation=0)
        
        # 各城市户型租金分布
        ax4 = axes[1, 1]
        room_city_data = []
        for room_type, indices in room_categories.items():
            if indices:
                room_data = df_clean.loc[indices].groupby('city')['total_rent'].mean()
                room_city_data.append(room_data)
        room_city_df = pd.DataFrame(room_city_data).T
        room_city_df.plot(kind='bar', ax=ax4)
        ax4.set_ylabel('平均租金(元)', fontsize=11)
        ax4.set_title('各城市不同户型平均租金', fontsize=12)
        ax4.tick_params(axis='x', rotation=45)
        ax4.legend(title='户型')
        
        plt.tight_layout()
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"✓ 已保存图表: {save_path}")
        plt.close()
    
    def plot_district_analysis(self, save_path='chart_4_district.png'):
        """
        可视化4：板块分析
        """
        df_clean = self.df_all[self.df_all['total_rent'] > 0].copy()
        
        fig = plt.figure(figsize=(16, 12))
        fig.suptitle('板块分析', fontsize=16, fontweight='bold')
        
        cities = sorted(df_clean['city'].unique())
        
        # 为每个城市创建子图
        for idx, city in enumerate(cities, 1):
            ax = plt.subplot(2, 3, idx)
            
            city_data = df_clean[df_clean['city'] == city]
            location_avg = city_data.groupby('location')['total_rent'].agg(['mean', 'count'])
            location_avg = location_avg[location_avg['count'] >= 3]  # 至少3个房源
            location_avg = location_avg.sort_values('mean', ascending=False).head(10)
            
            location_avg['mean'].plot(kind='barh', ax=ax, color='mediumpurple')
            ax.set_xlabel('平均租金(元)', fontsize=10)
            ax.set_title(f'{city} 主要板块 Top 10', fontsize=11)
        
        plt.tight_layout()
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"✓ 已保存图表: {save_path}")
        plt.close()
    
    def plot_aspect_analysis(self, save_path='chart_5_aspect.png'):
        """
        可视化5：朝向分析
        """
        df_clean = self.df_all[self.df_all['rent_per_sqm'] > 0].copy()
        
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle('朝向分析', fontsize=16, fontweight='bold')
        
        # 各朝向单位面积租金
        ax1 = axes[0, 0]
        aspect_sqm = df_clean.groupby('aspect')['rent_per_sqm'].agg(['mean', 'count'])
        aspect_sqm = aspect_sqm[aspect_sqm['count'] >= 10]
        aspect_sqm = aspect_sqm.sort_values('mean', ascending=False)
        aspect_sqm['mean'].plot(kind='bar', ax=ax1, color='orange')
        ax1.set_ylabel('单位面积租金(元/㎡)', fontsize=11)
        ax1.set_title('各朝向单位面积平均租金', fontsize=12)
        ax1.tick_params(axis='x', rotation=45)
        
        # 朝向房源数分布
        ax2 = axes[0, 1]
        aspect_count = df_clean['aspect'].value_counts().head(10)
        aspect_count.plot(kind='pie', ax=ax2, autopct='%1.1f%%')
        ax2.set_ylabel('')
        ax2.set_title('各朝向房源分布比例', fontsize=12)
        
        # 各城市最优朝向
        ax3 = axes[1, 0]
        best_aspects = []
        for city in sorted(df_clean['city'].unique()):
            city_data = df_clean[df_clean['city'] == city]
            best = city_data.groupby('aspect')['rent_per_sqm'].mean().idxmax()
            best_aspects.append({'city': city, 'aspect': best})
        
        # 创建表格展示
        ax3.axis('off')
        table_data = [[item['city'], item['aspect']] for item in best_aspects]
        table = ax3.table(cellText=table_data, colLabels=['城市', '最高朝向'],
                         cellLoc='center', loc='center', colWidths=[0.4, 0.4])
        table.auto_set_font_size(False)
        table.set_fontsize(10)
        table.scale(1, 2)
        ax3.set_title('各城市最优朝向', fontsize=12, pad=20)
        
        # 城市间朝向对比
        ax4 = axes[1, 1]
        top_aspects = aspect_sqm.head(5).index
        city_aspect_data = []
        for city in sorted(df_clean['city'].unique()):
            city_data = df_clean[df_clean['city'] == city]
            city_aspect_avg = city_data[city_data['aspect'].isin(top_aspects)].groupby('aspect')['rent_per_sqm'].mean()
            city_aspect_data.append(city_aspect_avg)
        
        pd.DataFrame(city_aspect_data).plot(kind='bar', ax=ax4)
        ax4.set_ylabel('单位面积租金(元/㎡)', fontsize=11)
        ax4.set_title('主要朝向在各城市的租金对比', fontsize=12)
        ax4.tick_params(axis='x', rotation=45)
        ax4.legend(title='朝向', bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=9)
        
        plt.tight_layout()
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"✓ 已保存图表: {save_path}")
        plt.close()
    
    def plot_salary_rent_correlation(self, salary_data, save_path='chart_6_salary.png'):
        """
        可视化6：工资-租金关联分析
        """
        df_clean = self.df_all[self.df_all['rent_per_sqm'] > 0].copy()
        
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle('工资-租金关联分析', fontsize=16, fontweight='bold')
        
        # 计算各城市数据
        city_data_list = []
        for city in sorted(df_clean['city'].unique()):
            city_df = df_clean[df_clean['city'] == city]
            avg_salary = salary_data.get(city, 0)
            avg_rent = city_df['total_rent'].mean()
            annual_rent = avg_rent * 12
            burden = (annual_rent / (avg_salary * 12)) * 100 if avg_salary > 0 else 0
            
            city_data_list.append({
                'city': city,
                'salary': avg_salary,
                'rent': avg_rent,
                'burden': burden
            })
        
        city_data_df = pd.DataFrame(city_data_list)
        
        # 工资对比
        ax1 = axes[0, 0]
        city_data_df.set_index('city')['salary'].plot(kind='bar', ax=ax1, color='green')
        ax1.set_ylabel('月平均工资(元)', fontsize=11)
        ax1.set_title('各城市月平均工资', fontsize=12)
        ax1.tick_params(axis='x', rotation=45)
        
        # 租金对比
        ax2 = axes[0, 1]
        city_data_df.set_index('city')['rent'].plot(kind='bar', ax=ax2, color='red')
        ax2.set_ylabel('月平均租金(元)', fontsize=11)
        ax2.set_title('各城市月平均租金', fontsize=12)
        ax2.tick_params(axis='x', rotation=45)
        
        # 租房负担比
        ax3 = axes[1, 0]
        burden_sorted = city_data_df.set_index('city')['burden'].sort_values(ascending=False)
        burden_sorted.plot(kind='bar', ax=ax3, color='crimson')
        ax3.set_ylabel('租房负担比(%)', fontsize=11)
        ax3.set_title('各城市租房负担比 (年房租/年工资)', fontsize=12)
        ax3.tick_params(axis='x', rotation=45)
        for i, v in enumerate(burden_sorted):
            ax3.text(i, v + 1, f'{v:.1f}%', ha='center', fontsize=9)
        
        # 工资vs租金散点图
        ax4 = axes[1, 1]
        scatter = ax4.scatter(city_data_df['salary'], city_data_df['rent'], 
                             s=300, alpha=0.6, c=city_data_df['burden'], 
                             cmap='YlOrRd')
        
        for idx, row in city_data_df.iterrows():
            ax4.annotate(row['city'], 
                        (row['salary'], row['rent']),
                        fontsize=10, ha='center', va='center')
        
        ax4.set_xlabel('月平均工资(元)', fontsize=11)
        ax4.set_ylabel('月平均租金(元)', fontsize=11)
        ax4.set_title('工资vs租金关系图', fontsize=12)
        cbar = plt.colorbar(scatter, ax=ax4)
        cbar.set_label('租房负担比(%)', fontsize=10)
        
        plt.tight_layout()
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"✓ 已保存图表: {save_path}")
        plt.close()
    
    def plot_all_visualizations(self, salary_data):
        """生成所有可视化图表"""
        print("\n" + "="*60)
        print("正在生成数据可视化图表...")
        print("="*60 + "\n")
        
        self.plot_agency_distribution()
        self.plot_overall_rent()
        self.plot_room_type()
        self.plot_district_analysis()
        self.plot_aspect_analysis()
        self.plot_salary_rent_correlation(salary_data)
        
        print("\n" + "="*60)
        print("所有图表已生成完成！")
        print("="*60)


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
    
    # 各城市平均工资数据
    salary_data = {
        '北京': 12840,
        '上海': 12430,
        '广州': 10360,
        '深圳': 11340,
        '南京': 9280
    }
    
    # 创建分析器和可视化器
    analyzer = RentalDataAnalysis(data_files)
    visualizer = RentalDataVisualization(analyzer)
    
    # 生成所有可视化
    visualizer.plot_all_visualizations(salary_data)


if __name__ == '__main__':
    main()
