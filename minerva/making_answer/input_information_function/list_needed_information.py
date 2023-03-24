import openai
import re
from ..task_tree_element import TaskTreeElement


def list_needed_information(openai_api_key: str, goal: str, tree_element_list: list[TaskTreeElement],
                            processed_task_number: int):
    openai.api_key = openai_api_key
    if len(tree_element_list) == 1:
        information_prompt = f'you have {tree_element_list[0].information}'
        information_prompt_for_user = f'in addition to {tree_element_list[0].information}'
        if tree_element_list[0].information == '':
            information_prompt = 'you have no information'
            information_prompt_for_user = ''

        system_input = f'''
{goal} is what the user ultimately wants to accomplish
Now you are doing the task that create the best output outline to achieve {goal}    
{information_prompt}'''
        user_prompt = f'''
List the information needed to perform the task that  create the best output outline to achieve {goal}
{information_prompt_for_user}
Answer in the form of [1. ~ \n2. ~ \n...]'''

    else:
        # 保留
        system_input = '''
        '''
        user_prompt = '''
        '''

    assistant_prompt = f'''
1. ~~
2. ~~
3. ~~
4. ~~
...'''

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

    # Extract the needed information from the AI response
    needed_information_list = re.findall(r'^\d+\.\s(.+)', ai_response, re.MULTILINE)

    return needed_information_list
