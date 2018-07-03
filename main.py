import json
from github import Github
import asana
from models import Tassue
from helpers import gen_common_repr_from_github, gen_github_issues

with open('jari.creds') as ff:
    creds = json.load(ff)


g = Github(creds['github'])
gorg = g.get_organization(creds['github_org'])
ac = asana.Client.access_token(creds['asana'])
me = ac.users.me()
ws_id = None
proj_id = None
for ws in me['workspaces']:
    if ws['name'] == creds['asana_org']:
        ws_id = ws['id']

for team in ac.teams.find_by_organization(ws_id):
    if team['name'] == creds['asana_team']:
        team_id = team['id']

projects = {}
for proj in ac.projects.find_by_workspace(ws_id):
    if proj['name'] == 'Github Issues':
        proj_id = proj['id']
    projects[proj['name']] = proj['id']


if not proj_id:
    raise Exception("Can't find correct project")

if __name__ == '__main__':
    issues = []
    for ii, issue in enumerate(gen_common_repr_from_github(gorg)):
        issues.append(issue)
        if ii > 0 and ii % 10 == 0:
            break

    for issue in issues:
        if issue.github_issue_obj.pull_request:
            print("{} is a PR, skipping".format(issue))
            continue
        repo_proj = issue.github_issue_obj.repository.full_name
        if repo_proj not in projects:
            proj = ac.projects.create_in_workspace(ws_id, {'name': repo_proj, 'team': team_id})
            projects[repo_proj] = proj['id']
        print("Adding {} to Asana".format(issue))
        task_dict = {'projects': [proj_id, projects[repo_proj]]}
        task_dict.update(issue.to_asana_task_dict())
        ac.tasks.create_in_workspace(ws_id, task_dict)
