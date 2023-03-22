from anytree import NodeMixin


class TaskTreeElement(NodeMixin):

    def __init__(self, number: int, task: str, tree_depth: int, process_order: int, information='',
                 answer='', parent=None, children=None):
        self.number = number
        self.task = task
        self.tree_depth = tree_depth
        self.process_order = process_order
        self.information = information
        self.answer = answer
        self.parent = parent
        if children:
            self.children = children
