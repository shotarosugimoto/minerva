import re

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
        print('IIFに入ります')
        print("-----list_needed_information")
        needed_information_list = list_needed_information(openai_api_key=self.openai_api_key, goal=self.goal,
                                                          tree_element_list=self.tree_element_list,
                                                          processed_task_number=self.processed_task_number)

        summarized_answer_list = []

        for i in range(len(needed_information_list)):
            print(f"needed information: "
                  f"\n{needed_information_list[i]}")
            print("-----create_questions")
            questions = create_questions(openai_api_key=self.openai_api_key, goal=self.goal,
                                         now_task_element=self.now_task_element,
                                         needed_information=needed_information_list[i])
            questions = questions.replace(" ", "") # 空欄を削除することで、不要なエラーを回避これからの経営方針を社員に伝える資料を作りたい
            print(f"questions: {questions}")
            questions_list = re.findall(r'^\d+\.(.+)', questions, re.MULTILINE)
            print("-----select_tool")
            use_tool_list = select_tool(openai_api_key=self.openai_api_key, goal=self.goal,
                                        now_task_element=self.now_task_element,
                                        needed_information=needed_information_list[i], question=questions_list)

            ask_user_list = []
            ask_gpt_list = []
            for j in range(len(questions_list)):
                print(f"questions: {questions_list[j]}")
                print(f"tools: {use_tool_list[j]}")
                if use_tool_list[j] == "U":
                    ask_user_list.append(questions_list[j])
                else:
                    ask_gpt_list.append(questions_list[j])

            # ユーザーによる回答
            if ask_user_list:
                print("-----answer_questions_by_user")
                print(f"(確認用)ask_user_list: {ask_user_list}")
                user_answers_list = answer_questions_by_user(goal=self.goal, needed_information=needed_information_list[i],
                                                             questions_list=ask_user_list)
            # gptによる回答
            if ask_gpt_list:
                print("-----create_gpt_role")
                print(f"(確認用)ask_gpt_list: {ask_gpt_list}")
                gpt_role_list = create_gpt_role(openai_api_key=self.openai_api_key, task=self.now_task_element.task,
                                                needed_information=needed_information_list[i], questions_list=ask_gpt_list)
                print("-----answer_questions_by_gpt")
                gpt_answers_list = answer_questions_by_gpt(openai_api_key=self.openai_api_key, task=self.now_task_element.task,
                                                           needed_information=needed_information_list[i],
                                                           questions_list=ask_gpt_list, role=gpt_role_list)

            # user_answers_listも、gpt_answers_listも、[Q: ~, A: ~] の形で入っている

            if ask_gpt_list:
                for j in range(len(gpt_answers_list)):
                    check_response = answer_reliable_check(openai_api_key=self.openai_api_key,
                                                           task=self.now_task_element.task,
                                                           needed_information=needed_information_list[i],
                                                           answer=gpt_answers_list[j])
                    """
                    リストじゃなくて、単体の文字列をquestionに入れて、userに入力してもらうfunctionを作らないといけない
                    その後に、gpt_answers_listのi番目の要素をnew_answerに入れ替える
                    if not check_response:
                        new_answers = answer_questions_by_user(goal=self.goal,
                                                               needed_information=needed_information_list[i],
                                                               questions=answer)
                    """
            # 必要な情報一つに対して、ユーザーとgpt両者へ質問を投げかけ、それに対する回答がuser_answers_listと、gpt_answers_list
            # これらを統合して、必要な情報に対しての一つの回答としてサマライズする

            acquired_answers = user_answers_list + gpt_answers_list
            print("-----summarize_answer")
            summarized_answer = summarize_answer(openai_api_key=self.openai_api_key,
                                                 task=self.now_task_element.task,
                                                 needed_information=needed_information_list[i],
                                                 answers=acquired_answers)
            print(f"必要な情報: {needed_information_list[i]}"
                  f"それに対する回答: {summarized_answer}")

            summarized_answer_list.append(summarized_answer)

        print("-----summarize_information")
        new_information = summarize_information(openai_api_key=self.openai_api_key, task=self.now_task_element.task,
                                                pre_information=self.now_task_element.information,
                                                needed_information_list=needed_information_list,
                                                answer_list=summarized_answer_list)
        print("IIFを抜けます")
        self.now_task_element.information = new_information
