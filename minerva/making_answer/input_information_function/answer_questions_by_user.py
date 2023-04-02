

def answer_questions_by_user(goal: str, needed_information: str, questions_list: list[str]):
    print(f'''
現在、必要な情報を取得するために以下の質問に対する答えをあなたに答えてもらう必要があります。
[必要な情報]
{needed_information}

[質問]
それぞれの質問に対する適切な入力をお願いします。
''')
    questions_answers = ''
    questions_num = 1
    for question in questions_list:
        print(f'{questions_num}.{question}')
        answer = input('答え: ')
        questions_answers += f'Q:{question}, A: {answer}\n'
        questions_num += 1

    return questions_answers
