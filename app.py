from scrapy import Request
import scrapy
import re


class QuotesSpider(scrapy.Spider):
    name = "grobmart"
    main_url = "https://www.grobmart.com/Buku?page="
    start_urls = [main_url + str(999)]

    def parse(self, response):
        max_page = response.css("ul.pagination a::text").getall()[-3]
        for i in range(1, int(max_page) + 1):
            yield Request(self.main_url + str(i), callback=self.next_parse)

    def next_parse(self, response):
        catalog = response.css("div.product-grid a.product-img::attr(href)")
        for link in catalog:
            link = response.urljoin(link.get())
            yield Request(link, callback=self.parse_detail)

    def parse_detail(self, response):
        detail = response.css("ul.list-unstyled")

        book = {
            "Source": response.url,
            "Judul": response.css("div.title::text").get().strip(),
            "Harga": response.css("div.product-price-new::text")
            .get()
            .replace("Rp", "Rp. ")
            .strip(),
            "Deskripsi": response.css("div.block-description::text").get(),
            "Penulis": detail.css("li.product-manufacturer a::text").get(),
            "Penerbit": detail.css("li.product-publisher a::text").get(),
            "ISBN": detail.css("li.product-model span::text").get(),
            "MPN": detail.css("li.product-mpn span::text").get(),
        }

        yield book
