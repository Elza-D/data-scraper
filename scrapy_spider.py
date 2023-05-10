import scrapy

class GameSpider(scrapy.Spider):
    name = 'gamespider'
    start_urls = ['https://www.metacritic.com/browse/games/score/metascore/all/all/filtered']

    def parse(self, response):
        # Loop through each game summary block and extract relevant data from listings page
        for games in response.css('td.clamp-summary-wrap'):
            items = {
                'title': games.css('.title h3::text').get(), 
                'release date': games.css('.platform+ span::text').get(),  
                'metascore': games.css('.positive::text').get(), 
                'platform': games.css('.platform .data::text').extract_first().strip(), 
                'genre': None, 
                'userscore': None, 
                'nr of user reviews': None, 
                'nr of critic reviews': None,
            }
            yield items
        
            # Follow each link to a game's details page and parse information
            urls = response.css('td.clamp-summary-wrap > a::attr(href)').extract()
            for url in urls:
                url = response.urljoin(url)
                yield scrapy.Request(url=url, callback=self.parse_details, meta={'items': items})

            # Follow pagination links to scrape additional pages of games
            for next_page in response.css('a.action'): 
                yield response.follow(next_page, self.parse)
        
    # Define callback function to extract information from a game's details page
    def parse_details(self, response):
        items = response.meta['items']
        items['genre'] = response.xpath('normalize-space(//*[contains(concat( " ", @class, " " ), concat( " ", "product_genre", " " ))]//*[contains(concat( " ", @class, " " ), concat( " ", "data", " " ))]/text())').extract()
        items['userscore'] = response.xpath('normalize-space(//*[contains(concat( " ", @class, " " ), concat( " ", "large", " " ))]/text())').extract_first() 
        rating_text = response.xpath('normalize-space(//*[contains(concat( " ", @class, " " ), concat( " ", "feature_userscore", " " ))]//a/text())').extract()[-1].strip() 
        items['nr of user reviews'] = int(rating_text.split()[0]) 
        items['nr of critic reviews'] = response.xpath('normalize-space(//*[contains(concat( " ", @class, " " ), concat( " ", "highlight_metascore", " " ))]//*[contains(concat( " ", @class, " " ), concat( " ", "count", " " ))]//text())').re_first('\d+')
        yield items