import openai
import re

from minerva.token_class import Token


def answer_questions_by_gpt(openai_api_key: str, task: str, needed_information: str, questions_list: list[str],
                            role: list[str]):
    loop_num = 0
    while True:
        openai.api_key = openai_api_key
        q_and_role = ""
        for i in range(len(questions_list)):
            q_and_role += f"{i+1}. question: {questions_list[i]}, role and skills: {role[i]}\n"

        system_input = f'''
        Your name is Minerva, and you're an AI that helps the user do their jobs.
        [current task] = {task}
        [needed information] ={needed_information}
        [question and role] = {q_and_role}
        Now you are doing [current task].
        [needed information] is needed to solve [current task].
        # output lang: jp
        '''

        assistant_prompt = f'''
        1. ~~
        2. ~~
        3. ~~
        4. ~~
        ...
        '''

        user_prompt = f'''
        [question and role] indicates the question and the role/skill, so answer the question as a professional with the specified role/skill.
        Answer in detail, referring to all the general information you have already learned.
        You may base your answer on information available online or on your general knowledge.
        Be sure to answer all questions.
        If you do not know, please output N/A.
        # output lang: jp
        # output style: [1. ~ \n2. ~ \n...]
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

        answer_list = re.findall(r'^\d+\.(.+)', ai_response, re.MULTILINE)
        loop_num += 1
        if len(questions_list) == len(answer_list):
            questions_answers = ''
            questions_num = 0
            for question in questions_list:
                questions_answers += f'Q:{question}, A: {answer_list[questions_num]}'
                questions_num += 1

            for i in range(len(questions_answers)):
                print(f'{questions_answers[i]}'
                      f'answer as {role[i]}')

            # トークン数のアウトプットの処理
            token = response["usage"]["total_tokens"]
            # print(f'usage tokens:{token}')
            use_token = Token(token)
            use_token.output_token_information('answer_questions_by_gpt')

            return questions_answers
        elif loop_num ==3:
            print("申し訳ございません。未熟者のため、タスクを上手くこなすことができませんでした。"
                  "\n最初からやり直していただくことになってしまいました。")
            break
        else:
            print("ごめんなさい。"
                  "うまく質問に答えることができなかったため、もう一度考えてみます。"
                  "少々お待ちください...")

