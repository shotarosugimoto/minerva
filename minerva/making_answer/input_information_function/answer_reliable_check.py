import openai

from minerva.token_class import Token


def answer_reliable_check(openai_api_key: str, task: str, needed_information: str, answer: str):
    openai.api_key = openai_api_key
    system_input = f'''
[task]:現在解きたい課題です
[need info]：[task]を解くために必要な情報です。
[need info ans]:[need info]の回答です

task: {task}
need info: {needed_information}
need info ans: {answer}'''

    user_prompt = f'''
[task]を解くために必要な[need info]のうち、[need info ans]は十分でしょうか？
十分である場合は、0とだけお答えください。
十分ではない場合は、1とお答えください
'''

    messages = [
        {"role": "system", "content": system_input},
        {"role": "user", "content": user_prompt},
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
    use_token.output_token_information('answer_reliable_check')

    return ai_response
