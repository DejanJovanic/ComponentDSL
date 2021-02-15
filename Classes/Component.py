
class Component:
    def __init__(self, **kwargs):
        if 'parent' in kwargs:
            self.parent = kwargs['parent']
        self.name = kwargs['name']
        if 'requirement' in kwargs:
            self.requirement = kwargs['requirement']
            if self.requirement is None:
                self.requirement = ""
        else:
            self.requirement = ""
        self.components = kwargs['components']
        self.requirement_expression = ""
        self.disabled_reason = ""
        self.enabled = True
