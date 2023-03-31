import openai

from minerva.token_class import Token


def answer_questions_by_gpt(openai_api_key: str, task: str, needed_information: str, questions: str, role: str):

    openai.api_key = openai_api_key

    system_input = f'''
[task]:現在解きたい課題です
[needed_information]:[task]を解くために必要な情報です
[question]:[needed_information]をさらに細分化したもの
[role]:[question]にこたえる時にアシスタントに与えられる役割

task: {task}
needed_information: {needed_information}
question: {questions}
role: {role}'''

    assistant_prompt = f'''
1. ~~
2. ~~
3. ~~
4. ~~
...'''

    user_prompt = f'''
[question]一つ一つの情報の答えを、詳しく教えて下さい。
既にあなたが学習済みの一般情報をすべて参照して、詳しく答えること。
オンライン上で入手可能な情報や一般的な知識に基づいて構いません。
あなたは、{role}という役割です。

Answer in the form of [1. ~ \n2. ~ \n...]
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
    # トークン数のアウトプットの処理
    token = response["usage"]["total_tokens"]
    # print(f'usage tokens:{token}')
    use_token = Token(token)
    use_token.output_token_information('answer_questions_by_gpt')

    return ai_response
