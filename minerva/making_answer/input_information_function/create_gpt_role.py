import openai
import re

from minerva.token_class import Token


def create_gpt_role(openai_api_key: str, task: str, needed_information: str, questions_list: list[str]):
    loop_num = 0
    while True:
        openai.api_key = openai_api_key
        questions = ""
        number = 1
        for question in questions_list:
            questions += f"{number}. {question}\n"
            number += 1

        system_input = f'''
        Your name is Minerva, and you're an AI that helps the user do their jobs.
        [current task] = {task}
        [needed information]: {needed_information}
        [question] = {questions}
        Now you are doing [current task].
        [needed information] is the information needed to do the [current task], and [questions] are created to acquire [needed information].
        '''

        assistant_prompt = '''
        1. role: ~, skills: ~
        2. role: ~, skills: ~
        3. role: ~, skills: ~
        ...
        '''

        user_prompt = f'''
        Please tell us what is the most appropriate job title for answering [question].
        Please tell us specifically what abilities, skills, and experience would best fit the position.
        Nouns only
        Do not write in sentences
        output example: [1. role: ~, skills: ~\n2. role: ~, skills: ~\n...]
        '''

        messages = [
            {"role": "system", "content": system_input},
            {"role": "assistant", "content": assistant_prompt},
            {"role": "user", "content": user_prompt}
        ]

        response = openai.ChatCompletion.create(
            temperature=0.3,
            max_tokens=1000,
            model="gpt-3.5-turbo",
            messages=messages
        )
        ai_response = response['choices'][0]['message']['content']
        # トークン数のアウトプットの処理
        token = response["usage"]["total_tokens"]
        # print(f'usage tokens:{token}')
        use_token = Token(token)
        use_token.output_token_information('create_gpt_role')
        ai_response = ai_response.replace(" ", "")
        gpt_role = re.findall(r'^\d+\.(.+)', ai_response, re.MULTILINE)
        print(f"（確認用）gpt_role: {gpt_role}")
        loop_num += 1
        if len(questions_list) != len(gpt_role):
            print("error questions_listとgpt_roleの長さが違うので"
                  "gpt_roleを出力し直します")
            continue
        elif loop_num ==3:
            print("申し訳ございません。未熟者のため、タスクを上手くこなすことができませんでした。"
                  "\n最初からやり直していただくことになってしまいました。")
            break
        else:
            number = 1
            for j in range(len(gpt_role)):
                print(f"{number}. {questions_list[j]}gpt role and skill: {gpt_role[j]}")
                number += 1
            return gpt_role

