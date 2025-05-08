# Items
# クロール対象のデータから抽出したいデータ構造を記述するモデルのようなものです
# 目的に応じて自由な構造を定義できます
# ItemsはSpiderで生成されPipelineに渡されます

import scrapy


class WebcrawlItem(scrapy.Item):
    url       = scrapy.Field()
    title   = scrapy.Field()
    content = scrapy.Field()
    pass
