import re


def answer_questions_by_user(goal: str, needed_information: str, questions: str):
    print(f'''
今私たちは以下のゴールの適切な答えを探しています。
[ゴール]
{goal}

現在、必要な情報を取得するために以下の質問に対する答えをあなたに答えてもらう必要があります。
[必要な情報]
{needed_information}

[質問]
{questions}
それぞれの質問に対する適切な入力をお願いします。
''')
    questions_list = re.findall(r'^\d+\.\s(.+)', questions, re.MULTILINE)
    questions_answers = ''
    questions_num = 1
    for question in questions_list:
        print(f'{questions_num}.{question}')
        answer = input('答え: ')
        questions_answers += f'{questions_num}. {answer}\n'
        questions_num += 1

    return questions_answers
