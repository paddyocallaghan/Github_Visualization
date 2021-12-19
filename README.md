# Github_api_visualization

## Setup
Download project from github and cd into project folder.

Enter the command below in a terminal with the project folder opened:
```
./setup.sh

```
This will  install pandas requests and matplotlib.

Add username and token to:
``
credentials.json 
``
## To Run
Enter the command below in the terminal: 

```
python .\get_repos.py
```
This will save the following:

- repo information in repo_info.csv
- commit information in commits_info.csv
- image 1 in graph1.png
- image 2 in graph2.png

## To see results
Start Server with the command below:
``
 python -m http.server   
``
Navigate to the link below on web browser:
``
http://localhost:8000/local_host_page.html
``




