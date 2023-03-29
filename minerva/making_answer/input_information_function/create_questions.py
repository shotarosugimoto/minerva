from ..task_tree_element import TaskTreeElement
import openai


def create_questions(openai_api_key: str, goal: str, now_task_element: TaskTreeElement, needed_information: str, tool: str,):

    openai.api_key = openai_api_key

    system_input = f'''
[goal] = {goal}
[current task] = {now_task_element.task}
Now you are doing [current task] to achieve [goal].
{needed_information}は{now_task_element.task}をこなすために必要な情報です
{tool}:{needed_information}をとってくる際に使うツールです'''

    assistant_prompt = '''
1. ~~
2. ~~
3. ~~
4. ~~
5. ~~
...'''

    user_prompt = f'''
現在のステップは。{now_task_element.task}をこなすために必要な{needed_information}を、{tool}を使って収集することです。
[output style]
この時{needed_information}を収集できるように、{needed_information}をできる限り細分化して、箇条書きで列挙しなさい。
Answer in the form of [1. ~ \n2. ~ \n...]
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
    return ai_response



