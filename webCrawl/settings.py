# Scrapy settings for webCrawl project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = "webCrawl"

SPIDER_MODULES = ["webCrawl.spiders"]
NEWSPIDER_MODULE = "webCrawl.spiders"

ADDONS = {}


# Webページをダウンロードするのに何秒の間隔を空けるか
DOWNLOAD_DELAY = 5  # 5秒
DOWNLOAD_TIMEOUT: 10
RETRY_TIMES= 3
DEPTH_LIMIT    = 2  # クロールできる最新深度 

# HTTPのキャッシュ設定
## 同じページを何度もダウンロードしないようにする
HTTPCACHE_ENABLED           = True
HTTPCACHE_EXPIRATION_SECS   = 0
HTTPCACHE_DIR               = 'httpcache'
HTTPCACHE_IGNORE_HTTP_CODES = []
HTTPCACHE_STORAGE           = 'scrapy.extensions.httpcache.FilesystemCacheStorage'



# パイプライン設定
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   "webCrawl.pipelines.WebcrawlPipeline": 300,
}

FEED_EXPORT_ENCODING = "utf-8"
