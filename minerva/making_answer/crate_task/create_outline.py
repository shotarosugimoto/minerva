import openai
from ..task_tree_element import TaskTreeElement
import re


def create_outline(openai_api_key: str, goal: str, tree_element_list: list[TaskTreeElement],
                   processed_task_number: int, initial_information: str):
    openai.api_key = openai_api_key

    if len(tree_element_list) == 1:
        information_prompt = tree_element_list[0].information
        system_input = f'''
Your name is Minerva, and you're an AI that helps the user do their jobs.
[goal] = {goal}
[current task] = create the best output outline to achieve [goal]
[Owned information] = {information_prompt}
[user intent] = {initial_information}
Keep in mind [goal].
Now you are doing [current task].
[Owned information] is information that is needed and available for reference when solving [current task].
[user intent] is user\'s intent, so keep this request in mind when answering.
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
[current task] = {tree_element_list[processed_task_number]}
[Owned information] = {tree_element_list[processed_task_number].information}
[user intent] = {parents_task.user_intent}
Keep in mind [goal].
Now you are doing [current task].
[Owned information] is information that is needed and available for reference when solving [current task].
[user intent] is user\'s intent, so keep this request in mind when answering.
{task_and_answer_prompt} are tasks and their answers on the same layer as [current task]
, which are decomposed tasks to solve {parents_task}.
Currently, [current task] is divided {tree_element_list[processed_task_number].depth} times from the final output.
# output lang: jp
        '''

    assistant_prompt = f'''
1. ~~
2. ~~
3. ~~
4. ~~
...'''

    user_prompt = f'''
Think about what steps you need to break down into in order to do [current task]
Structure the task in a logical sequence
Do not write anything other than the issues and steps.
# output lang: jp
example: [1. ~~ \n2. ~~ ...]
    '''

    messages = [
        {"role": "system", "content": system_input},
        {"role": "assistant", "content": assistant_prompt},
        {"role": "user", "content": user_prompt}
    ]

    # Call the ChatCompletion API
    response = openai.ChatCompletion.create(
        temperature=1,
        max_tokens=1000,
        model="gpt-3.5-turbo",
        messages=messages
    )

    ai_response = response['choices'][0]['message']['content']

    output = re.findall(r'^\d+\.\s(.+)', ai_response, re.MULTILINE)

    return output
