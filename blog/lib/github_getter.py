from requests import get
import datetime


def get_commits():
    url = 'https://api.github.com/repos/biryukov-m/c-media/commits'
    try:
        r = get(url)
        dic = r.json()
        output = []
        for d in dic:
            date = d['commit']['committer']['date']
            date = datetime.datetime.strptime(date, "%Y-%m-%dT%H:%M:%SZ")
            message = d['commit']['message']
            html_url = d['html_url']
            if len(message) > 180:
                output.append([date, message, html_url])
        return output
    except:
        return None