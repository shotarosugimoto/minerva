from .generate_hypothesis import GenerateHypothesis
from .summarize_hypothesis import SummarizeHypothesis


class DecideGoal:
    def __init__(self, openai_api_key: str, goal: str, information: str):
        self.openai_api_key = openai_api_key
        self.goal = goal
        self.information = information
        self.user_intent_for_summarize = ''
        self.user_intent_for_hypothesis = ''

    # main.pyで最初に呼び出される。ゴールを規定する機能
    def redefine_goal(self):
        selected_hypotheses = []

        while True:
            generate_hypothesis = GenerateHypothesis(
                openai_api_key=self.openai_api_key,
                goal=self.goal,
                information=self.information,
                hypothesis_list=selected_hypotheses,
                user_intent=self.user_intent_for_hypothesis,
            )
            print('Please wait a moment.')

            hypothesis_list = generate_hypothesis.generate_hypothesis()
            # ユーザーに仮説を選択させる
            selected_hypotheses = select_hypothesis(hypothesis_list)

            # 新しい仮説が必要ならば追加情報を入力させる
            new_intent = input('追加の要望を入力して新しい仮説を生成するか、満足している場合は Enter を押してください:')
            # 追加情報が入力されなかったら、サマライズに進む
            if not new_intent:
                # 仮説が一つも選択されていなかったら、エラーを返し、最初から仮説を作り直す
                if not selected_hypotheses:
                    print('少なくとも1つは意図にあった仮説が出てくるまで情報をください')
                    continue
                else:
                    break
            # 情報が入力されたら、選択された仮説と追加情報をuser intentに入れて新たに仮説を生成するループに戻る
            else:
                self.user_intent_for_hypothesis = new_intent + ', '.join(selected_hypotheses)
            print(f"user_intent_for_hypothesis: {self.user_intent_for_hypothesis}")
            continue

        # 選択された仮説を要約して明確な目標を作成
        while True:
            summarize_hypothesis = SummarizeHypothesis(
                openai_api_key=self.openai_api_key,
                goal=self.goal,
                information=self.information,
                hypothesis_list=selected_hypotheses,
                user_intent=self.user_intent_for_summarize,
            )
            print('情報の提供ありがとうございます！\n')
            print('最終的なアウトプットのイメージを考えていますので、少々お待ちください。\n')
            summarize_result = summarize_hypothesis.create_summarize()

            print('こちらが、私が今考えているアウトプットのイメージです:')
            print(f'{summarize_result}\n')

            user_answer = input('このアウトプットの形で大丈夫な場合は 0 を入力し、そうでない場合は 1 を入力してください')
            # 最終的にはここをマニュアルで編集も可能にしたい
            while user_answer not in ['0', '1']:
                user_answer = input('Invalid input. このアウトプットの形で大丈夫な場合は 0 を入力し、そうでない場合は 1 を入力してください')
            if user_answer == '0':
                break
            del summarize_hypothesis
            # 新たな目標を生成するための追加情報を入力させる
            self.user_intent_for_summarize = input('より正確なアウトプットイメージを作るために追加情報を入力してください:')

        return summarize_result


# redefine_goalで呼び出される。ミネルバが出した仮説を取捨選択する機能
def select_hypothesis(hypothesis_list):
    selected_hypotheses = []
    print("最終的に私が作成するものは以下のようなものでよろしいでしょうか？\nここで選択されなかった仮説は破棄され、選択された仮説をもとに最終的なアウトプットイメージを出力します")
    for num in range(len(hypothesis_list)):
        print(f'{num + 1}. {hypothesis_list[num]}')
    for num in range(len(hypothesis_list)):
        print(f'{num + 1}. {hypothesis_list[num]}')
        user_input = input('Enter Y if you accept this hypothesis, N if you do not.')
        while user_input not in ['Y', 'N']:
            print('Invalid input. Please enter Y if you accept this hypothesis, N if you do not.')
            user_input = input()
        if user_input == 'Y':
            selected_hypotheses.append(hypothesis_list[num])
    return selected_hypotheses
