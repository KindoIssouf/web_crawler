import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from bs4 import BeautifulSoup
import hashlib
import re


class KennesawSpiderSpider(CrawlSpider):
    name = 'kennesaw_spider'
    allowed_domains = ['kennesaw.edu']
    start_urls = ['https://www.kennesaw.edu/',
                  'https://ccse.kennesaw.edu/',
                  'https://hr.kennesaw.edu/']
    headers = {
        'User-Agent': 'KSU CS4422-IRbot/0.1',
    }

    rules = (
        Rule(LinkExtractor(allow=r'kennesaw.edu', canonicalize=False,
                           unique=True), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        soup = BeautifulSoup(str(response.text), 'html.parser')
        entry = dict.fromkeys(['pageid', 'url', 'title', 'body', 'emails'])
        pageid = str(response.url).encode()
        entry["pageid"] = hashlib.md5(pageid).hexdigest()
        entry["url"] = response.url
        entry["title"] = response.css('title::text').get()
        entry["emails"] = re.findall("[a-zA-Z]+@[a-z.]+", str(response.text))
        entry["body"] = soup.get_text()
        yield entry
