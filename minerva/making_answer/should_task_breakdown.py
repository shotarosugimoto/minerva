from task_tree_element import TaskTreeElement
import openai


def should_task_breakdown(openai_api_key: str, goal: str, tree_element_list: list[TaskTreeElement],
                          processed_task_number: int):
    openai.api_key = openai_api_key

    if len(tree_element_list) == 1:
        # 保留
        system_input = '''
        '''
        assistant_prompt = '''
        '''
        user_prompt = '''
        '''
    else:
        current_task = tree_element_list[processed_task_number]
        parents_task: TaskTreeElement = current_task.parent
        children_task: list[TaskTreeElement] = parents_task.children
        # 保留
        system_input = '''
        '''
        assistant_prompt = '''
        '''
        user_prompt = '''
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

    if ai_response == '0':
        return False
    return True
