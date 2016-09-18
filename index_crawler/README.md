## Index crawler
----

### Description
Crawler used only to fetch article urls from a certain news website. It crawl news website and find article urls and then write these urls down to INDEX_OUT_FILE (see settings.py). The purpose of this is to decouple different crawlers and make it more scalable.

### Crawler Speed
This project is not for real world crawling. So we set a very slow crawling speed to be polite. Download speed is 1 page per 5 seconds and currency is 1. Tasks will only run for an acceptable period of time. Local static files will be used for development/testing purpose. Settings related with crawling speed showed below:
```python
DOWNLOAD_DELAY = 5
CONCURRENT_REQUESTS_PER_DOMAIN = 1
```

### Additional Settings
Result output file is configurable by modifying INDEX_OUT_FILE value in settings.py.
```python
INDEX_OUT_FILE = '/your/path/to/index_out.file'
```

Two pipelines are used in this module. Pipeline *index_crawler.pipelines.DuplicatesPipeline* is used for skipping crawled urls in local machine. For a standalone small size crawler, this pipeline is effective. For a distributed small size crawler, urls can be hashed to a certain node to make this pipeline effective. But this DuplicatesPipeline is not ideal enough, cause it only record crawled url in local memory. That means crawled urls record will lose after a restart. So, **TODO: a more effective way of skipping crawled urls is required**.

The other pipeline here, named *index_crawler.pipelines.IndexWriterPipeline*, is for writing article urls found in current page to a file. We set a higher priority to *index_crawler.pipelines.DuplicatesPipeline* than *index_crawler.pipelines.IndexWriterPipeline* for a correct logic.
