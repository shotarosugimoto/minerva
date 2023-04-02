import openai

from minerva.token_class import Token


def answer_reliable_check(openai_api_key: str, task: str, needed_information: str, answer: str):
    openai.api_key = openai_api_key
    system_input = f'''
    Your name is Minerva, and you're an AI that helps the user do their jobs.
    [current task] = {task}
    [needed_information] = {needed_information}
    [answers] = {answer}
    Now you are doing [current task].
    [needed information] is information that is needed to solve [current task].
    [answers] are questions and their answers to obtain [needed information].
    '''

    assistant_prompt = f'''
    F
    '''

    user_prompt = f'''
    Output "T" if [answers] is correct.
    Output "F" if [answers] may contain errors.    
    Be sure to output only "T" or "F".
    Do not write any other explanations, notes, or circumstances that led to the output.
    just write "T" or "F".
    '''

    messages = [
        {"role": "system", "content": system_input},
        {"role": "assistant", "content": assistant_prompt},
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

    if ai_response.strip() == "T":
        print(f"{answer}\ncorrect information")
        return True
    elif ai_response.strip() == "F":
        print(f"{answer}\nPossible error in information")
        return False
    else:
        return "Error: Invalid response"
