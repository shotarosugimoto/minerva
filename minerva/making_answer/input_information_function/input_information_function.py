from .list_needed_information import list_needed_information
from .select_tool import select_tool
from .create_questions import create_questions
from .answer_questions_by_user import answer_questions_by_user
from .answer_questions_by_gpt import answer_questions_by_gpt
from .summarize_answer import summarize_answer
from .summarize_information import summarize_information
from .answer_reliable_check import answer_reliable_check
from .create_gpt_role import create_gpt_role
from ..task_tree_element import TaskTreeElement


class InputInformationFunction:

    def __init__(self, openai_api_key: str, goal: str, tree_element_list: list[TaskTreeElement],
                 processed_task_number: int):
        self.openai_api_key = openai_api_key
        self.goal = goal
        self.tree_element_list: list[TaskTreeElement] = tree_element_list
        self.processed_task_number = processed_task_number
        self.now_task_element = tree_element_list[processed_task_number]

    def iif_process(self):
        needed_information_list = list_needed_information(openai_api_key=self.openai_api_key, goal=self.goal,
                                                          tree_element_list=self.tree_element_list,
                                                          processed_task_number=self.processed_task_number)

        summarized_answer_list = []
        for needed_information in needed_information_list:
            use_tool = select_tool(openai_api_key=self.openai_api_key, goal=self.goal,
                                   now_task_element=self.now_task_element, needed_information=needed_information)
            questions = create_questions(openai_api_key=self.openai_api_key, now_task_element=self.now_task_element,
                                         needed_information=needed_information, tool=use_tool)
            answers: str
            if use_tool == 'user_input':
                answers = answer_questions_by_user(goal=self.goal, needed_information=needed_information,
                                                   questions=questions)
            else:
                gpt_role = create_gpt_role(openai_api_key=self.openai_api_key, task=self.now_task_element.task,
                                           needed_information=needed_information, questions=questions)
                answers = answer_questions_by_gpt(openai_api_key=self.openai_api_key, task=self.now_task_element.task,
                                                  needed_information=needed_information, questions=questions,
                                                  role=gpt_role)
            summarized_answer = summarize_answer(openai_api_key=self.openai_api_key,
                                                 needed_information=needed_information, questions=questions,
                                                 answers=answers,)

            if use_tool != 'user_input':
                check_response = answer_reliable_check(openai_api_key=self.openai_api_key,
                                                       task=self.now_task_element.task,
                                                       needed_information=needed_information, answer=summarized_answer)
                if check_response == '1':
                    new_answers = answer_questions_by_user(goal=self.goal, needed_information=needed_information,
                                                           questions=questions)
                    summarized_answer = summarize_answer(openai_api_key=self.openai_api_key,
                                                         needed_information=needed_information, questions=questions,
                                                         answers=new_answers, )

            summarized_answer_list.append(summarized_answer)

        new_information = summarize_information(openai_api_key=self.openai_api_key, task=self.now_task_element.task,
                                                pre_information=self.now_task_element.information,
                                                needed_information_list=needed_information_list,
                                                answer_list=summarized_answer_list)
        self.now_task_element.information = new_information
