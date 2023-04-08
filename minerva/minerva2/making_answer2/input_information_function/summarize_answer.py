import openai

from minerva.token_class import Token


def summarize_answer(openai_api_key: str, task: str, needed_information: str, answers: list[str]):
    openai.api_key = openai_api_key
    system_input = f'''
    Your name is Minerva, and you're an AI that helps the user do their jobs.
    [current task] = {task}
    [needed_information] = {needed_information}
    [answers] = {answers}
    Now you are doing [current task].
    [needed information] is information that is needed to solve [current task].
    [answers] are questions and their answers to obtain [needed information].
    # output lang: jp
    '''

    user_prompt = f'''
    summarize [answers] to meet the information required by [need_information].
    summarize [answers] so that there is no excess or deficiency of information.
    Output only the content of the summary. No preface is needed.
    # output lang: jp
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
    print(f"summarize gpt answers: {ai_response}")
    # トークン数のアウトプットの処理
    token = response["usage"]["total_tokens"]
    print(f'usage tokens:{token}')
    use_token = Token(token)
    use_token.output_token_information('summarize_answer')

    return ai_response
