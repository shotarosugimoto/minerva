from ..task_tree_element import TaskTreeElement
import openai

from ...token_class import Token


def create_questions(openai_api_key: str, goal: str, now_task_element: TaskTreeElement, needed_information: str):

    openai.api_key = openai_api_key

    system_input = f'''
    Your name is Minerva, and you're an AI that helps the user do their jobs.
    [goal] = {goal}
    [current task] = {now_task_element.task}
    [needed information] = {needed_information}
    Keep in mind [goal].
    Now you are doing [current task].
    [needed information] is needed to solve [current task].
    # output lang: jp
    '''

    assistant_prompt = '''
    1. ~~
    2. ~~
    3. ~~
    4. ~~
    5. ~~
    ...
    '''

    user_prompt = f'''
    Create a question to acquire the [needed information] needed to do [current task].
    Make the questions as detailed as possible so that [needed information] can be successfully collected.
    # output lang: jp
    # output style: [1. ~ \n2. ~ \n...]
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
    # トークン数のアウトプットの処理
    token = response["usage"]["total_tokens"]
    # print(f'usage tokens:{token}')
    use_token = Token(token)
    use_token.output_token_information('create_questions')

    ai_response = response['choices'][0]['message']['content']
    return ai_response



