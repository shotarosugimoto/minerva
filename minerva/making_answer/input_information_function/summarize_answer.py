import openai


def summarize_answer(openai_api_key: str, needed_information: str, questions: str, answers: str):
    openai.api_key = openai_api_key
    system_input = f'''
[needed_information]:現在求めている情報です
[questions]：[needed_information]をさらに細分化したもの
[answers]:[questions]の答えです。番号はそれぞれ対応しています。

needed_information: {needed_information}
questions: {questions}
answers: {answers}'''

    user_prompt = f'''
ここでは、[needed_information]の適切な答えを導出するために、[questions]と[answers]を用意しました。
[needed_information]の適切な答えとなるために、[questions]と[answers]の内容をようやくしてください。
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
    return ai_response
