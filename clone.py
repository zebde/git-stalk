"""Manages scraping from git repos."""
from __future__ import print_function

import argparse
import json
import os

import requests
from git import Repo

OBJS = []
API_URL = "https://api.github.com/users/"


def _parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--target',
                        help='Targeted GitHub user/org')
    parser.add_argument('--directory', default=os.getcwd(),
                        help='Target directory')
    parser.add_argument('--connect', default="offline",
                        help='Sets the connection, offline/online.')
    opts = parser.parse_args()
    if opts.target:
        opts.connect = "online"
    if not (opts.target or opts.directory):
        parser.error("You have to specify either a target or a directory!")
    return opts


def _SubDirPath(d):
    return filter(os.path.isdir, [os.path.join(d, f) for f in os.listdir(d)])


def _getOnline(target, output):
    cnt = 1
    print("[+] Going online")
    while cnt > 0:
        url = API_URL + target + "/repos?page=" + str(cnt) + "&per_page=100"
        js_data = json.loads(requests.get(url).content)
        if len(js_data) == 0:
            print("No more repositories")
            cnt = -10
        else:
            if "message" in js_data and "limit exceeded" in js_data["message"]:
                print("Rate limit reached")
                cnt = -10
            else:
                for y in js_data:
                    git_url = y["clone_url"]
                    out_name = os.path.join(output, y["name"])
                    _getRepo(out_name, git_url, "online")

        cnt = cnt+1


def _getRepo(repo_name, git_url, connect):
    if os.path.isdir(repo_name):
        print("[+] %s already exists" % repo_name)
        repo = Repo(repo_name)
        if connect is "online":
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


def scrape_git(target, directory, connect):
    """Scrape git repositories for identities."""
    if connect is "offline":
        nn = _SubDirPath(directory)
        for name in nn:
            _getRepo(name, "url", connect)
    elif connect is "online":
        _getOnline(target, directory)
    sets = [dict(y) for y in set(tuple(x.items()) for x in OBJS)]
    print("[+] Scraping identified " + str(len(sets)) + " identities")
    return json.dumps(sets, indent=4)


def _main():
    opts = _parse_args()
    print(scrape_git(opts.target, opts.directory, opts.connect))


if __name__ == "__main__":
    _main()
