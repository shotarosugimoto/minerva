import openai


def create_gpt_role(openai_api_key: str, task: str, needed_information: str, questions: str):

    openai.api_key = openai_api_key

    system_input = f'''
[task]:現在解きたい課題です
[needed_information]:[task]を解くために必要な情報です
[question]:[needed_information]をさらに細分化したもの
[role]:[question]にこたえる時にアシスタントに与えられる役割

task: {task}
needed_information: {needed_information}
question: {questions}
role: 今からあなたに決めてもらいます'''

    user_prompt = f'''
[needed_information]について詳しい立場の人間は、どういう人でしょうか。
ふさわしものを一つだけお答えください。

[output style]
～に詳しい人
名詞だけ記述
文章では書かない
一つのみ記載
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
    return ai_response
