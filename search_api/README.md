### Usage:
```python
>>> import requests
>>> requests.get('http://li1438-193.members.linode.com:7501/token/ID123456/123456').json()
{'token': 'TK123456', 'expires_in': 86400}
>>> requests.post('http://li1438-193.members.linode.com:7701/search/ID123456/TK123456', data={'query': 'Guinness World Records'}).json()[0]
>>> ....
```
