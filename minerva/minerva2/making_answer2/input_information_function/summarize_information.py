import openai

from minerva.token_class import Token


def summarize_information(openai_api_key: str, task: str, pre_information: str, needed_information_list: list[str],
                          answer_list: list[str]):
    openai.api_key = openai_api_key

    system_input = f'''
    Your name is Minerva, and you're an AI that helps the user do their jobs.
    [current task] = {task}
    [owned information] = {pre_information}
    [needed information] = {needed_information_list}
    [answers] = {answer_list}
    Now you are doing [current task].
    [owned information] is information that is needed and available for reference when solving [current task].
    [needed information] is information that is needed to solve [current task].
    [answers] are questions and their answers to obtain [needed information]
    # output lang: jp
    '''

    user_prompt = f'''
    summarize [Owned information] and [answers] to accomplish [current task].
    summarize [Owned information] and [answers] so that there is no excess or deficiency of information.
    # output lang: jp
    '''

    messages = [
        {"role": "system", "content": system_input},
        {"role": "user", "content": user_prompt},
    ]

    response = openai.ChatCompletion.create(
        temperature=0,
        max_tokens=1000,
        model="gpt-3.5-turbo",
        messages=messages
    )
    ai_response = response['choices'][0]['message']['content']
    print(f"summarized information acquired by IIF: {ai_response}")
    # トークン数のアウトプットの処理
    token = response["usage"]["total_tokens"]
    print(f'usage tokens:{token}')
    use_token = Token(token)
    use_token.output_token_information('summarize_information')

    return ai_response
