from task_tree_element import TaskTreeElement
from anytree import RenderTree


class MakingAnswer:
    tree_initial: list[TaskTreeElement]

    def __init__(self, openai_api_key, initial_goal, initial_information):
        self.openai_api_key = openai_api_key
        self.initial_goal = initial_goal
        self.initial_information = initial_information
        self.task_number = 0
        self.tree_initial[self.task_number] = TaskTreeElement(number=self.task_number, task=initial_goal, tree_depth=0,
                                                              process_order=0, information=initial_information,
                                                              answer='')

    def task_process(self):
        a = TaskTreeElement(number=self.task_number+1, task='ss', tree_depth=0, process_order=0,
                            information='ssss', answer='', parent=self.tree_initial)
        for pre, _, node in RenderTree(self.tree_initial):
            treestr = u"%s%s" % (pre, node.number)
            print(treestr.ljust(8),)
        print(self.tree_initial.children[0].number)


aaa = MakingAnswer(openai_api_key='ss', initial_goal='ss', initial_information='sss')
aaa.task_process()
