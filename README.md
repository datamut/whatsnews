## whatsnews (what's news)
**v0.0.1**

----

### Introduction
**Whatsnews** is a system used for scrawling content from news websites like bbc
and the guardian. It is only for development use.

Requirements is based on an interview test. Details of this test is confidential
and will not be mentioned here. Project name, naming of variables and comments
do not contain any thing related with this test.


### Sub modules/systems/services
This project consists of several different sub systems as below:
+ index_crawler - to crawl article urls from news websites
+ article_crawler - to crawl article content using urls fetched above
+ index_builder - to build index to mongodb/search-engine for full text search
+ auth_api - API used to grant privilege of using other APIs like search_api for external users
+ auth_service - centralized authorization service, called by auth_api and other APIs
+ search_api - search interface for users
+ search_service - service in charge of full text search on news content in search engine mentioned above
+ query_service - service used to process user's input queries, e.g. extend relevant queries, change queries, etc.
+ rank_service - service used for sorting search result, e.g. sort according user's profile/preferences

A flowchart will be provided for better understanding of this project.


### Environment
This version use [MongoDB](https://www.mongodb.com) as database and full text search engine. Crawler use [Scrapy](https://scrapy.org) as crawler engine, and [Kafka](http://kafka.apache.org) is used for scalability. [Readability](https://pypi.python.org/pypi/readability-lxml) is used for distilling the content of articles. Services and APIs mainly use [Python](https://www.python.org) and [Flask](http://flask.pocoo.org) framework. Development version of these tools are listed below:

+ MongoDB 3.2.9
+ Kafka 2.11-0.10.0.0
+ Python 3.5.2
+ Scrapy 1.1.2
+ Flask 0.11.1

Requirement details of each sub project can be found in its root directory.


### API Usage
```python
>>> import requests
>>> requests.get('http://authapi.kc7ctmpd2z.us-west-2.elasticbeanstalk.com/token/ID123456/123456').json()
{'token': 'TK123456', 'expires_in': 86400}
>>> requests.post('http://searchapi.kc7ctmpd2z.us-west-2.elasticbeanstalk.com/search/ID123456/TK123456', data={'query': 'Guinness World Records'}).json()[0]
>>> ...
```

**A very basic web interface has been built for an easier interact:**[Search on What's News](http://searchapi.kc7ctmpd2z.us-west-2.elasticbeanstalk.com)


### Project flowchart
*Coming soon*
