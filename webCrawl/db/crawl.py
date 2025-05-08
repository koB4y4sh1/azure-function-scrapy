from webCrawl.db.client import client
from webCrawl.items import WebcrawlItem

def save_crawl_data(item: WebcrawlItem):
    response = client.table("crawl").insert({
        "url": item["url"],
        "title": item["title"],
        "content": item["content"],
    }).execute()
    return response