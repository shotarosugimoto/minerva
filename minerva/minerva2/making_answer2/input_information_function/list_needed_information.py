import openai
import re
from ..task_tree_element import TaskTreeElement
from ...token_class import Token


def list_needed_information(openai_api_key: str, goal: str, tree_element_list: list[TaskTreeElement],
                            processed_task_number: int):
    openai.api_key = openai_api_key

    if len(tree_element_list) == 1:
        system_input = f'''
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
        You are assigned the role of "List necessary info".
        # output lang: jp
        '''

        user_prompt = f'''
        According to instructions, let's work this out in a step by step way to be sure we have the right answer.
        Output only the final result.
        <note>
        # Understand the Description and your role and have clear your responsibility.
        #　keep the information you list to a minimum.
        <Instruction>
        List information needed to perform [current task].
        <constraints>
        Remove unnecessary information to perform [current task].
        Delete all information in [owned information] and [goal].
        only bullet numbers and the needed information in a clear manner.
        Do not write any other information.
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
        [owned information] = {all_information}
        [same layer task and answer] = {task_and_answer_prompt}
        Now you are doing [current task].
        [owned information] is information that Minerva already has.
        [parent task] is divided into [same layer task and answer].
        <Description>
        The Minerva system consists of several AIs.
        Each AI is required to fulfill a given role. 
        You are assigned the role of "List necessary info".
        # output lang: jp
        '''

        user_prompt = '''
        According to instructions, let's work this out in a step by step way to be sure we have the right answer.
        Output only the final result.
        <note>
        # Understand the Description and your role and have clear your responsibility.
        #　keep the information you list to a minimum.
        <Instruction>
        List information needed to perform the task [current task].
        <constraints>
        Remove unnecessary information to perform [current task].
        Delete all information in [owned information] and [goal].
        Delete information related to tasks in [same layer task and answer].
        only bullet numbers and the required information in a clear manner.
        Do not write any other information.
        # output lang: jp
        # output style: [1. ~ \n2. ~ \n...]
        '''

    # 共通
    assistant_prompt = f'''
    1. ~~
    2. ~~
    3. ~~
    4. ~~
    ...
        '''

    messages = [
        {"role": "system", "content": system_input},
        {"role": "assistant", "content": assistant_prompt},
        {"role": "user", "content": user_prompt}
    ]

    response = openai.ChatCompletion.create(
        temperature=0,
        max_tokens=1000,
        model="gpt-3.5-turbo",
        messages=messages
    )

    ai_response = response['choices'][0]['message']['content']
    print(f"needed information(row): {ai_response}")
    # トークン数のアウトプットの処理
    token = response["usage"]["total_tokens"]
    print(f'usage tokens:{token}')
    use_token = Token(token)
    use_token.output_token_information('list_needed_information')
    ai_response = ai_response.replace(" ", "")
    # Extract the needed information from the AI response
    needed_information_list = re.findall(r'^\d+\.(.+)', ai_response, re.MULTILINE)

    return needed_information_list
