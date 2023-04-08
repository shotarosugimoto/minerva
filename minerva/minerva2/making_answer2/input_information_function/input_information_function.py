import re

from .list_needed_information import list_needed_information
from .select_tool import select_tool
from .create_questions import create_questions
from .answer_questions_by_user import answer_questions_by_user
from .answer_questions_by_gpt import answer_questions_by_gpt
from .summarize_answer import summarize_answer
from .summarize_information import summarize_information
from .summarize_questions import summarize_questions
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
        print('IIFに入ります')
        print("-----list_needed_information")
        needed_information_list = list_needed_information(openai_api_key=self.openai_api_key, goal=self.goal,
                                                          tree_element_list=self.tree_element_list,
                                                          processed_task_number=self.processed_task_number)
        print("-----create_questions")
        question = create_questions(openai_api_key=self.openai_api_key, goal=self.goal,
                                    now_task_element=self.now_task_element,
                                    tree_element_list=self.tree_element_list,
                                    processed_task_number=self.processed_task_number,
                                    needed_information_list=needed_information_list)
        question = question.replace(" ", "")
        questions_list = re.findall(r'^\d+\.(.+)', question, re.MULTILINE)
        print(f"questions_list: {questions_list}")

        print("-----select_tool")
        use_tool_list = select_tool(openai_api_key=self.openai_api_key, goal=self.goal,
                                    now_task_element=self.now_task_element,
                                    needed_information=needed_information_list, questions=questions_list)
        ask_user_list = []
        ask_gpt_list = []
        for j in range(len(questions_list)):
            if use_tool_list[j] == "U":
                ask_user_list.append(questions_list[j])
            else:
                ask_gpt_list.append(questions_list[j])
        summarized_answer_list = []
        # ユーザーによる回答
        user_answers_list = []
        if ask_user_list:
            print("-----answer_questions_by_user")
            print(f"(確認用)ask_user_list: {ask_user_list}")
            user_answers_list = answer_questions_by_user(goal=self.goal,
                                                         needed_information=needed_information_list,
                                                         questions_list=ask_user_list)
        # gptによる回答
        gpt_answers_list = []
        if ask_gpt_list:
            print(f"(確認用)ask_gpt_list: {ask_gpt_list}")
            """
            print("-----create_gpt_role")
            gpt_role_list = create_gpt_role(openai_api_key=self.openai_api_key, task=self.now_task_element.task,
                                            needed_information=needed_information_list,
                                            questions_list=ask_gpt_list)
            """
            print("-----answer_questions_by_gpt")
            gpt_answers_list = answer_questions_by_gpt(openai_api_key=self.openai_api_key,
                                                       now_task_element=self.now_task_element,
                                                       task=self.now_task_element.task,
                                                       needed_information=needed_information_list,
                                                       questions_list=ask_gpt_list)
            # 必要な情報一つに対して、ユーザーとgpt両者へ質問を投げかけ、それに対する回答がuser_answers_listと、gpt_answers_list
            # user_answers_listも、gpt_answers_listも、[Q: ~, A: ~] の形で入っている
            # これらを統合して、必要な情報に対しての一つの回答としてサマライズする
        acquired_answers = [user_answers_list, gpt_answers_list]
        """
        print("-----summarize_answer")
        summarized_answer = summarize_answer(openai_api_key=self.openai_api_key,
                                             task=self.now_task_element.task,
                                             needed_information=needed_information_list,
                                             answers=acquired_answers)
        print(f"必要な情報: {needed_information_list}\n"
              f"それに対する回答: {summarized_answer}")
            # この時点で獲得したinformationを格納しないと同じ質問がくる超うざい
        self.now_task_element.information += summarized_answer
        summarized_answer_list.append(summarized_answer)
        """

        print("-----summarize_information")
        new_information = summarize_information(openai_api_key=self.openai_api_key, task=self.now_task_element.task,
                                                pre_information=self.now_task_element.information,
                                                needed_information_list=needed_information_list,
                                                answer_list=acquired_answers)
        print("IIFを抜けます")
        self.now_task_element.information = new_information

        """
        if ask_gpt_list:
            for j in range(len(gpt_answers_list)):
                check_response = answer_reliable_check(openai_api_key=self.openai_api_key,
                                                       task=self.now_task_element.task,
                                                       needed_information=needed_information_list[i],
                                                       answer=gpt_answers_list[j])
                リストじゃなくて、単体の文字列をquestionに入れて、userに入力してもらうfunctionを作らないといけない
                その後に、gpt_answers_listのi番目の要素をnew_answerに入れ替える
                if not check_response:
                    new_answers = answer_questions_by_user(goal=self.goal,
                                                           needed_information=needed_information_list[i],
                                                           questions=answer)
                """

        """
        # 質問の数がえらいことになるからやめた
        # need infoごとに作った質問をquestionsに格納して、summarize_questionsに渡す
        print(f"question: {question}")
            questions.append(question)
            
        print("-----summarize_questions")
        questions_list = []
        # 同じ質問がくることを回避するために、先に質問を作って、それらをまとめてから回答を求める
        summarized_questions = summarize_questions(openai_api_key=self.openai_api_key,
                                                   task=self.now_task_element.task,
                                                   needed_information=needed_information_list,
                                                   questions=questions,
                                                   tree_element_list=self.tree_element_list,
                                                   processed_task_number=self.processed_task_number
                                                   )
        summarized_questions = summarized_questions.replace(" ", "")
        questions_list = re.findall(r'^\d+\.(.+)', summarized_questions, re.MULTILINE)
        print(f"questions: {questions_list}")
        """
