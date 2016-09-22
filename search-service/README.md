# Search Service

----

### Environment variables
+ MONGODB_HOSTS
+ MONGODB_DBNAME

**Note:** MONGODB_HOSTS is in following format:
```shell
mongodb://[username:password@]host1[:port1][,host2[:port2],...[,hostN[:portN]]][/[database][?options]]
```

Environment variables can be set in ~/.bashrc or similar system configuration
files on linux/unix like operating systems.
```
MONGODB_HOSTS=xxx MONGODB_DBNAME=yyy python run.py
```
is another way setting environment variables when you execute a program.
On AWS, these variables can be set in '*Environment variables*' correspondingly.

### Run Test
Run test like this, replace MONGODB_HOSTS and MONGODB_DBNAME as your own value.
```shell
MONGODB_HOSTS=mongodb://localhost:27017 MONGODB_DBNAME=whatsnews python run_test
```