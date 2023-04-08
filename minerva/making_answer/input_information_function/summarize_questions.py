import openai
from ..task_tree_element import TaskTreeElement
from minerva.token_class import Token


def summarize_questions(openai_api_key: str, task: str, needed_information: list[str], questions: list[str],
                        tree_element_list: list[TaskTreeElement],
                        processed_task_number: int):
    openai.api_key = openai_api_key
    need_info_and_questions = ""
    for i in range(len(needed_information)):
        need_info_and_questions += f"needed information: {needed_information[i]}, question: {questions[i]}"

    system_input = f'''
    Your name is Minerva, and you're an AI that helps the user do their jobs.
    [current task] = {task}
    [owned information] = {tree_element_list[0].information}
    [needed information and questions] = {need_info_and_questions}
    Now you are doing [current task].
    [needed information and questions] is the information needed to do the [current task] and the questions to get that information.
    # output lang: jp
    '''

    assistant_prompt = f'''
            1. ~~
            2. ~~
            3. ~~
            ...
            '''

    user_prompt = f'''
    There are a number of questions in [needed information and questions] that are covered, so please summarize questions.
    Do not include needed information in the output. 
    Please combine the same questions into a single question, and create a new bulleted list of questions with no over/underlining.
    Output only the content of questions. No preface is needed.
    Never create a question that requires the user to answer the same question.
    Never create a question that requires the user to answer what is in [owned information].
    # output lang: jp
    # output style: [1. ~\n2. ~\n...]
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
    print(f"summarize questions: {ai_response}")
    # トークン数のアウトプットの処理
    token = response["usage"]["total_tokens"]
    print(f'usage tokens:{token}')
    use_token = Token(token)
    use_token.output_token_information('summarize_questions')

    return ai_response
