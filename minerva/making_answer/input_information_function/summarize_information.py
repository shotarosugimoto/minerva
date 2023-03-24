import openai


def summarize_information(openai_api_key: str, task: str, pre_information: str, needed_information_list: list[str],
                          answer_list: list[str]):
    needed_information = ''
    answer = ''
    for i in range(len(needed_information_list)):
        needed_information += f'{i+1}.{needed_information_list[i]}\n'
        answer += f'{i+1}.{answer_list[i]}\n'

    openai.api_key = openai_api_key
    system_input = f'''
[task]:現在解きたい課題です。
[pre info]:[task]を解くための情報で、元々存在していた情報です。
[need　info]:[task]を解くために必要な情報です。その答えは[answer]です。番号はそれぞれ対応しています。
[answer]:[need info]の答えです。番号はそれぞれ対応しています。

task: {task}
pre info: {pre_information}
need info: {needed_information}
answer: {answer}'''

    user_prompt = f'''
[pre info],[need info]を、[answer]を参考にまとめなさい。
[task]に役立つ情報をまとめること。'''

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
