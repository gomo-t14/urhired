# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Jobs(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    job_id = scrapy.Field()
    Industry = scrapy.Field() # will be hardcoded according tp which url the spider is running 
    Title = scrapy.Field()
    Company = scrapy.Field()
    Location = scrapy.Field()
    Renumeration = scrapy.Field()
    Type_of_Work = scrapy.Field()
    Experience = scrapy.Field()
    Employment_type = scrapy.Field()
    Operating_mode = scrapy.Field()
    Requirements = scrapy.Field()
    Description = scrapy.Field()
    Url = scrapy.Field()
    Keywords = scrapy.Field() #to be populated in pipeline  using minstral model to help withh job search 



   