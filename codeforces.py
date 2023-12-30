import requests

def get_upcoming_contests():
    return get_contests(lambda x: x['phase'] == 'BEFORE')

def get_unfinished_contests():
    return get_contests(lambda x: x['phase'] != 'FINISHED' and x['relativeTimeSeconds'] < 360000)

def get_contests(filter):
    link = 'https://codeforces.com/api/contest.list?gym=false'
    data = requests.get(link)
    data = data.json()['result']
    res = []
    for d in data:
        if filter(d):
            res.append(d)
    res.reverse()
    return res
