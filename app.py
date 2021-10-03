from flask import Flask
import datetime

from flask import Flask, jsonify
from github import Github
import requests
import logging
import json

TOKEN = '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'
# USER = 'pallets'
# REPO = 'flask'

# USER = 'temoto'
# REPO = 'vender'

USER = 'PyGithub'
REPO = 'PyGithub'


app = Flask(__name__)


@app.route('/hello', methods=["GET"])
def hello_world():  # put application's code here
    return jsonify({'hello': 'Hello World!'})

@app.route('/flask', methods=["GET"])
def github_pallets_flask_details():
    g = Github(TOKEN)
    f = g.get_user('pallets').get_repo('flask')
    return jsonify({'id': f.id, 'full_name': f.full_name})

@app.route('/flask/full_name', methods=["GET"])
def github_pallets_flask_full_name():
    g = Github(TOKEN)
    f = g.get_user('pallets').get_repo('flask')
    return f.full_name

@app.route('/flask/issues_url', methods=["GET"])
def github_pallets_flask_issues_url():
    g = Github(TOKEN)
    f = g.get_user('pallets').get_repo('flask')
    return f.get_issue()

@app.route('/flask/issues', methods=["GET"])
def github_pallets_flask_issues():
    g = Github(TOKEN)
    iss = g.get_user('pallets').get_repo('flask').get_issues()

    return jsonify({'issues_count': iss.totalCount})

@app.route('/flask/pulls', methods=["GET"])
def github_pallets_flask_pulls():
    g = Github(TOKEN)
    pulls = g.get_user('pallets').get_repo('flask').get_pulls()

    return jsonify({'pulls_count': pulls.totalCount})

@app.route('/flask/pulls_14days', methods=["GET"])
def github_pallets_flask_pulls_14days():
    g = Github(TOKEN)
    # aSince = (datetime.datetime.now() - datetime.timedelta(days=14))
    pulls = g.get_user('pallets').get_repo('flask').get_pulls()
    count = 0
    for pull in pulls:
        print(f"merged_at: {pull.merged_at}")
        # if pull.merged_at is None and (datetime.datetime.today() - pull.merged_at) > datetime.timedelta(days=14):
        if pull.merged_at is None and (datetime.datetime.today() - pull.created_at) > datetime.timedelta(days=14):
                count += 1

    return jsonify({'pulls_count': count})

@app.route('/PyGithub/pulls', methods=["GET"])
def github_PyGithub_PyGithub_pulls():
    g = Github(TOKEN)
    pulls = g.get_user('PyGithub').get_repo('PyGithub').get_pulls()

    return jsonify({'pulls_count': pulls.totalCount})

@app.route('/PyGithub/pulls_14days', methods=["GET"])
def github_PyGithub_PyGithub_pulls_14days():
    g = Github(TOKEN)
    # aSince = (datetime.datetime.now() - datetime.timedelta(days=14))
    pulls = g.get_user('PyGithub').get_repo('PyGithub').get_pulls()
    count = 0
    for pull in pulls:
        print(f"merged_at: {pull.merged_at}")
        # if pull.merged_at is None and (datetime.datetime.today() - pull.merged_at) > datetime.timedelta(days=14):
        if pull.merged_at is None and (datetime.datetime.today() - pull.created_at) > datetime.timedelta(days=14):
                count += 1

    return jsonify({'pulls_count': count})

@app.route('/details', methods=["GET"])
def get_details():
    res = requests.request('GET', f'https://api.github.com/repos/{USER}/{REPO}')
    return res.content

@app.route('/issues', methods=["GET"])
def get_issues():
    res = requests.request('GET', f'https://api.github.com/repos/{USER}/{REPO}/issues')
    return res.content

@app.route('/forks', methods=["GET"])
def get_forks():
    res = requests.request('GET', f'https://api.github.com/repos/{USER}/{REPO}/forks')
    return res.content

@app.route('/pulls', methods=["GET"])
def get_pulls():
    res = requests.request('GET', f'https://api.github.com/repos/{USER}/{REPO}/pulls')
    return res.content


if __name__ == '__main__':
    app.run()
