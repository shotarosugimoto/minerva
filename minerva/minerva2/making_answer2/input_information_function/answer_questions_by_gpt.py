import openai
from ..task_tree_element import TaskTreeElement
from minerva.token_class import Token


def answer_questions_by_gpt(openai_api_key: str, now_task_element: TaskTreeElement, task: str, needed_information: str, questions_list: list[str]):
    loop_num = 0
    while True:
        openai.api_key = openai_api_key

        assistant_prompt = f'''
        回答: ~
        '''
        user_prompt = f'''
        <note>
        # [question] indicates the question, so answer the question as a professional.
        # Basically, please use [owned information] to answer the question.
        # First, try to answer the questions from the information in [owned information].
        # Second, try to answer the question by making inferences from the [owned information].
        # Finally, make a general answer.
        <Instruction>
        answer the [question].
        <constraints>
        If you do not know, please output N/A.
        Keep your answers concise.
        Outputting only answers to questions.
        # output lang: jp
        # output style: [回答: ~ ]
        '''
        answer_list = []
        i = 0
        for question in questions_list:
            system_input = f'''
            Your name is Minerva, and you're an AI that helps the user do their jobs.
            [current task] = {task}
            [owned information] = {now_task_element.information}
            [needed information] ={needed_information}
            [question] = {question}
            Now you are doing [current task].
            [needed information] is needed to solve [current task].
            [owned information] is information that Minerva already has.
            # output lang: jp
            '''

            messages = [
                {"role": "system", "content": system_input},
                {"role": "assistant", "content": assistant_prompt},
                {"role": "user", "content": user_prompt}
            ]

            response = openai.ChatCompletion.create(
                temperature=0,
                max_tokens=300,
                model="gpt-3.5-turbo",
                messages=messages
            )
            ai_response = response['choices'][0]['message']['content']
            print(f"question: {question}, "
                  f"\nanswer: {ai_response}")
            answer_list.append(ai_response)
            token = response["usage"]["total_tokens"]
            print(f'usage tokens:{token}')
            use_token = Token(token)
            use_token.output_token_information('answer_questions_by_gpt')

        loop_num += 1
        if len(questions_list) == len(answer_list):
            questions_answers = []
            questions_num = 0
            for question in questions_list:
                questions_answers.append(f'Q:{question}, A: {answer_list[questions_num]}')
                questions_num += 1
            return questions_answers
        elif loop_num ==3:
            print("申し訳ございません。未熟者のため、タスクを上手くこなすことができませんでした。"
                  "\n最初からやり直していただくことになってしまいました。")
            break
        else:
            print("ごめんなさい。"
                  "うまく質問に答えることができなかったため、もう一度考えてみます。"
                  "少々お待ちください...")

