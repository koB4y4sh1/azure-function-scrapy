# Pipeline
# Spider より渡された Items に対する処理を記述します
# DB への保存、ファイル出力など目的に応じて自由に処理を記述できます


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from webCrawl.db.crawl import save_crawl_data
import json
import os

class WebcrawlPipeline:

    def process_item(self, item, spider):
        """
        itemを加工・保存する
        """
        # 各行の前後空白を除去し、空でない行だけをスペースで連結
        item['content'] = " ".join(
            line.strip() for line in item['content'].splitlines() if line.strip()
        )
        self.save_db(item) # supabaseに保存
        self.save_txt(item) # data/output.txtに出力
        return item

    def save_db(self, item):
        """
        itemをDBに保存する
        """
        # TODO:DB保存の条件分岐処理

        # DB保存
        save_crawl_data(item)

    def save_txt(self, item):
        """
        itemをoutput.txtに出力する
        """
        output_path = os.path.join(os.getcwd(), "data", "output.txt")
        with open(output_path, "a", encoding="utf-8") as f:
            json.dump(dict(item), f, ensure_ascii=False)
            f.write("\n")
