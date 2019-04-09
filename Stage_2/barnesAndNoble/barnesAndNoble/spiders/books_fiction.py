# -*- coding: utf-8 -*-
import scrapy
import urllib.parse as urlparse


class BooksFictionSpider(scrapy.Spider):
    name = 'books_fiction'
    allowed_domains = ['www.barnesandnoble.com']
    start_urls = [
        'https://www.barnesandnoble.com/b/books/fiction/literary-fiction/_/N-29Z8q8Z10k1?Nrpp=40/',
        'https://www.barnesandnoble.com/b/books/fiction/fiction-literature-classics/_/N-29Z8q8Z11hi?Nrpp=40/',
        'https://www.barnesandnoble.com/b/books/biography/entertainment-biography/_/N-29Z8q8Zsp8?Nrpp=40/',
        'https://www.barnesandnoble.com/b/books/history/ancient-history/_/N-29Z8q8Z11tt?Nrpp=40/',
        'https://www.barnesandnoble.com/b/books/biography/political-biography/_/N-29Z8q8Zt0w?Nrpp=40',
        'https://www.barnesandnoble.com/b/books/fiction/historical-fiction/_/N-29Z8q8Z10nf?Nrpp=40',
        'https://www.barnesandnoble.com/b/books/literature/world-fiction/_/N-29Z8q8Z1pi4?Nrpp=40',
        'https://www.barnesandnoble.com/b/books/biography/sports-adventure-biography/_/N-29Z8q8Zt29?Nrpp=40'
        ]

    max_page_count = 50

    def parse(self, response):
        print("processing " + response.url)
        parsed_url = urlparse.urlparse(response.url)
        search_params = urlparse.parse_qs(parsed_url.query)
        if 'page' in search_params:
            page_count = int(search_params['page'][0])
        else:
            page_count = 1

        # get links of book description pages
        urls = response.css("div.product-shelf-title a::attr(href)").extract()

        for url in urls:
            yield scrapy.Request(
                response.urljoin(url),
                callback=self.parseBookInfo
            )

        # Handle Pagination
        if page_count < self.max_page_count:
            next_page_url = response.css("li.pagination__next a::attr(href)").extract_first()
            if next_page_url:
                yield scrapy.Request(
                    response.urljoin(next_page_url),
                    callback=self.parse
                )

    def parseBookInfo(self, response):
        print("processing " + response.url)

        # here collect all info about the book using css selectors

        title = response.css("h1.pdp-header-title::text").get()
        authors = response.css("span#key-contributors a::text").get()
        book_format = response.css("h2#pdp-info-format::text").get()
        cur_price = '$' + response.css("span#pdp-cur-price::text").get()
        old_price = response.css("s.old-price::text").get()
        if not old_price:
            old_price = cur_price
        isbn13 = response.xpath("//tr[th='ISBN-13:']/td[1]/text()").get()
        publisher = response.xpath("//tr[th='Publisher:']/td[1]/a/text()").get()
        publication_date = response.xpath("//tr[th='Publication date:']/td[1]/text()").get()
        pages = response.xpath("//tr[th='Pages:']/td[1]/text()").get()
        product_dimenstions = response.xpath("//tr[th='Product dimensions:']/td[1]/text()").get()

        scraped_info = {
            'title': title,
            'authors': authors,
            'book_format': book_format,
            'cur_price': cur_price,
            'old_price': old_price,
            'isbn13': isbn13,
            'publisher': publisher,
            'publication_date': publication_date,
            'pages': pages,
            'product_dimensions': product_dimenstions
        }

        yield scraped_info


#appends results to csv in each run.
