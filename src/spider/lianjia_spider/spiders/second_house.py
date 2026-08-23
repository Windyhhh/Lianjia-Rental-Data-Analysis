# 链家二手房爬虫
import scrapy
from lianjia_spider.items import SecondHouseItem


class SecondHouseSpider(scrapy.Spider):
    """链家二手房爬虫 - 爬取第3-7页数据"""

    name = 'second_house'
    allowed_domains = ['lianjia.com']

    def start_requests(self):
        """生成请求 - 二手房第3-7页"""
        base_url = 'https://bj.lianjia.com/ershoufang/'

        for page in range(3, 8):  # 第3-7页
            url = f'{base_url}pg{page}/'
            yield scrapy.Request(
                url,
                callback=self.parse,
                headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
                },
                meta={'page': page}
            )

    def parse(self, response):
        """解析二手房列表页面"""
        page = response.meta.get('page', 1)
        self.logger.info(f'正在爬取二手房第{page}页')

        # 使用正确的选择器提取每个二手房项目
        houses = response.xpath('//li[@class="clear LOGCLICKDATA"]')

        if not houses:
            # 尝试其他可能的选择器
            houses = response.xpath('//ul[@class="sellListContent"]/li[@class="clear"]')

        self.logger.info(f'第{page}页找到 {len(houses)} 套二手房')

        for house in houses:
            try:
                item = SecondHouseItem()

                # 小区名称
                community = house.xpath('.//div[@class="title"]//a/text()').get('')
                if not community:
                    community = house.xpath('.//a[@data-el="region"]/text()').get('')
                item['community_name'] = community.strip()

                # 地点（位置信息）
                location = house.xpath('.//div[@class="positionInfo"]//a/text()').getall()
                if not location:
                    location = house.xpath('.//div[@class="flood"]//a/text()').getall()
                item['location'] = ' '.join([loc.strip() for loc in location if loc.strip()])

                # 房型（不拆分，保持原样）
                room_info = house.xpath('.//div[@class="houseInfo"]/text()').get('')
                if not room_info:
                    room_info = house.xpath('.//div[@class="houseInfo"]//text()').getall()
                    room_info = ' '.join([r.strip() for r in room_info if r.strip()])
                item['room_type'] = room_info.strip().split('|')[0].strip() if '|' in str(room_info) else room_info.strip()

                # 单价
                unit_price = house.xpath('.//div[@class="unitPrice"]//span/text()').get('')
                if not unit_price:
                    unit_price = house.xpath('.//div[@class="unitPrice"]/text()').get('')
                item['unit_price'] = unit_price.strip()

                # 总价
                total_price = house.xpath('.//div[@class="totalPrice"]//span/text()').get('')
                if not total_price:
                    total_price = house.xpath('.//div[@class="totalPrice"]/text()').get('')
                item['total_price'] = total_price.strip()

                # 只有当小区名称存在时才返回数据
                if item['community_name']:
                    yield item
                else:
                    self.logger.warning(f'未能提取到小区名称')

            except Exception as e:
                self.logger.error(f'解析二手房项目时出错: {e}')
                import traceback
                self.logger.error(traceback.format_exc())
                continue
