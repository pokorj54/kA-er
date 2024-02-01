import feedparser
import requests
import source

class Euler(source.Source):
    def __init__(self):
        super().__init__()

    def get_news_inner(self):
        d = feedparser.parse('https://projecteuler.net/rss2_euler.xml')
        answer = {i["guid"]:f'{i["title"]}({i["link"]}): {i["description"]}' for i in d["entries"]}
        return answer
    def get_upcomming_inner(self):
        url = 'https://projecteuler.net/minimal=new'
        html = requests.get(url).text.split('\r\n')
        items = list(map(lambda x: x.split('##'),html))
        response = {k:(int(v), f'Problem {k}') for k,v in items[:-1]}
        return response

if __name__ == "__main__":
    euler = Euler()
    print(euler.get_upcomming_inner())
    print(euler.get_news_inner())
