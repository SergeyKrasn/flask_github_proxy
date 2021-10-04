from flask import Flask, jsonify
from github import Github, PullRequest
import requests
import logging
import os
import sys
import datetime

TOKEN = os.environ.get('TOKEN')

# REPO = 'pallets/flask'
# REPO = 'temoto/vender'
# REPO = 'PyGithub/PyGithub'
REPO = os.environ.get('REPO')

# print(sys.argv)
app = Flask(__name__)

def get_repo(token, repo):
    github = Github(token)
    return github.get_repo(repo)

@app.route('/details')
def get_details():
    # res = requests.request('GET', f'https://api.github.com/repos/{REPO}')
    # return res.content
    r = get_repo(TOKEN, REPO)
    return r.raw_data

@app.route('/issues')
def get_issues():
    res = requests.get(f'https://api.github.com/repos/{REPO}/issues')
    return res.content
    # r = get_repo(TOKEN, REPO)
    # issues = r.get_issues()
    # res = []
    # for iss in issues:
    #     res.append(iss.raw_data)
    # return jsonify(res)

@app.route('/forks')
def get_forks():
    res = requests.request('GET', f'https://api.github.com/repos/{REPO}/forks')
    return res.content


@app.route('/pulls')
def get_pulls():
    res = requests.request('GET', f'https://api.github.com/repos/{REPO}/pulls')
    return res.content

def filter14days(pull: PullRequest) -> bool:
    return (
            pull.merged_at is None and
            (datetime.datetime.today() - pull.created_at) > datetime.timedelta(days=14)
    )

@app.route('/pulls/14days')
def pulls_14days():
    r = get_repo(TOKEN, REPO)
    pulls = r.get_pulls()
    res = [p.raw_data for p in pulls if filter14days(p)]

    return jsonify(res)


if __name__ == '__main__':
    print('start app.py')

    args = sys.argv[1:]
    if len(args) < 2:
        print("""\
        USAGE: python app.py ????? 
        """)
        sys.exit(1)

    # app.config.update({
    #     'REPO': REPO,
    #     'TOKEN': TOKEN
    # })
    app.run()
