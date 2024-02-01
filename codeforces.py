import requests
import time
import source

class Codeforces(source.Source):
    def __init__(self):
        super().__init__()
    def get_contests(self, filter):
        link = 'https://codeforces.com/api/contest.list?gym=false'
        data = requests.get(link)
        data = data.json()['result']
        res = []
        for d in data:
            if filter(d):
                res.append(d)
        res.reverse()
        return res
    
    def get_upcomming_inner(self):
        contests =  self.get_contests(lambda x: x['phase'] == 'BEFORE')
        return { c['id']:(int(c['startTimeSeconds']), c['name']) for c in contests}

    def get_news_inner(self):
        contests = self.get_contests(lambda x: x['phase'] != 'FINISHED' and x['relativeTimeSeconds'] < 360000)
        res = dict()
        for c in contests:
            if c['phase'] == "BEFORE":
                t = time.time()
                at = time.strftime('%Y-%m-%d %H:%M %Z', time.localtime(c['startTimeSeconds']))
                rh = int((c['startTimeSeconds']-t)// 3600)
                rm = int((c['startTimeSeconds']-t)% 3600 // 60)
                dh = int(c['durationSeconds']// 3600)
                dm = int(c['durationSeconds']% 3600 // 60)
                msg = f"- {c['name']} in {rh}h{str(rm).zfill(2)}m, at {at}, duration {dh}:{str(dm).zfill(2)}\n"
            else:
                msg = f"{c['name']} phase changed to {c['phase']}"
            res[(c['id'],c['phase'])] = msg
        return res

if __name__ == "__main__":
    cf = Codeforces()
    print(cf.get_upcomming_inner())
    print(cf.get_news_inner())
