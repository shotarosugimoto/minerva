import openai
from minerva.making_answer.task_tree_element import TaskTreeElement


def create_answer_from_bottom_elements(openai_api_key: str, goal: str, tree_element_list: list[TaskTreeElement],
                                       processed_task_number: int):
    openai.api_key = openai_api_key
    # 事前準備 現在のタスクの子供の情報や子供のタスク&アンサーを取得する必要がある
    current_task = tree_element_list[processed_task_number]
    parents_task = current_task.parent
    children_task_list = current_task.children #現在のタスクの下のタスクのリスト
    all_information = ''
    children_task_and_answer_prompt = ''
    all_information += current_task.information + '\n'
    all_information += parents_task.information + '\n'

    for element in children_task_list:
        all_information += element.information + '\n'
        children_task_and_answer_prompt += f'task:{element.task}, answer:{element.answer}'

    system_input = f'''
Your name is Minerva, and you're an AI that helps the user do their jobs.
[goal] = {goal}
[current task] = {tree_element_list[processed_task_number]}
[Owned information] = {all_information}
[user intent] = {current_task.user_intent}
[Subdivided tasks and answers] = {children_task_and_answer_prompt} 
Keep in mind [goal].
Now you are doing [current task] to accomplish {parents_task}.
[Owned information] is information that is needed and available for reference when solving [current task].
[user intent] is user\'s intent, so keep this request in mind when answering.
Since [Subdivided tasks and answers] are the tasks and their answers broken down to do [current_task].
Currently, [current task] is divided {tree_element_list[processed_task_number].depth} times from the final output.
# output lang: jp
    '''
    assistant_prompt = f'''
1.題名: ~
1.説明: ~
2.題名: ~
2.説明: ~
...
    '''
    user_prompt = f'''
Use [Owned information] and [Subdivided tasks and answers] to answer [current task] in detail.
Keep in mind that you are doing [current task] to do [parent task].
If there are themes, list each theme separately.
Each theme should have two parts: a summary and a detailed explanation.
Write a summary before the detailed explanation so that busy people can look at it quickly.
Write a detailed explanation so that everyone can easily understand it.
# output lang: jp
output example: [1.題名: ~\n1.説明: ~\n2.題名: ~\n2.説明\n...]
'''

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

    tree_element_list[processed_task_number].answer = ai_response
