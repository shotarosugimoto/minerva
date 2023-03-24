from .create_outline import create_outline
from ..task_tree_element import TaskTreeElement


class CreateTask:

    def __init__(self, openai_api_key, goal, tree_element_list: list[TaskTreeElement],
                 processed_task_number: int):
        self.openai_api_key = openai_api_key
        self.goal = goal
        self.tree_element_list = tree_element_list
        self.processed_task_number = processed_task_number

    def create_task(self):
        while 1:
            outline_list = create_outline(openai_api_key=self.openai_api_key, goal=self.goal,
                                          tree_element_list=self.tree_element_list,
                                          processed_task_number=self.processed_task_number)

            print('\nThese are the tasks into which the current task is divided.')
            print(f'The current task: {self.tree_element_list[self.processed_task_number].task}')
            print('The divided tasks:\n')
            for i in range(len(outline_list)):
                print(f'{i+1}.: {outline_list[i]}\n')
            print('If you think this division is appropriate, please press enter, '
                  'otherwise please write what you want us to consider')
            user_input = input('Press enter or write something')
            if user_input == '':
                break
            self.tree_element_list[self.processed_task_number].user_intent = user_input

        return outline_list
