import openai
from minerva.making_answer.task_tree_element import TaskTreeElement
from minerva.token_class import Token


class EnoughInformation:

    def __init__(self, openai_api_key: str, goal: str, tree_element_list: list[TaskTreeElement],
                 processed_task_number: int):
        openai.api_key = openai_api_key
        if len(tree_element_list) == 1:
            self.current_task = "Divide into the rough steps to complete the document as defined by the user's [goal]."
            self.system_input = f'''
            Your name is Minerva, and you're an AI that helps the user do their jobs.
            <Definition>
            [goal] = {goal}
            [current task] = Divide into the rough steps to complete the document as defined by the user's [goal].
            [owned information] = {tree_element_list[0].information}
            Now you are doing [current task].
            [owned information] is information that Minerva already has.
            <Description>
            The Minerva system consists of several AIs.
            Each AI is required to fulfill a given role. 
            You are assigned the role of "Determine if [owned information] is sufficient to create [goal]".
            # output lang: jp
            '''

        else:  # 最初以外のタスクを分解する前のenough info
            self.current_task = tree_element_list[processed_task_number].task
            current_task = tree_element_list[processed_task_number]
            parents_task = current_task.parent
            children_task_list = parents_task.children
            all_information = ''
            task_and_answer_prompt = ''
            all_information += current_task.information + ', '
            all_information += parents_task.information + ', '
            for element in children_task_list:
                all_information += element.information + ', '
                if element.answer:
                    task_and_answer_prompt += f'task:{element.task}, answer:{element.answer}'
                else:
                    task_and_answer_prompt += f'task:{element.task}, answer: not yet, '

            self.system_input = f'''
            Your name is Minerva, and you're an AI that helps the user do their jobs.
            <Definition>
            [goal] = {goal}
            [completion process] = 
            [current task] = {current_task.task}
            [parent task] = {parents_task.task}
            [owned information] = {all_information}
            [same layer task and answer] = {task_and_answer_prompt}
            Now you are doing [current task].
            [owned information] is information that Minerva already has.
            [parent task] is divided into [same layer task and answer].
            <Description>
            The Minerva system consists of several AIs.
            Each AI is required to fulfill a given role. 
            You are assigned the role of "Determine if [owned information] is sufficient to perform the [current task]".
            # output lang: jp
            '''

        # ここから共通
        self.assistant_prompt = f'''
        T 
        '''

        self.user_prompt = f'''
        According to instructions, let's work this out in a step by step way to be sure we have the right answer.
        <Instruction>
        If more information is needed to [current task] in addition to [owned information], print "F".
        If enough information is available to [current task], print "T"
        <constraints>
        Be sure to output only "T" or "F".
        Do not write any other explanations, notes, or circumstances that led to the output.
        just write "T" or "F".
        '''

        self.messages = [
            {"role": "system", "content": self.system_input},
            {"role": "assistant", "content": self.assistant_prompt},
            {"role": "user", "content": self.user_prompt},
        ]

    def response_result(self):
        print(f"現在のタスク：{self.current_task}"
              f"\nこのタスクをこなすのに十分な情報があるかどうかを判断しています。"
              f"\n少々お待ちください...")
        response = openai.ChatCompletion.create(
            temperature=0,
            max_tokens=1000,
            model="gpt-3.5-turbo",
            messages=self.messages
        )
        ai_response = response['choices'][0]['message']['content']
        print(f"enough_information(row): {ai_response}")
        # トークン数のアウトプットの処理
        token = response["usage"]["total_tokens"]
        print(f'usage tokens:{token}')
        use_token = Token(token)
        use_token.output_token_information('enough_information')
        if ai_response.strip() == "T":
            print("=====Enough information=====")
            return True
        elif ai_response.strip() == "F":
            print("=====Need more information=====")
            return False
        else:
            return "Error: Invalid response"
