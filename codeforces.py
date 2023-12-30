import requests

def get_upcoming_contests():
    link = 'https://codeforces.com/api/contest.list?gym=false'
    data = requests.get(link)
    data = data.json()['result']
    i = 0
    res = []
    while data[i]['phase'] == 'BEFORE':
        res.append(data[i])
        i += 1 
    res.reverse()
    return res
