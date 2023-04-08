import openai
from ..task_tree_element import TaskTreeElement
from ...token_class import Token


def solve_task(openai_api_key: str, goal: str, tree_element_list: list[TaskTreeElement], processed_task_number: int,
               role: str):
    # role　使ってないよ！
    openai.api_key = openai_api_key
    # 事前準備
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
    [goal] = {goal}
    [current task] = {current_task.task}
    [Owned information] = {all_information}
    [user intent] = {parents_task.user_intent}
    Keep in mind [goal].
    Now you are doing [current task].
    [Owned information] is information that is needed and available for reference when solving [current task].
    [user intent] is user\'s intent, so keep this request in mind when answering.
    {task_and_answer_prompt} are tasks and their answers on the same layer as [current task]
    , which are decomposed tasks to solve {parents_task.task}.
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
    Use [Owned information] and answer [current task] in detail.
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

    # Call the ChatCompletion API
    response = openai.ChatCompletion.create(
        temperature=1,
        max_tokens=1000,
        model="gpt-3.5-turbo",
        messages=messages
    )

    ai_response = response['choices'][0]['message']['content']

    # トークン数のアウトプットの処理
    token = response["usage"]["total_tokens"]
    print(f'usage tokens:{token}')
    use_token = Token(token)
    use_token.output_token_information('solve_task')

    tree_element_list[processed_task_number].answer = ai_response
