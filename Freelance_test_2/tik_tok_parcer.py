from bs4 import BeautifulSoup
import requests
import time
import random
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

nik_names = ["nekoglai"
]  #, "jojohfsex

def get_html(url):
    time.sleep(random.randrange(1,4))
    session = requests.Session()
    retry = Retry(connect=3, backoff_factor=0.5)
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session.get(url).text

def parse_site(name):
    site = "https://www.tiktok.com"
    url = site + '/@' + name
    print(url)
    html = get_html(url)
    soup = BeautifulSoup(html, 'lxml')
    followers = soup.find(title="Followers").text
    print(f"followers: {followers}")
    likes = soup.find(title="Likes").text
    print(f"likes: {likes}")
    following = soup.find(title="Following").text
    print(f"following: {following}")
    videos = soup.find(text="user-post-item-list")
    print(videos)






for name in nik_names:
    parse_site(name)