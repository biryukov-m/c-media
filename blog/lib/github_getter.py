from requests import get
import datetime


def get_commits():
    url = 'https://api.github.com/repos/biryukov-m/django-media/commits'
    try:
        r = get(url)
        dic = r.json()
        output = {}
        for d in dic[:10]:
            date = d['commit']['committer']['date']
            date = datetime.datetime.strptime(date, "%Y-%m-%dT%H:%M:%SZ")
            message = d['commit']['message']
            output[date] = ' '.join(message.split(' '))
        return output
    except:
        return None