from minerva.making_answer.task_tree_element import TaskTreeElement
from minerva.making_answer.enough_information import EnoughInformation
from minerva.making_answer.input_information_function.input_information_function import InputInformationFunction
from minerva.making_answer.should_task_breakdown import should_task_breakdown
from minerva.making_answer.crate_task.create_task import CreateTask
from minerva.making_answer.solve_task.crate_gpt_role import crate_gpt_role
from minerva.making_answer.solve_task.solve_task import solve_task
from minerva.making_answer.create_answer_from_bottom_elements import create_answer_from_bottom_elements

from anytree import RenderTree


class MakingAnswer:
    tree_element_list: list[TaskTreeElement] = []

    def __init__(self, openai_api_key, initial_goal, initial_information):
        self.openai_api_key = openai_api_key
        self.initial_goal = initial_goal
        self.initial_information = initial_information
        self.task_number = 0
        self.tree_element_list.append(TaskTreeElement(
            number=self.task_number, task=initial_goal, tree_depth=0, process_order=0,
            information=initial_information,))
        self.task_number += 1

    def task_process(self, processed_task_number, step_number):

        # enough_informationから、breakdownまで
        if step_number == 0:
            enough_information = EnoughInformation(openai_api_key=self.openai_api_key, goal=self.initial_goal,
                                                   tree_element_list=self.tree_element_list,
                                                   processed_task_number=processed_task_number)

            if not enough_information.response_result():
                input_information_function \
                    = InputInformationFunction(openai_api_key=self.openai_api_key, goal=self.initial_goal,
                                               tree_element_list=self.tree_element_list,
                                               processed_task_number=processed_task_number)
                input_information_function.iif_process()

            breakdown_response = should_task_breakdown(openai_api_key=self.openai_api_key, goal=self.initial_goal,
                                                       tree_element_list=self.tree_element_list,
                                                       processed_task_number=processed_task_number)
            if not breakdown_response:
                return processed_task_number, 1

            create_task = CreateTask(openai_api_key=self.openai_api_key, goal=self.initial_goal,
                                     tree_element_list=self.tree_element_list,
                                     processed_task_number=processed_task_number)
            new_task_list = create_task.create_task()
            next_processed_task_number = self.task_number
            process_order = 0
            for new_task in new_task_list:
                self.tree_element_list.append(
                    TaskTreeElement(
                        number=self.task_number,
                        task=new_task,
                        tree_depth=self.tree_element_list[processed_task_number].depth,
                        process_order=process_order,
                        parent=self.tree_element_list[processed_task_number]
                    )
                )
                self.task_number += 1
                process_order += 1
            return next_processed_task_number, 0

        if step_number == 1:
            gpt_role = crate_gpt_role(openai_api_key=self.openai_api_key,
                                      now_task_element=self.tree_element_list[processed_task_number])
            solve_task(openai_api_key=self.openai_api_key, goal=self.initial_goal,
                       tree_element_list=self.tree_element_list, processed_task_number=processed_task_number,
                       role=gpt_role)

            if processed_task_number == 0:
                return processed_task_number, 3

            task_parents: TaskTreeElement = self.tree_element_list[processed_task_number].parent
            if len(task_parents.children)+1 != self.tree_element_list[processed_task_number].process_order:
                return processed_task_number+1, 0

            return task_parents.number, 2

        if step_number == 2:
            create_answer_from_bottom_elements(openai_api_key=self.openai_api_key, goal=self.initial_goal,
                                               tree_element_list=self.tree_element_list,
                                               processed_task_number=processed_task_number)
            if processed_task_number == 0:
                return processed_task_number, 3
            task_parents: TaskTreeElement = self.tree_element_list[processed_task_number].parent
            if len(task_parents.children) + 1 != self.tree_element_list[processed_task_number].process_order:
                return processed_task_number + 1, 0
            return task_parents.number, 2

    def print_final_answer(self):
        print(f'Your goal is {self.initial_goal}')
        print(f'Answer is {self.tree_element_list[0].answer}')
