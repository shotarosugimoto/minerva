from dotenv import load_dotenv
import os
from decide_goal.decide_goal import DecideGoal
from making_answer.making_answer import MakingAnswer
from token_class import Token


def main():
    # APIKeyの取得
    env_path = os.path.join(os.path.dirname(__file__), '../.env')
    load_dotenv(env_path)
    openai_api_key: str = os.environ.get("OPENAI_API_KEY")

    # アウトプットファイルの作成、初期化
    Token.create_token_file()

    # 最初に言語選択をして、それをlangに入れるといいかもしれない
    # 最初のユーザーインプット
    initial_goal = input('（何を作ってほしいですか？） What would you like to create with Minerva? (This is required): ')
    while True:
        if initial_goal != '':
            break
        initial_goal = input('（何を作ってほしいですか？） What would you like to create with Minerva? (This is required): ')

    initial_purpose = input('(This is required) （どんな目的で使用しますか？「〜のため」の形式で答えて下さい）the output is used to: ')
    while True:
        if initial_purpose != '':
            break
        initial_purpose = input('(This is required) （どんな目的で使用しますか？「〜のため」の形式で答えて下さい）the output is used to : ')

    # ユーザーインプットを元にゴールの設定
    initial_goal = "What the user wants to create with Minerva is" + initial_goal
    initial_purpose = "Minerva's output is used to" + initial_purpose
    initial_goal += initial_goal + " , " + initial_purpose

    initial_add_information = input('(optional) Write your additional information : ')

    initial_information = "Additional information provided by the user: " + initial_add_information

    # decide_goalの処理
    # 一番大きいアウトラインまで完成する
    decide_goal = DecideGoal(openai_api_key=openai_api_key, goal=initial_goal, information=initial_information)
    new_goal = decide_goal.redefine_goal()

    making_answer = MakingAnswer(openai_api_key=openai_api_key, initial_goal=new_goal,
                                 initial_information=initial_information)

    processed_task_number: int = 0
    step_number: int = 0

    while 1:
        process_location = making_answer.task_process(processed_task_number=processed_task_number,
                                                      step_number=step_number)
        processed_task_number = process_location[0]
        step_number = process_location[1]
        if processed_task_number == 0 and step_number == 3:
            break

    making_answer.print_final_answer()

