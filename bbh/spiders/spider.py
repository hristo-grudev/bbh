import scrapy

from scrapy.loader import ItemLoader
from ..items import BbhItem
from itemloaders.processors import TakeFirst


class BbhSpider(scrapy.Spider):
	name = 'bbh'
	start_urls = ['https://www.bbh.com/global/en/insights/library.html']

	def parse(self, response):
		post_links = response.xpath('//h2[@class="cmp-teaser__title "]/a/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

	def parse_post(self, response):
		title = response.xpath('//h2[@class="cmp-teaser__title "]/text()').get()
		description = response.xpath('//div[@class="cmp-text t-cmp-dna"]//text()[normalize-space()]').getall()
		description = [p.strip() for p in description]
		description = ' '.join(description).strip()
		date = response.xpath('//div[@class="cmp-teaser__tout-date"]/text()').get()

		item = ItemLoader(item=BbhItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
