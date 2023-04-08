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

        # ドキュメントに含むべき内容をユーザーと決める
        while True:
            generate_hypothesis = GenerateHypothesis(
                openai_api_key=self.openai_api_key,
                goal=self.goal,
                information=self.information,
                hypothesis_list=selected_hypotheses,
                user_intent=self.user_intent_for_hypothesis,
            )
            print('Please wait a moment.')
            # ドキュメントに入れるべきだと考えられる内容を考えて、提示する
            print("-----generate_hypothesis")
            hypothesis_list = generate_hypothesis.generate_hypothesis()
            # ユーザーに仮説を選択させる、選択された仮説が返される
            print("以下の内容をドキュメントに含めるのがいいのではないかと仮説を立ててみました。")
            for num in range(len(hypothesis_list)):
                print(f'{num + 1}. {hypothesis_list[num]}')
            new_intent = input('1から作り直してほしい場合は "1" を入力してくださ\n'
                               '仮説を取捨選択したり、このまま行きたい場合は、Enterを押してください')
            if new_intent == "1":
                continue
            else:
                print("-----select_hypothesis")
                selected_hypotheses = select_hypothesis(hypothesis_list)

                # 新しい仮説が必要ならば追加情報を入力させる
                new_intent = input('満足している場合は "1"'
                                   '\n追加の要望を入力して新しい仮説を生成したい場合は "2"'
                                   '\n: ')
                # 追加情報が入力されなかったら、サマライズに進む
                while new_intent not in ['1', '2']:
                    new_intent = input('満足している場合は "1"'
                                       '\n追加の要望を入力して新しい仮説を生成したい場合は "2"'
                                       '\n: ')
                # 追加情報が入力されなかったら、サマライズに進む
                # 情報が入力されたら、選択された仮説と追加情報をuser intentに入れて新たに仮説を生成するループに戻る
                if new_intent == "2":
                    new_intent = input ('追加の要望を入力してください: ')
                    self.user_intent_for_hypothesis = new_intent

                elif new_intent == "1":
                    # 仮説が一つも選択されていなかったら、エラーを返し、最初から仮説を作り直す
                    if not selected_hypotheses:
                        print('少なくとも1つは意図にあった仮説が出てくるまで情報をください')
                        continue
                    else:
                        break
                continue

        # ドキュメントに入れる内容とユーザーの意図から、ゴールを作成する。ゴールに入るプロンプトとして適切なものにする作業
        while True:
            print("-----summarize_hypothesis")
            summarize_hypothesis = SummarizeHypothesis(
                openai_api_key=self.openai_api_key,
                goal=self.goal,
                information=self.information,
                contents_list=selected_hypotheses,
                user_intent=self.user_intent_for_summarize,
            )
            print(f'内容：\n{selected_hypotheses}')
            print('最終的なアウトプットのイメージを考えていますので、少々お待ちください。\n')
            summarize_result = summarize_hypothesis.create_summarize()

            print('こちらが、私が今考えているアウトプットのイメージです:')
            print(f'{summarize_result}\n')

            user_answer = input('このアウトプットの形で大丈夫な場合は 1 を入力し、そうでない場合は 2 を入力してください')
            # 最終的にはここをマニュアルで編集も可能にしたい
            while user_answer not in ['1', '2']:
                user_answer = input('Invalid input. このアウトプットの形で大丈夫な場合は 1 を入力し、そうでない場合は 2 を入力してください')
            if user_answer == '1':
                break
            del summarize_hypothesis
            # 新たな目標を生成するための追加情報を入力させる
            self.user_intent_for_summarize = input('より正確なアウトプットイメージを作るために追加情報を入力してください:')

        return summarize_result


# redefine_goalで呼び出される。ミネルバが出した仮説を取捨選択する機能
# 最終的には、仮説全体が表示され、それぞれにチェックボックスがあって、選択されたものがselected_hypothesesに入る
# そして、追加の情報があれば入れてもらう
# そのまま一つのゴールを作成するか、もう少し意図のすり合わせを行うかを選べるようにする
def select_hypothesis(hypothesis_list):
    # ただ選択するだけじゃなくて、一つ一つに文句を言わせてほしい、いいんだけど...みたいなのあるから、
    # それを踏まえて、最初から作り直すのでもいいかもしれない
    selected_hypotheses = []
    print("意図に合うものを選択して下さい\nここで選択されなかった内容は破棄され、選択された内容をもとに最終的なアウトプットイメージを考えます")
    for num in range(len(hypothesis_list)):
        print(f'{num + 1}. {hypothesis_list[num]}')
        user_input = input('Enter 1 if you accept this hypothesis, 2 if you do not.')
        while user_input not in ['1', '2']:
            print('Invalid input. Please enter 1 if you accept this hypothesis, 2 if you do not.')
            user_input = input()
        if user_input == '1':
            selected_hypotheses.append(hypothesis_list[num])
    return selected_hypotheses
