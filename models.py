from typing import List
import json

class CommonRepr(object):
    def __init__(self):
        self.asana_id = None
        self.github_id = None
        self.on_asana = None
        self.on_github = None

    def __repr__(self):
        # return json.dumps(vars(self), indent=2)
        return str(vars(self))

class Comment(CommonRepr):
    def __init__(self):
        super(Comment, self).__init__()

class Body(CommonRepr):
    def __init__(self):
        super(Body, self).__init__()

class Title(CommonRepr):
    def __init__(self):
        super(Title, self).__init__()

# Tassue is neither task not issue, it's both
class Tassue(object):
    def __init__(self):
        self.body = Body()
        self.title = Title()
        self.comments = []
        self.asana_id = None
        self.github_issue_obj = None

    def __repr__(self):
        #return json.dumps(vars(self), indent=2)
        return str(vars(self))

    def to_asana_task_dict(self):
        return {'name': self.title.on_github,
                'notes': self.body.on_github + "\nGithub Link: " + self.github_issue_obj.url}
