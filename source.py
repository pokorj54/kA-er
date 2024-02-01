

class Source:
    def __init__(self):
        self.seen_news = set()

    def get_news(self):
        all_news = self.get_news_inner()
        answer = list()
        for id in all_news:
            if id in self.seen_news:
                continue
            self.seen_news.add(id)
            answer.append(all_news[id])
        return answer
        
    def get_upcoming(self):
        return self.get_upcomming_inner()
        
