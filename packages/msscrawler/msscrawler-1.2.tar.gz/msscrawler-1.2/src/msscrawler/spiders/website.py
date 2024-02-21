from ..items.website_item import WebsiteItem
from .base import BaseSpider
import scrapy
from twisted.internet.error import DNSLookupError
from twisted.internet.error import TimeoutError, TCPTimedOutError


class WebsiteSpider(BaseSpider):
    instance = "website"

    # def __init__(self, url):
    #     super().__init__(url)

    def __init__(self, url, **kwargs):
        super().__init__(url, **kwargs)

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(
                url, callback=self.parse, dont_filter=True, errback=self.err_callback
            )

    @staticmethod
    def get_new_item_instance():
        return WebsiteItem()

    def set_default_value(self):
        items = super().set_default_value()
        items["css_selector"] = ""
        items["categories_num"] = []
        items["total_categories"] = 0  # update when error

        # use in pipeline to create categories and send message
        items["category_urls"] = []

        items["errors"] = []
        return items

    def err_callback(self, failure):
        items = self.set_default_value()

        if failure.check(DNSLookupError):
            # this is the original request
            request = failure.request
            self.graylog.error(
                f"[x] Error when crawl page {self.instance} (spider {self.name}: {self.instance_url}). \n DNSLookupError on {request.url}"
            )

            items["errors"].append(f"DNSLookupError on {request.url}")

        elif failure.check(TimeoutError, TCPTimedOutError):
            request = failure.request
            self.graylog.error(
                f"[x] Error when crawl page {self.instance} (spider {self.name}: {self.instance_url}). \n TimeoutError on {request.url}"
            )

            items["errors"].append(f"TimeoutError on {request.url}")

        yield items
