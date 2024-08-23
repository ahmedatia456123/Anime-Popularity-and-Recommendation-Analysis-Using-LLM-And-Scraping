from typing import Any
import scrapy
from scrapy.http import Response


class AnimiesSpider(scrapy.Spider):
    name = "animies"
    allowed_domains = ["blkom.com"]
    start_urls = ["https://blkom.com/animes-list"]

    def parse(self, response):
        pageination_end = int(response.xpath("//ul[@class='pagination']/li[position() = last() - 1]/a/text()").get())
        page_links = [f"https://blkom.com/animes-list?page={i}" for i in range(1, (pageination_end+1))]
        for link in page_links:
            yield response.follow(url=link,callback=self.parse_animes_list,meta={'max_retry_times':500})

    def parse_animes_list(self,response):
        animes_list = response.xpath("//div[@class='contents text-center']/div/div/div[@class='poster']/a/@href")

        animes_list_links = [link.get() for link in animes_list]

        for link in animes_list_links:
            yield response.follow(url=link,callback=self.parse_anime_data,meta={'max_retry_times':500})


    def parse_anime_data(self,response):
        name = response.xpath("//h1/text()").get().strip()
        rating = response.xpath("//button[@class='rating-box pull-left dropdown-toggle']/span/text()").get()
        myanimelist = response.xpath("//a[@class='blue cta ']/@href").get()
        ep_links_list = response.xpath("//ul[@class='nano-content episodes-links']/li/a/@href")
        for link in ep_links_list:
            yield response.follow(url=link.get(),callback=self.parse_anime_server,meta={'name':name,'rating':rating,'myanimelist':myanimelist,'max_retry_times':500})

    def parse_anime_server(self,response):
        mat_obj = response.request.meta
        name = mat_obj['name']
        rating = mat_obj['rating']
        myanimelist = mat_obj['myanimelist']
        veiws = response.xpath("//div[@class='views']/span/text()").get().strip()
        counting_comment = len(response.xpath("//div[@class='comment-info']"))
        episode_number = response.xpath("//p[@class='episode-number']/text()").get()
        yield{
            'name':name,
            'rating':rating,
            'myanimelist':myanimelist,
            'veiws':veiws,
            'counting_comment':counting_comment,
            'episode_number':episode_number,
        }