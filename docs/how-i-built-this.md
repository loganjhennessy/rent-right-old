# Step 1: Getting the data

Step 1 is to get the data.

## Spin up an EC2 instance for scraping

This will host two things:

- A simple python web scraper
- A Mongo database

The web scraper will just grab raw documents and put them in MongoDB for
later retrieval and processing.

I chose a t2.micro instance with 30 GBs of storage for now. If I need
to expand later that shouldn't be too hard.

I did not create an IAM account specifically for this machine, I figure
since this is a personal project, I can just use my master account.

I *did* create a new key pair and downloaded that to my .ssh foler

## Proxy Service

After some difficulty trying to access [Storm Proxies](
http://stormproxies.com/), I finally settled on [Proxy Rotator](
https://www.proxyrotator.com/) for my proxy needs.

Proxy Rotator allows you to test out their proxies before actually
paying for their service, to do this. They even have an API which
allows for dynamic querying for a random proxy. Their site did not
include example Python code for using this so I setup a little bit of
Python code of my own to query [whoishostingthis](
https://www.whoishostingthis.com/tools/user-agent), and verify I was
seeing random IPs. Here's how:

**Imports**
```python
import requests

from bs4 import BeautifulSoup
from fake_useragent import UserAgent
```

fake_useragent is used to provide a random user agent for every request.
I wasn't sure if I needed this at first, but found that response times
were cut from tens of seconds to almost instant when I *did* use a
random user agent. I guess whoishostingthis optimizes for browsers.

**Setup**
```python
proxyapi = 'http://api.proxyrotator.com/' # Proxy Rotator's API
params = {
    'apiKey' = '<YOUR API KEY>'
    'get': 'true', # Only return proxies that allow get requests
    'userAgent': 'true', # Only return proxies allowing for User-Agent header
    'country': 'US'
}
```

**Get the proxy**
```python
resp = requests.get(proxyapi, params=params)
proxy = resp.json()['proxy']
print('Proxy from API: ' + proxy)
```

**Using the proxy**
```python
proxies = {
    'http': proxy,
    'https': proxy
}
ua = UserAgent()
headers = {
    'User-Agent': ua.random
}
whoishostingthis = 'https://www.whoishostingthis.com/tools/user-agent'
resp = requests.get(whoishostingthis, proxies=proxies, headers=headers)
```

**Parsing the response**
```python
soup = BeautifulSoup(resp.content, 'html.parser')
ipaddress = soup.select('.info-box.ip')[0].span.text
useragent = soup.select('.info-box.user-agent')[0].text
print(ipaddress)
print(useragent)
```

## Rotating proxy endpoint

Great, proxy verified. Now let's try to use Proxy Rotator's rotating
proxy endpoint. I whitelisted my IP, but I still have some time 


