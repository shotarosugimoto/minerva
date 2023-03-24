import openai
from ..task_tree_element import TaskTreeElement
import re


def create_outline(openai_api_key: str, goal: str, tree_element_list: list[TaskTreeElement],
                   processed_task_number: int):
    openai.api_key = openai_api_key
    if len(tree_element_list) == 1:
        user_intent_prompt = ''
        if tree_element_list[processed_task_number].user_intent != '':
            user_intent_prompt = f'{tree_element_list[processed_task_number].user_intent} is user\'s intent, ' \
                                 f'so keep this request in mind when answering.'
        system_input = f'''
{goal} is what the user ultimately wants to accomplish.
Now you are doing the task that {tree_element_list[processed_task_number].task}.
{user_intent_prompt}
You have {tree_element_list[processed_task_number].information}.'''

    else:
        user_intent_prompt = ''
        if tree_element_list[processed_task_number].user_intent != '':
            user_intent_prompt = f'{tree_element_list[processed_task_number].user_intent} is user\'s intent, ' \
                                 f'so keep this request in mind when answering.'
        system_input = f'''
{goal} is what the user ultimately wants to accomplish.
Now you are doing the task that {tree_element_list[processed_task_number].task}.
The current {tree_element_list[processed_task_number].task} is located where the {goal} is 
divided {tree_element_list[processed_task_number].tree_depth} times.
{user_intent_prompt}
You have {tree_element_list[processed_task_number].information}.'''

    assistant_prompt = f'''
1. ~~
2. ~~
3. ~~
4. ~~
...'''

    user_prompt = f'''
create an outline for solving {tree_element_list[processed_task_number].task}
example: [1. ~~ \n2. ~~ ...]'''

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
