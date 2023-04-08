import openai
from ..task_tree_element import TaskTreeElement
import re

from ...token_class import Token


def create_outline(openai_api_key: str, goal: str, tree_element_list: list[TaskTreeElement],
                   processed_task_number: int, selected_tasks: list[str]):
    openai.api_key = openai_api_key
    loop_num = 0
    while True:
        if len(tree_element_list) == 1:
            system_input = f'''
            Your name is Minerva, and you're an AI that helps the user do their jobs.
            <Definition>
            [goal] = {goal}
            [current task] = Develop process for document completion
            [owned information] = {tree_element_list[0].information}
            [user intent] = {tree_element_list[0].user_intent}
            [selected tasks] = {selected_tasks}
            Now you are doing [current task].
            [owned information] is information that Minerva already has.
            [user intent] is user\'s intent, so keep this request in mind when answering.
            Include tasks from [selected tasks], because the user has already deemed them necessary.
            <Prerequisite>
            The Minerva system consists of several AIs.
            Each AI is required to fulfill a given role.    
            You are assigned the role of "Develop process for document completion".
            # output lang: jp
            '''
            user_prompt = f'''
            let's work this out in a step by step way to be sure we have the right answer.
            Output only the final result.
            <note>
            # Understand the Description and your role and have clear your responsibility.
            # Clearly understand [goal].
            <Instruction>
            List the steps required to create the document as determined by [goal],
            and put these in the proper order, assuming you are going to do the tasks in order.
            <constraints>
            Only output the final result.
            # output lang: jp
            # output style: [1. ~ \n2. ~ \n...]
            '''

        else:
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

            system_input = f'''
            Your name is Minerva, and you're an AI that helps the user do their jobs.
            <Definition>
            [goal] = {goal}
            [current task] = {current_task.task}
            [parent task] = {parents_task.task}
            [owned information] = {tree_element_list[processed_task_number].information}
            [user intent] = {parents_task.user_intent}
            [selected tasks] = {selected_tasks}
            [task_and_answer_prompt] = {task_and_answer_prompt}
            Now you are doing [current task].
            [parent task] is divided into [same layer task and answer].
            [owned information] is information that Minerva already has.
            [user intent] is user\'s intent, so keep this request in mind when answering.
            Include tasks from [selected tasks], because the user has already deemed them necessary.
            [parent task] is divided into [same layer task and answer].
            <Prerequisite>
            The Minerva system consists of several AIs.
            Each AI is required to fulfill a given role.    
            You are assigned the role of "Divide large tasks into small tasks".
            # output lang: jp
            '''
            user_prompt = f'''
            According to instructions, let's work this out in a step by step way to be sure we have the right answer.
            Output only the final result.
            <note>
            # Understand the Description and your role and have clear your responsibility
            # Clearly understand [goal] & [current task]
            <Instruction>
            List the steps required to do [current task]
            <constraints>
            Never include unnecessary steps for [current task] from these steps.
            put lists in the proper order, assuming you are going to do the tasks in order.
            Only output the final result.
            # output lang: jp
            # output style: [1. ~ \n2. ~ \n...]
            '''

        assistant_prompt = f'''
        1. ~
        2. ~
        3. ~
        ...
        '''

        print(f"(確認用)system_input: {system_input}")
        messages = [
            {"role": "system", "content": system_input},
            {"role": "assistant", "content": assistant_prompt},
            {"role": "user", "content": user_prompt}
        ]

        # Call the ChatCompletion API
        response = openai.ChatCompletion.create(
            temperature=0,
            max_tokens=1000,
            model="gpt-3.5-turbo",
            messages=messages
        )

        ai_response = response['choices'][0]['message']['content']
        print(f"（確認用）divided tasks: {ai_response}")
        # トークン数のアウトプットの処理
        token = response["usage"]["total_tokens"]
        # print(f'usage tokens:{token}')
        use_token = Token(token)
        use_token.output_token_information('create_outline')
        ai_response = ai_response.replace(" ", "") # 不要なエラーをなくすために空欄を削除
        output = re.findall(r'^\d+\.(.+)', ai_response, re.MULTILINE)
        loop_num +=1
        if output:
            return output
        elif loop_num ==3:
            print("申し訳ございません。未熟者のため、タスクを上手くこなすことができませんでした。"
                  "\n最初からやり直していただくことになってしまいました。")
            break
        else:
            print("ごめんなさい。タスクを分解するのを失敗してしまいました。"
                  "\n再度、タスクを分解しますので、少々お待ちください...")
            continue
