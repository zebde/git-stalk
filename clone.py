"""Manages scraping from git repos."""
from __future__ import print_function

import json
import os

import requests
from git import Repo

OBJS = []
API_URL = "https://api.github.com/users/"


def _SubDirPath(d):
    return filter(os.path.isdir, [os.path.join(d, f) for f in os.listdir(d)])


def _getOnline(target, output):
    cnt = 1
    while cnt > 0:
        url = API_URL + target + "/repos?page=" + str(cnt) + "&per_page=100"
        js_data = json.loads(requests.get(url).content)
        if len(js_data) == 0:
            print("No more repositories")
            cnt = -10
        else:
            print('count: ' + str(cnt) + ' : ' + str(len(js_data)))
            if "message" in js_data and "limit exceeded" in js_data["message"]:
                print("Rate limit reached")
                cnt = -10
            else:
                for y in js_data:
                    git_url = y["clone_url"]
                    out_name = os.path.join(output, y["name"])
                    _getRepo(out_name, git_url)

        cnt = cnt+1


def _getRepo(repo_name, git_url):
    if os.path.isdir(repo_name):
        repo = Repo(repo_name)
        repo.remotes.origin.pull()
        log = repo.git.log('--pretty=%ae|%an').splitlines()
        for x in log:
            y = x.split('|')
            d = {
                'user': y[1],
                'email': y[0]
            }
            OBJS.append(d)
    else:
        print(git_url)
        Repo.clone_from(git_url, repo_name)


def scrape_git(target, output, status):
    """Scrape git repositories for identities."""
    if status is "offline":
        nn = _SubDirPath(output)
        for name in nn:
            _getRepo(name, "url")
    elif status is "online":
        _getOnline(target, output)
    sets = [dict(y) for y in set(tuple(x.items()) for x in OBJS)]
    print("[+] Scraping identified " + str(len(sets)) + " identities")
    return json.dumps(sets, indent=4)


if __name__ == "__main__":
    print(scrape_git("zebde", "/tmp/repos", "offline"))
