import requests
from bs4 import BeautifulSoup
import ssl
from urllib.request import urlopen
import re

class Frontier:
    def __init__(self):
        self.visited = set() #checks if url is here
        self.queue = [] #removes old url and replaces with a new one

    def add_url(self, url): #appends url to queue
        if url not in self.visited and url not in self.queue:
            self.queue.append(url)

    def next_url(self):
        url = self.queue.pop(0) #removes first url from queue
        self.visited.add(url) #adds first url in set
        print("current queue", url)
        return url #returns url

    def done(self): #checks of queue is empty
        return len(self.queue) == 0

def retrieve_html(url):
    try:
        response = requests.get(url) 
        response.raise_for_status()
        print(response.text)
        return response.text
    except requests.RequestException as e:
        print(f"Error retrieving the HTML from {url}: {e}")
        return None

def store_page(url, html):
   pass

def target_page(html):
    if html is None:
        return False
    try:
        targetPage = "Permanent Faculty"
        bs = BeautifulSoup(html, 'html.parser')

        regex = re.compile('^navbar')
        nav_links = bs.find_all(_class=regex)
        #nav_links = bs.find_all(_class="nav-links")

        for link in nav_links:
            if link.get_text().strip() == "Permanent Faculty":
                for sibling in link.find_next_siblings('li'):
                    if sibling.get_text().strip() == targetPage:
                        return True

        return False

    except Exception as e:
        print(f"Error checking target page: {e}")
        return False

def parse(html):
    if html is None:
        return []
    try:
        bs = BeautifulSoup(html, 'html.parser')
        regex = re.compile('^navbar')
        links = [link.get('href') for link in bs.find_all('nav', _class=regex, href=True)]
        return links
    except Exception as e:
        print(f"Error parsing HTML: {e}")
        return []

def crawler_thread(frontier):
    while not frontier.done():

        url = frontier.next_url()
        html = retrieve_html(url)
        
        if target_page(html):
            frontier.queue.clear()
        else:
            print("still found nothing")
            for link in parse(html):
                print("for each html", link)
                frontier.add_url(link)

if __name__ == '__main__':
    # frontier = Frontier()
    # frontier.add_url('https://www.cpp.edu/sci/computer-science/')  # Start URL
    # crawler_thread(frontier)
    url = "https://www.cpp.edu/sci/computer-science/"
    retrieve_html(url)

