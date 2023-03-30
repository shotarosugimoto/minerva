import openai
from ..task_tree_element import TaskTreeElement
from ...token_class import Token


def crate_gpt_role(openai_api_key, now_task_element: TaskTreeElement):
    openai.api_key = openai_api_key

    system_input = f'''
    Your name is Minerva, and you're an AI that helps the user do their jobs.
    [current task] = {now_task_element.task}
    [Owned information] = {now_task_element.information}
        '''

    user_prompt = f'''
    Please tell us what is the most appropriate job title for the [current task].
    Please tell us specifically what abilities, skills, and experience would best fit the position.
    Nouns only
    Do not write in sentences
    output example: [role: ~\nskills: ~]
    '''

    messages = [
        {"role": "system", "content": system_input},
        {"role": "user", "content": user_prompt}
    ]

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
    use_token.output_token_information('crate_gpt_role')

    return ai_response
