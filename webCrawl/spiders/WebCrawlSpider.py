# Spider
# クロール対象のサイトへのリクエスト、レスポンスのパース処理を記述します
# どのようにサイトを辿って、ページの内容をどうパースするかのロジックが Spider に書かれます
import os
import json
from pathlib import Path
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from urllib.parse import urlparse

from webCrawl.items import WebcrawlItem



class WebCrawlSpider(CrawlSpider):
    """
    start_urls.jsonで指定されたURLリストからクロールを開始し、
    サイト内の「/item/」配下のページのみをLinkExtractorでたどりながら、
    最大100ページまでページ情報（URL、タイトル、本文テキスト）を収集するScrapyクローラー。

    LinkExtractorのallow/denyパターンにより、
    「/item/」以下のページのみをクロール対象とし、
    「images」「localshops」「#」「imgview」「pricehistory」を含むURLは除外します。

    クロール対象ドメイン（allowed_domains）はstart_urlsから自動的に設定されます。

    属性:
        name (str): このクローラーの名前（Scrapyでの識別子）。
        allowed_domains (list): クロール対象とするドメインのリスト（start_urls.jsonから取得）。
        start_urls (list): クロール開始となるURLリスト（start_urls.jsonから取得）。
        max_pages (int): クロールする最大ページ数（デフォルト100）。
        page_count (int): 現在クロールしたページ数。

    ルール:
        - LinkExtractor: クロールされたページからどのようにリンクを抽出するかを指定する。何も指定しなかった場合はそのページの中の全てのリンクを抽出する。
          - allow: 正規表現でマッチしたリンクを抽出する。何も与えられない場合は全てのリンクにマッチする。
          - deny : 正規表現でマッチしたリンクを除外する。allowよりも優先度が高い。指定されていない場合はリンクを除外しない
        - callback: 指定した文字列の名前のメソッドにレスポンスを渡す。
    """
    name = "webCrawl"
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name= "webCrawl"
        start_urls = self.get_urls()
        self.allowed_domains = [urlparse(url).netloc for url in start_urls]
        self.start_urls = start_urls
        self.page_count = 0
        self.max_pages = 100

    rules = (
        Rule(
            LinkExtractor(
                allow=r'/*/',  # 許可するリンクパターン
                deny=r'/item/.*/(images|localshops|#|imgview|pricehistory).*' # 拒否するリンクパターン
            ),
            callback='parse', # parse関数にresponseを渡す
            follow=True
            ),
    )

    def parse(self, response):
        """
        パース処理を行い、WebCrawlItemにクロールしたページの情報を格納する。
        """
        if self.page_count >= self.max_pages:
            self.crawler.engine.close_spider(self, 'Page limit reached')
            return
        self.page_count += 1
        item = WebcrawlItem()
        item['title'] = response.xpath('//title/text()').get()
        item['content'] = " ".join(response.css("body *::text").getall()).strip()
        item['url'] = response.url
        yield item

    def get_urls(self, path=None):
        """
        Webクロール先のURLリストを取得する。
        """
        if path is None:
            base_dir = Path(__file__).resolve().parents[2]
            path = os.path.join(base_dir, "data", "start_urls.json")
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data.get("urls", [])
