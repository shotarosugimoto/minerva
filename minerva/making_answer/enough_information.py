import openai
from minerva.making_answer.task_tree_element import TaskTreeElement
from minerva.token_class import Token


class EnoughInformation:

    def __init__(self, openai_api_key: str, goal: str, tree_element_list: list[TaskTreeElement],
                 processed_task_number: int):
        openai.api_key = openai_api_key
        if len(tree_element_list) == 1:  # 一番最初のアウトラインを作るところ
            print("最初のアウトラインを作るところ、")

            self.system_input = f'''
Your name is Minerva, and you're an AI that helps the user do their jobs.
[goal] = {goal}
[current task] = create the best output outline to achieve [goal]
[owned information] = {tree_element_list[0].information}
Keep in mind [goal].
Now you are doing [current task].
            '''
            print(f"system_input:{self.system_input}")

        else:  # 最初以外のタスクを分解する前のenough info
            current_task = tree_element_list[processed_task_number]
            parents_task = current_task.parent
            children_task_list = parents_task.children
            all_information = ''
            task_and_answer_prompt = ''
            all_information += current_task.information + '\n'
            all_information += parents_task.information + '\n'
            processed_order = current_task.path
            for element in children_task_list:
                all_information += element.information + '\n'
                if element.process_order < processed_order:
                    task_and_answer_prompt += f'task:{element.task}, answer:{element.answer}'
                if element.process_order > processed_order:
                    task_and_answer_prompt += f'task:{element.task}, answer: not yet'

            self.system_input = f'''
Your name is Minerva, and you're an AI that helps the user do their jobs.
[goal] = {goal}
[current task] = {current_task}
[ownd information] = {all_information}
Keep in mind [goal].
Now you are doing [current task].
{task_and_answer_prompt} are tasks and their answers on the same layer as [current task]
, which are decomposed tasks to solve {parents_task}.
            '''

        # ここから共通
        self.assistant_prompt = f'''
        1Q
        '''

        self.user_prompt = f'''
If more information is needed to [current task] in addition to [ownd information], print "1Q".
If enough information is available to [current task], sprint "1"
Be sure to output only "iQ" or "1".
Do not write any other explanations, notes, or circumstances that led to the output.
just write  1"iQ" or "1".
        '''

        self.messages = [
            {"role": "system", "content": self.system_input},
            {"role": "assistant", "content": self.assistant_prompt},
            {"role": "user", "content": self.user_prompt},
        ]

    def response_result(self):
        response = openai.ChatCompletion.create(
            temperature=1,
            max_tokens=1000,
            model="gpt-3.5-turbo",
            messages=self.messages
        )
        # 確認用
        print(f"system_input:{self.system_input}")
        ai_response = response['choices'][0]['message']['content']
        # トークン数のアウトプットの処理
        token = response["usage"]["total_tokens"]
        print(f'usage tokens:{token}')
        use_token = Token(token)
        use_token.output_token_information('enough_information')
        if ai_response.strip() == "1":
            print("enough information")
            return True
        elif ai_response.strip() == "1Q":
            print("need more information")
            return False
        else:
            return "Error: Invalid response"
