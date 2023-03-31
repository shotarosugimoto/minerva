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
    [goal] = {goal}
    [current task] = create the best output outline to achieve [goal]
    [owned information] = {tree_element_list[0].information}
    Keep in mind [goal]
    Now you are doing the task that [current task]
    # output lang: jp
            '''

    else:
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

        system_input = f'''
    Your name is Minerva, and you're an AI that helps the user do their jobs.
    [goal] = {goal}
    [current task] = {current_task}
    [owned information] = {all_information}
    Keep in mind [goal]
    Now you are doing the task that [current task]
    {task_and_answer_prompt} are tasks and their answers on the same layer as [current task]
    , which are decomposed tasks to solve {parents_task}
    # output lang: jp
            '''

    # 共通
    assistant_prompt = f'''
    1. ~~
    2. ~~
    3. ~~
    4. ~~
    ...
        '''

    user_prompt = f'''
    List the information needed to perform the task [current task] in addition to [ownd information]
    Also, output only bullet numbers and the information you want in a straightforward manner.
    Do not write any other information.
    # output lang: jp
    Answer in the form of [1. ~ \n2. ~ \n...]
        '''
    print(f"system_input:{system_input}")

    messages = [
        {"role": "system", "content": system_input},
        {"role": "assistant", "content": assistant_prompt},
        {"role": "user", "content": user_prompt}
    ]

    response = openai.ChatCompletion.create(
        temperature=1,
        max_tokens=1000,
        model="gpt-3.5-turbo",
        messages=messages
    )

    ai_response = response['choices'][0]['message']['content']
    print(f"needed information: {ai_response}")
    # トークン数のアウトプットの処理
    token = response["usage"]["total_tokens"]
    # print(f'usage tokens:{token}')
    use_token = Token(token)
    use_token.output_token_information('list_needed_information')

    # Extract the needed information from the AI response
    needed_information_list = re.findall(r'^\d+\.\s(.+)', ai_response, re.MULTILINE)

    return needed_information_list
