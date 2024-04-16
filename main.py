import os
from github import Github
from datetime import datetime, timedelta
import requests
now = datetime.now()
try:
    g = Github(os.environ["GITHUB_TOKEN"])
    repo = g.get_repo(os.environ['REPO_NAME'])
    pulls = repo.get_pulls(state='open')
    print("hello from docker")
    print(f"{repo}")
    msg = {
        # 1 stale PR
        "stale_label" : 'This PR is stale because it has been open 15 days with no activity. Remove stale label or comment/update PR otherwise this will be closed in next 2 days.' ,
        "stale_days" : 1,
        "stale_close_days" : 1,
        # 2.close staled PR if 2 days of no activity
        "staled_PR_closing" : 'This PR was closed because it has been stalled for 2 days with no activity.' ,
        # 3.Check if the pull request targets the master branch directly
        }
    for pull in pulls:
        time_diff = now - pull.updated_at
    # 1. Check if the time difference is greater than the stale_days
        if time_diff > timedelta(days=msg.get("stale_days")):
            print(f"Pull request: {pull.number} is stale!")
            pull.create_issue_comment(msg.get("stale_label"))
            pull.add_to_labels('Stale')

except Exception as e:
    print(f"Failed to run the job. exception: {str(e)}")  
