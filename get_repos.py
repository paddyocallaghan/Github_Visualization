import json
import pandas as pd
import requests
import matplotlib.pyplot as plt
from requests.auth import HTTPBasicAuth
from http.server import BaseHTTPRequestHandler

# get credentials
credentials = json.loads(open('credentials.json').read())
authentication = HTTPBasicAuth(credentials['username'], credentials['password'])
# get data
data = requests.get('https://api.github.com/user', auth=HTTPBasicAuth('username',
                                                                      credentials['password']))
data = data.json()
# collect repo info
print("Collecting Repo information")
url = data['repos_url']
page_no = 1
repo_data = []
while True:
    # request repos_url data
    repo_response = requests.get(url, auth=HTTPBasicAuth('username', credentials['password']))
    repo_response = repo_response.json()
    # add repos_url data iteratively
    repo_data = repo_data + repo_response
    repo_fetched = len(repo_response)
    # check if page limit passed
    if repo_fetched == 30:
        page_no = page_no + 1
        url = data['repos_url'] + '?page=' + str(page_no)
    else:
        break
# add repo data to array
repo_information = []
for i, repo in enumerate(repo_data):
    data = [repo['id'], repo['name'], repo['description'], repo['created_at'], repo['updated_at'],
            repo['owner']['login'], repo['license']['name'] if repo['license'] is not None else None, repo['has_wiki'],
            repo['forks_count'], repo['open_issues_count'], repo['stargazers_count'], repo['watchers_count'],
            repo['url'], repo['commits_url'].split("{")[0]]

    repo_information.append(data)
# convert to dataframe
repo_df = pd.DataFrame(repo_information, columns=['Id', 'Name', 'Description', 'Created on', 'Updated on',
                                                  'Owner', 'License', 'Includes wiki', 'Forks count',
                                                  'Issues count', 'Stars count', 'Watchers count',
                                                  'Repo URL', 'Commits URL'])
print("Saved repo information to repo_info.csv")
# Collect commit info
print("Collecting commit info")
commit_information = []
# use Commit url found in repo data frame
for i in range(repo_df.shape[0]):
    url = repo_df.loc[i, 'Commits URL']
    page_no = 1
    # get number of commits per repo along with other commit data
    while True:
        # request commit data
        repo_response = requests.get(url, auth=HTTPBasicAuth('username', credentials['password']))
        repo_response = repo_response.json()
        # count commits per repo and add to repo dataframe
        repo_df.loc[i, 'commit number'] = len(repo_response)
        # save repo info to csv
        repo_df.to_csv('repo_info.csv', index=False)
        # add commit info to array
        for commit in repo_response:
            commit_data = [repo_df.loc[i, 'Id'], commit['sha'], commit['commit']['committer']['date'],
                           commit['commit']['message']]
            commit_information.append(commit_data)
        # check page number
        if len(repo_response) == 30:
            page_no = page_no + 1
            url = repo_df.loc[i, 'Commits URL'] + '?page=' + str(page_no)
        else:
            break

# convert to data frame
commit_df = pd.DataFrame(commit_information, columns=['Repo Id', 'Commit Id', 'Date', 'Message'])
commit_df.to_csv('commits_info.csv', index=False)
print("Saved commits information to commits_info.csv")
# label dataframes for use in graphing
dataFrame = pd.DataFrame(data=repo_df)
dataFrame2 = pd.DataFrame(data=commit_df)

# graph commits per repo
dataFrame.plot.bar(x='Name', y='commit number', title="Bar Plot of Commits per Repository")
plt.xticks(rotation=0)  # rotate x - axis labels
plt.xlabel("")
plt.ylabel("Number of Commits")
plt.legend(['Commits'])
# save graph as image for use in html file
plt.savefig('graph1.png')

# graph commits versus data
dataFrame2.plot.scatter(y='Repo Id', x='Date', c='Repo Id', cmap='rainbow')
plt.title('Scatter Plot of Commits versus Date')
plt.xlabel("Date", labelpad=1)

plt.ylabel("")
plt.xticks(rotation=90)  # rotate x - axis labels
# save graph as image for use in html file
plt.savefig('graph2.png')

# display html file on localhost
class Serv(BaseHTTPRequestHandler):

    def do_get(self):
        if self.path == '/':
            self.path = '/local_host_page.html'

        try:
            file_to_open = open(self.path[1:]).read()
            self.send_response(200)
        except:
            file_to_open = "File not found"
            self.send_response(404)
        self.end_headers()
        self.wfile.write(bytes(file_to_open, 'utf-8'))
