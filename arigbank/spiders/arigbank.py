import scrapy
from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst
from datetime import datetime
from arigbank.items import Article


class arigbankSpider(scrapy.Spider):
    name = 'arigbank'
    start_urls = ['https://www.arigbank.mn/mn/news']

    def parse(self, response):
        links = response.xpath('//a[@class="btn-link"]/@href').getall()
        print(links[0])
        links = [link[0] + 'mn' + link[1:] for link in links]
        yield from response.follow_all(links, self.parse_article)

    def parse_article(self, response):
        if 'pdf' in response.url.lower():
            return

        item = ItemLoader(Article())
        item.default_output_processor = TakeFirst()

        title = response.xpath('//h2/text()').get()
        if title:
            title = title.strip()

        content = response.xpath('//div[@class="blog-content"]//text()').getall()
        content = [text.strip() for text in content if text.strip() and '{' not in text]
        content = " ".join(content).strip()

        item.add_value('title', title)
        item.add_value('link', response.url)
        item.add_value('content', content)

        return item.load_item()
