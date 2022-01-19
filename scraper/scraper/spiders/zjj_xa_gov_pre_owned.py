from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from ..items.zjj_xa_gov_pre_owned import PreOwnedItemLoader, PreOwnedItem


class ZjjXaGovPreWonedSpider(CrawlSpider):
    """西安住建局二手房发布数据"""
    name = 'zjj_xa_gov_pre_woned'
    allowed_domains = ['zjj.xa.gov.cn']
    start_urls = [
        'https://zjj.xa.gov.cn/esfgp/index.aspx?a1=10',
        'https://zjj.xa.gov.cn/esfgp/index.aspx?a1=20',
        'https://zjj.xa.gov.cn/esfgp/index.aspx?a1=30',
        'https://zjj.xa.gov.cn/esfgp/index.aspx?a1=40',
        'https://zjj.xa.gov.cn/esfgp/index.aspx?a1=50',
        'https://zjj.xa.gov.cn/esfgp/index.aspx?a1=60',
        'https://zjj.xa.gov.cn/esfgp/index.aspx?a1=65',
        'https://zjj.xa.gov.cn/esfgp/index.aspx?a1=68',
        'https://zjj.xa.gov.cn/esfgp/index.aspx?a1=69'
    ]
    rules = [
        # 按地域搜索二手房列表页面
        Rule(LinkExtractor(allow=('index\.aspx\?a1=10',)), callback='parse_region_list', cb_kwargs={"region": "碑林区"}),
        Rule(LinkExtractor(allow=('index\.aspx\?a1=20',)), callback='parse_region_list', cb_kwargs={"region": "莲湖区"}),
        Rule(LinkExtractor(allow=('index\.aspx\?a1=30',)), callback='parse_region_list', cb_kwargs={"region": "新城区"}),
        Rule(LinkExtractor(allow=('index\.aspx\?a1=40',)), callback='parse_region_list', cb_kwargs={"region": "雁塔区"}),
        Rule(LinkExtractor(allow=('index\.aspx\?a1=50',)), callback='parse_region_list', cb_kwargs={"region": "未央区"}),
        Rule(LinkExtractor(allow=('index\.aspx\?a1=60',)), callback='parse_region_list', cb_kwargs={"region": "灞桥区"}),
        Rule(LinkExtractor(allow=('index\.aspx\?a1=65',)), callback='parse_region_list', cb_kwargs={"region": "高新区"}),
        Rule(LinkExtractor(allow=('index\.aspx\?a1=68',)), callback='parse_region_list', cb_kwargs={"region": "曲江新区"}),
        Rule(LinkExtractor(allow=('index\.aspx\?a1=69',)), callback='parse_region_list',
             cb_kwargs={"region": "经济技术开发区"}),
        # 列表分页解析
        Rule(LinkExtractor(allow=('index\.aspx\?.*page=')))
    ]

    def parse_region_list(self, response, **kwargs):
        """
        解析区域列表页面
        :param response:
        :param kwargs:
        :return:
        """
        # # 列表项数据
        # detail_link_extractor = LinkExtractor(allow=('fyxq\.aspx\?id='), restrict_xpaths=('//*[@id="datalist"]',))
        # detail_links = detail_link_extractor.extract_links(response)

        # 检测对应房源是否被标记为存在抵押 exists_mortgage
        detail_links = {}
        detail_link_blocks = response.xpath('//*[@id="datalist"]/div[@class="esf_fylb"]')
        for block_sel in detail_link_blocks:
            detail_link = block_sel.xpath('div[@class="esf_fyhym"]//a/@href').get()
            non_mortgage = block_sel.xpath('div[@class="esf_fyjbxx"]//img[@src="img/ydy.png"]/@style').re(
                'display: (none)')
            detail_links[detail_link] = bool(non_mortgage)  # True 没有抵押， False 有抵押

        for detail_link in detail_links:
            yield response.follow(
                detail_link,
                callback=self.parse_detail,
                cb_kwargs={
                    **kwargs,
                    'exists_mortgage': not detail_links[detail_link]
                }
            )

    def parse_detail(self, response, **kwargs):
        """
        二手房详情页解析
        :param response:
        :return:
        """

        pre_owned_item_loader = PreOwnedItemLoader(
            item=PreOwnedItem(),
            response=response
        )

        pre_owned_item_loader.add_xpath('reference_monthly_repayment', '//*[@id="lbl_ckyg"]/text()')
        pre_owned_item_loader.add_xpath('building_area', '//*[@id="lbl_jzmj"]/text()')
        pre_owned_item_loader.add_xpath('building_layout', '//*[@id="lbl_hx"]/text()')
        pre_owned_item_loader.add_xpath('floor_level', '//*[@id="lbl_zcs"]/text()')
        pre_owned_item_loader.add_xpath('age_of_building', '//*[@id="lbl_jznf"]/text()')
        pre_owned_item_loader.add_xpath('decoration_type', '//*[@id="lbl_zxqk"]/text()')
        pre_owned_item_loader.add_xpath('building_orientation', '//*[@id="lbl_cx"]/text()')
        pre_owned_item_loader.add_xpath('building_structure', '//*[@id="lbl_jzjg"]/text()')
        pre_owned_item_loader.add_xpath('building_type', '//*[@id="lbl_yt"]/text()')
        pre_owned_item_loader.add_xpath('building_description', '//*[@id="lbl_fyms"]/text()')
        pre_owned_item_loader.add_xpath('residential_quarter', '//*[@id="lbl_xq"]/text()')
        pre_owned_item_loader.add_xpath('address', '//*[@id="lbl_fbzl"]/text()')
        pre_owned_item_loader.add_xpath('affiliated_transportation', '//*[@id="lbl_jtqk"]/text()')
        pre_owned_item_loader.add_xpath('affiliated_facilities', '//*[@id="lbl_ptss"]/text()')
        pre_owned_item_loader.add_xpath('published_at', '//*[@id="lbl_fbsj"]/text()')
        pre_owned_item_loader.add_value('info_from', response.url)
        pre_owned_item_loader.add_xpath('check_code', '//*[@id="lbl_fyhym"]/text()')
        pre_owned_item_loader.add_value('exists_mortgage', kwargs['exists_mortgage'])
        pre_owned_item_loader.add_value('region', kwargs['region'])

        pre_owned_item = pre_owned_item_loader.load_item()
        yield pre_owned_item
