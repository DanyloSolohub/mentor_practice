import scrapy
from quotes import models as dj
from itemadapter import ItemAdapter
from scrapy.crawler import CrawlerRunner
from scrapy.item import Item, Field
from twisted.internet import reactor
from twisted.internet.error import ReactorNotRestartable


class AuthorItem(Item):
    user = Field()
    fullname = Field()
    born_date = Field()
    born_location = Field()
    description = Field()


class QuoteItem(Item):
    user = Field()
    author = Field()
    quote = Field()
    tags = Field()


class Pipeline:
    def open_spider(self, spider):
        self._db_authors: dict[str, int] = {}
        self._db_tags: dict[str, int] = {}

        self.authors = []
        self.quotes = []

    def _get_tags(self, tags: list[str]) -> list:
        tags_db = []

        for tag in tags:
            db_tag = self._db_tags.get(tag)

            if not db_tag:
                try:
                    new_tag = dj.Tag.objects.get(name=tag)
                except dj.Tag.DoesNotExist:
                    new_tag = dj.Tag(name=tag)
                    new_tag.save()

                db_tag = new_tag

            tags_db.append(db_tag)

        return tags_db

    def close_spider(self, spider):
        for item in self.authors:
            try:
                author = dj.Author.objects.get(fullname=item['fullname'])
            except dj.Author.DoesNotExist:
                author = dj.Author(**item)
                author.save()

            self._db_authors[item['fullname']] = author

        for item in self.quotes:
            quote_text = str(item['quote']).lstrip('“').rstrip('”')

            if not dj.Quote.objects.filter(quote=quote_text).exists():
                quote = dj.Quote(
                    user=item['user'],
                    author=self._db_authors[item['author']],
                    quote=quote_text
                )
                quote.save()
                quote.tags.set(self._get_tags(item['tags']))

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        if isinstance(item, AuthorItem):
            self.authors.append(adapter.asdict())
        elif isinstance(item, QuoteItem):
            self.quotes.append(adapter.asdict())

        return item


class QuotesSpider(scrapy.Spider):
    name = 'quotes_and_authors'
    custom_settings = {
        "ITEM_PIPELINES": {Pipeline: 300}
    }
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com/']

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

    def parse(self, response, *args, **kwargs):
        for quote in response.xpath("/html//div[@class='quote']"):
            yield QuoteItem(
                user=self.user,
                tags=quote.xpath("div[@class='tags']/a/text()").extract(),
                author=quote.xpath("span/small/text()").get().strip(),
                quote=quote.xpath("span[@class='text']/text()").get().strip()
            )

            yield scrapy.Request(
                self.start_urls[0] + quote.xpath("span/a/@href").get(),
                callback=self.get_author
            )

        next_link = response.xpath("//li[@class='next']/a/@href").get()
        if next_link:
            yield scrapy.Request(url=self.start_urls[0] + next_link)

    def get_author(self, response):
        body = response.xpath('/html//div[@class="author-details"]')

        yield AuthorItem(
            user=self.user,
            fullname=body.xpath('h3[@class="author-title"]/text()').get().strip(),
            born_date=body.xpath('p/span[@class="author-born-date"]/text()').get().strip(),
            born_location=body.xpath('p/span[@class="author-born-location"]/text()').get().strip(),
            description=body.xpath('div[@class="author-description"]/text()').get().strip(),
        )


def scrape_quotes(user) -> None:
    try:
        runner = CrawlerRunner()

        d = runner.crawl(QuotesSpider, user=user)
        d.addBoth(lambda _: reactor.stop())  # noqa
        reactor.run()  # noqa
    except ReactorNotRestartable as e:
        print('ReactorNotRestartable:', e)
