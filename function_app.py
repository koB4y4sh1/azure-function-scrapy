import logging
import azure.functions as func
from multiprocessing import Process

from dotenv import load_dotenv
from scrapy.utils.project import get_project_settings
from scrapy.crawler import CrawlerProcess 
from webCrawl.spiders.WebCrawlSpider import WebCrawlSpider

app = func.FunctionApp()
load_dotenv()

def do_crawl():
    """
    Scrapyのクローラーを実行する関数。

    この関数は、Scrapyの設定を取得し、WebCrawlSpiderを指定して
    クローリング処理を開始します。クローラーは新しいプロセスで実行されます。
    """
    settings = get_project_settings() # scrapy.cfgに記載されたsettings情報を取得
    process = CrawlerProcess(settings)
    process.crawl(WebCrawlSpider)
    process.start()


@app.timer_trigger(schedule="0 0 * * * *", arg_name="myTimer", run_on_startup=False,
              use_monitor=False) 
def crawl_scrapy(myTimer: func.TimerRequest) -> None:
    if myTimer.past_due:
        logging.info('🚨 タイマーが期限を過ぎています！')
    
    logging.info('🔧 Python タイマートリガー関数が実行されました。')
    try:
        # Function実行毎に独立したプロセス空間でScrapyを実行させる (https://qiita.com/shiozaki/items/cd5242a3fc488f1a3bf6)
        # Scrapyを直接同一プロセスで複数回実行しようとすると、非同期フレームワークTwistedが使用するReactor（イベントループ）が
        # 一度しか起動できない仕様のため、「ReactorNotRestartable」エラーが発生する。
        # これを回避するため、毎回別プロセス（multiprocessing）でクローラーを実行する必要がある。
        process = Process(target=do_crawl)
        process.start()
        process.join()
        logging.info('✅ Scrapy クローリングが正常に完了しました')
    
    except Exception as e:
        logging.exception(f"❌ クローリング中に予期しないエラーが発生しました: {e}")
        raise e