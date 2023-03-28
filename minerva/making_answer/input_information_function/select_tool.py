from ..task_tree_element import TaskTreeElement
import openai

from ...token_class import Token


def select_tool(openai_api_key: str, goal: str, now_task_element: TaskTreeElement, needed_information: str):
    openai.api_key = openai_api_key
    if now_task_element.information != '':
        information_prompt = f'''
{now_task_element.information}は、{now_task_element.task}を解くために必要であり、参照できる情報である。
{needed_information}は、{now_task_element.task}を解く際に、現在の{now_task_element.information}以外に必要な情報です。'''
    else:
        information_prompt = f'''
{needed_information}は、{now_task_element.task}を解く際に必要な情報です。'''

    tool_character = '''
userに聞く情報
・userしか正確な情報は持っていないと思われる情報
・userが知っている情報であるとともに、正確性に関して確認が必要な場合がある情報
・主観的な情報や個人情報など、user自身の経験や感情に関する情報
・userの知識や経験に関する情報
・userの情報や数値など、正確性が重要視される情報

GPT-3.5に聞く情報
・userが知らないと思われる情報
・客観的な情報や一般的な知識、特定の分野の専門知識など、オンライン上で入手可能な情報
'''

    system_input = f'''
{goal}は最終的な課題です。
{now_task_element.task}は、{goal}を求めるために、現在取り組んでいる課題である。
{information_prompt}

toolには　['userに聞く情報', 'GPT-3.5に聞く情報']の二つがあります。
以下は、それぞれのtoolに適した情報の例です
userに聞く情報
・userしか正確な情報は持っていないと思われる情報
・userが知っている情報であるとともに、正確性に関して確認が必要な場合がある情報
・主観的な情報や個人情報など、user自身の経験や感情に関する情報
・userの知識や経験に関する情報
・userの情報や数値など、正確性が重要視される情報

GPT-3.5に聞く情報
・userが知らないと思われる情報
・客観的な情報や一般的な知識、特定の分野の専門知識など、オンライン上で入手可能な情報

上の例を参考に、{needed_information}を得るためにどのtoolを使うべきか決めてください
'''
    user_prompt = f'''
{tool_character}を参考にして、{needed_information}が,「userに聞く情報」なのか、「GPT3.5に聞く情報」なのかを判断しなさい
「userに聞く情報」である場合は、0のみ出力してください
「GPT3.5に聞く情報」である場合は、1のみ出力してください
言語は書かず、数字のみ出力しなさい。
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
    # print(f'usage tokens:{token}')
    use_token = Token(token)
    use_token.output_token_information('select_tool')

    if ai_response == '0':
        return 'user_input'
    elif ai_response == '1':
        return 'GPT-3.5'
    else:
        raise ValueError('not 0 or 1')
