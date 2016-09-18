## This is a instruction of starting a Kafka developing environment

### Download Kafka
Download Kafka tar ball and unarchive to a directory
```shell
 wget http://apache.mirror.amaze.com.au/kafka/0.10.0.1/kafka_2.11-0.10.0.1.tgz
```

### Zookeeper
Start Zookeeper server
```shell
bin/zookeeper-server-start.sh config/zookeeper.properties
```

### Brokers
Duplicate config/server.properties file and start 3 Brokers:
```shell
bin/kafka-server-start.sh config/server-1.properties
bin/kafka-server-start.sh config/server-2.properties
bin/kafka-server-start.sh config/server-3.properties
```

### Topics
Create topics for index_crawler and article_crawler:
```shell
bin/kafka-topics.sh --list --zookeeper localhost:2181
bin/kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 3 --partitions 18 --topic whatsnews_topic_index
bin/kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 3 --partitions 18 --topic whatsnews_topic_article
```

### Producers
Here we use Kafka connect to import/export file content. We have to type of files need to process. One is crawled urls file, and the other is crawled article content. We start a standalone connect to process these two type of files. *Note that in production environment, there may only have one type of files on a certain node, we need to make corresponding changes for production environment.*
```shell
bin/connect-standalone.sh config/connect-standalone.properties config/connect-file-source-whatsnews-index.properties config/connect-file-source-whatsnews-article.properties
```

**TODO: There is a unsolved problem here. Monitored file will be increasing and it may grow to a very large size. But we haven't found a solution to mv/rm this monitored file yet, cause once we mv/rm this file, Kafka connect will stop work.**

### Consumers
There are two type of consumers in this project. One is a consumer integrated with Scapy for article content crawling, and the other one is a standalone consumer to build search engine index. There are in article_crawler and index_builder respectively.

### Groups
Group id of article_crawler is whatsnews_group_index and group id of index_builder is whatsnews_group_article.

### TODO
Variables like group ids, topics mention above will be configurable in the future.
