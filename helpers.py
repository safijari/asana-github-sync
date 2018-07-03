from models import Tassue


def gen_github_issues(org):
    paginator = org.get_issues(filter='all')
    i = 0
    while True:
        page = paginator.get_page(i)
        i += 1
        if not page:
            break
        for issue in page:
            yield issue


def gen_common_repr_from_github(org):
    for issue in gen_github_issues(org):
        i = issue
        t = Tassue()
        t.title.on_github = i.title
        t.title.github_id = i
        t.body.on_github = i.body
        t.body.github_id = i
        t.github_issue_obj = i
        yield t
