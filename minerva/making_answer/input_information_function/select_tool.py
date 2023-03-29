from ..task_tree_element import TaskTreeElement
import openai
import re


def select_tool(openai_api_key: str, goal: str, now_task_element: TaskTreeElement, needed_information: str):
    openai.api_key = openai_api_key

    tool_character = '''
    Information that you should ask the user:
    ・Information that only the user may have accurate information
    ・Information that is known to the user and may need to be verified for accuracy
    ・Information about the user's own knowledge, experience, or feelings, such as subjective information or personal information
    ・Information about which accuracy is important, such as user information and numerical values.

    Information that should be asked to GPT-3.5：
    ・Information that the user does not seem to know
    ・Information available online, such as objective information, general knowledge, or expertise in a particular field
    '''

    if now_task_element.information != '':
        system_input = f'''
Your name is Minerva, and you're an AI that helps the user do their jobs.
[goal] = {goal}
[Owned information] = {now_task_element.information}
[current task] = {now_task_element.task}
Keep in mind [goal]
Now you are doing [current task] to achieve [goal].
[Owned information] is information that is needed and available for reference when solving [current task].
{needed_information} is information other than [Owned information] that is needed to solve [current task].'''

    # informationが空の時
    else:
        system_input = f'''
Your name is Minerva, and you're an AI that helps the user do their jobs.
[goal] = {goal}
[current task] = {now_task_element.task}
[tool character] = {tool_character}
Keep in mind [goal]
Now you are doing [current task] to achieve [goal].
{needed_information} is information that is needed to solve [current task].
[tool character] is'''

    # ここから共通
    assistant_prompt = f'''
1. G
2. U
3. U
...
    '''

    user_prompt = f'''
Using {tool_character} as a reference, 
determine whether each {needed_information} are "Information that you should ask the user" 
or "Information that should be asked to GPT-3.5".
If it is "Information that you should ask the user", output only U.
If it is "Information that should be asked to GPT-3.5", output only G
Do not write the language, output only numbers.
# output example: [1. ~\n2. ~\n3. ~\n...]
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

    tools = []
    for char in ai_response:
        if char == "G" or char == "U":
            tools.append(char)

    if len(tools) == len(needed_information):
        return tools
    else:
        raise ValueError(f"ツールが正確に選択されませんでした")

