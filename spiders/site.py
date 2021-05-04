import scrapy
import logging

class SiteSpider(scrapy.Spider):
    name = 'site'
    allowed_domains = ['www.a2zproperty.in']
    start_urls = ['https://www.a2zproperty.in/Gujarat/Ahmedabad/index.html']

    def parse(self, response):
        areas= response.xpath("/html/body/section[2]/div/div[2]/div/a")
        for area in areas:
            # name=area.xpath(".//text()").getall()
            area_link = area.xpath(".//@href").get()

            yield response.follow(url=area_link, callback=self.parse_sites)

    def parse_sites(self, response):
        sites = response.xpath("/html/body/section[2]/div/div[2]/div")
        for site in sites:
            site_link = site.xpath(".//div[1]/div/div[2]/a/@href").get()

            yield response.follow(url=site_link, callback=self.parse_data)

    def parse_data(self, response):
        infos = response.xpath("/html/body/section[@class='bg-shadow']/table/tbody")
        for info in infos:
            name = info.xpath(".//tr[1]/td[2]/h4[@class='h4-125']/text()").get()
            add = info.xpath(".//tr[1]/td[2]/p[@class='font-12 mb-0']/text()").get()
            contact = info.xpath(".//tr[2]/td[2]/h4[@class='h4-125']/text()").get()
            promoter = info.xpath(".//tr[5]/td[2]/p[@class='mb-0']/text()").get()
            StartDate = info.xpath(".//tr[7]/td[2]/p[@class='mb-0']/text()").get()
            EndDate = info.xpath(".//tr[8]/td[2]/p[@class='mb-0']/text()").get()
            AreaOfPlot = info.xpath(".//tr[9]/td[2]/p[@class='mb-0']/text()").get()
            projectType = info.xpath(".//tr[12]/td[2]/p[@class='mb-0']/text()").get()
            Architect = info.xpath(".//tr[13]/td[2]/p[@class='mb-0']/text()").get()
            Stucture = info.xpath(".//tr[14]/td[2]/p[@class='mb-0']/text()").get()

            yield {
                'Site Name': name,
                'Site Address': add,
                'Contact No.': contact,
                'Promoter': promoter,
                'Start Date': StartDate,
                'End Date': EndDate,
                'Area Of Project': AreaOfPlot,
                'Project Type': projectType,
                'Architect': Architect,
                'Structure': Stucture
            }