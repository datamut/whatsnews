### Usage:
```python
>>> import requests
>>> requests.get('http://authapi.kc7ctmpd2z.us-west-2.elasticbeanstalk.com/token/ID123456/123456').json()
{'token': 'TK123456', 'expires_in': 86400}
>>> requests.post('http://searchapi.kc7ctmpd2z.us-west-2.elasticbeanstalk.com/search/ID123456/TK123456', data={'query': 'Guinness World Records'}).json()[0]
>>> ...
```

### Run Test
```shell
AUTH_SERVICE_URL=http://a.com:29371 SEARCH_SERVICE_URL=http://b.com:28391 python run_tests.py
```