# 链家新房爬虫 - 两层爬虫实现
import scrapy
from lianjia_spider.items import NewHouseItem


class NewHouseSpider(scrapy.Spider):
    """链家新房爬虫 - 爬取第3-7页数据（两层爬虫）"""

    name = 'new_house'
    allowed_domains = ['lianjia.com']

    def start_requests(self):
        """生成请求 - 新房第3-7页"""
        base_url = 'https://bj.lianjia.com/loupan/'

        for page in range(3, 8):  # 第3-7页
            url = f'{base_url}pg{page}/'
            yield scrapy.Request(
                url,
                callback=self.parse_list,
                headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
                },
                meta={'page': page}
            )

    def parse_list(self, response):
        """第一层：解析新房列表页面，获取详情页URL和建面面积"""
        page = response.meta.get('page', 1)
        self.logger.info(f'正在爬取新房第{page}页列表')

        # 获取详情页URL列表
        urls = response.xpath("//div[@class='resblock-name']/a/@href").getall()
        # 获取建面面积列表
        areas = response.xpath("//div[@class='resblock-area']/span/text()").getall()

        self.logger.info(f'第{page}页找到 {len(urls)} 个楼盘')

        # 遍历每个楼盘，请求详情页
        for area, url in zip(areas, urls):
            # 如果URL是相对路径，需要拼接完整URL
            if not url.startswith('http'):
                url = response.urljoin(url)

            yield scrapy.Request(
                url,
                callback=self.parse_detail,
                headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
                },
                meta={'area': area.strip()},
                dont_filter=True
            )

    def parse_detail(self, response):
        """第二层：解析详情页，提取楼盘详细信息"""
        try:
            item = NewHouseItem()

            # 楼盘名称
            item['name'] = response.xpath("//div[@class='title-wrap']//h2/text()").get('').strip()
            self.logger.info(f'正在爬取楼盘: {item["name"]}')

            # 类型（从标签中提取）
            item['house_type'] = response.xpath("//div[@class='tags-wrap']/span[@class='tag-item house-type-tag']/text()").get('').strip()

            # 地点（位置信息）
            item['location'] = response.xpath("//ul[@class='info-list']//span[@class='content']/text()").get('').strip()

            # 房型（从详情页提取）
            room_type = response.xpath("//ul[@class='info-list']//li[contains(text(), '户型')]/following-sibling::li/span[@class='content']/text()").get('')
            if not room_type:
                room_type = response.xpath("//div[@class='huxing-info']//span/text()").get('')
            item['room_type'] = room_type.strip()

            # 面积（从列表页传递过来）
            item['area'] = response.meta.get('area', '')

            # 单价（从价格区域提取）
            unit_price = response.xpath("//div[@class='price']//span[@class='unit']/text()").get('')
            if not unit_price:
                unit_price = response.xpath("//div[@class='price-item']//span[contains(text(), '元/平')]/text()").get('')
            item['unit_price'] = unit_price.strip()

            # 总价（从价格区域提取）
            total_price = response.xpath("//div[@class='price']/span[@class='price-number']/text()").get('')
            if not total_price:
                total_price = response.xpath("//div[@class='price-item']//span[@class='total']/text()").get('')
            item['total_price'] = total_price.strip()

            # 只有当楼盘名称存在时才返回数据
            if item['name']:
                yield item
            else:
                self.logger.warning(f'未能提取到楼盘名称: {response.url}')

        except Exception as e:
            self.logger.error(f'解析详情页时出错: {e}, URL: {response.url}')
            import traceback
            self.logger.error(traceback.format_exc())
