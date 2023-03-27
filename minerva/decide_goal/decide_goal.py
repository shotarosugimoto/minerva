import sys
sys.path.append('/Users/tasuku/SALT2')

from .generate_hypothesis import GenerateHypothesis
from .summarize_hypothesis import SummarizeHypothesis


class DecideGoal2:

    def __init__(self, openai_api_key: str, goal: str, information: str):
        self.openai_api_key = openai_api_key
        self.goal = goal
        self.information = information
        self.user_intent_for_summarize = ''
        self.user_intent_for_hypothesis = ''

    def redefine_goal(self):
        generate_hypothesis = GenerateHypothesis(
            openai_api_key=self.openai_api_key,
            goal=self.goal,
            information=self.information,
            user_intent=self.user_intent_for_hypothesis,
        )
        print('Please wait a moment.')
        ##最初の仮説を作り、ユーザーに見せる
        initial_hypothesis_list = generate_hypothesis.generate_hypothesis()
        print('There are hypothesis\n')
        for num in range(len(initial_hypothesis_list)):
            print(f'{num+1}. {initial_hypothesis_list[num]}')

        print('\nIf you are satisfied with these hypotheses, press enter. '
              'If not, please write additional information to generate new hypotheses')

        hypothesis_list = initial_hypothesis_list
        self.user_intent_for_hypothesis = input('Press enter or write additional information:')
        # ユーザーが求める仮説が見つかるまでループ
        while 1:
            del generate_hypothesis
            if self.user_intent_for_hypothesis == '':
                break
            generate_hypothesis = GenerateHypothesis(
                openai_api_key=self.openai_api_key,
                goal=self.goal,
                information=self.information,
                user_intent=self.user_intent_for_hypothesis,
            )
            print('Please wait a moment.')
            hypothesis_list = generate_hypothesis.generate_hypothesis()
            print('仮説\n')
            """
            print('There are hypothesis\n')
            """
            for num in range(len(hypothesis_list)):
                print(f'{num + 1}. {hypothesis_list[num]}')
            print('\nIf you are satisfied with these hypotheses, press enter.'
                  'If not, please write additional information to generate new hypotheses')
            self.user_intent_for_hypothesis = input('Press enter or write additional information')

        print('Thank you for choosing hypothesis.')
        print('The next step is to choose some correct hypothesis out of the five hypotheses\n')
        new_hypothesis_list = []

        while 1:
            for num in range(len(hypothesis_list)):
                print(f'{num+1}. {hypothesis_list[num]}')
                user_input = input('Enter 0 if you accept this hypothesis, 1 if you do not.')
                if user_input == '0':
                    new_hypothesis_list.append(hypothesis_list[num])
            if len(new_hypothesis_list):
                break
            new_hypothesis_list = []
            print('You should choose more than one hypotheses')

        while 1:
            summarize_hypothesis = SummarizeHypothesis(
                openai_api_key=self.openai_api_key,
                goal=self.goal,
                information=self.information,
                hypothesis_list=new_hypothesis_list,
                user_intent=self.user_intent_for_summarize,
            )
            print('We are creating more obvious goal')
            print('Please wait a moment.\n')
            summarize_result = summarize_hypothesis.create_summarize()

            print('Here are some of the more obvious goal we came up with:')
            print(f'{summarize_result}\n')
            del summarize_hypothesis
            user_answer = input('Enter 0 if you are satisfied with this goal, 1 otherwise:')

            if user_answer == '0':
                break
            self.user_intent_for_summarize = input('please write additional information to generate new goal')

        return summarize_result
class DecideGoal:
    def __init__(self, openai_api_key: str, goal: str, information: str):
        self.openai_api_key = openai_api_key
        self.goal = goal
        self.information = information
        self.user_intent_for_summarize = ''
        self.user_intent_for_hypothesis = ''
    # redefine_goalで呼び出される。ミネルバが出した仮説を取捨選択する機能
    def select_hypothesis(self, hypothesis_list):
        selected_hypotheses = []
        print("最終的に私が作成するものは以下のようなものでよろしいでしょうか？\nここで選択されなかった仮説は破棄され、選択された仮説をもとに最終的なアウトプットイメージを出力します")
        for num in range(len(hypothesis_list)):
            print(f'{num+1}. {hypothesis_list[num]}')
        for num in range(len(hypothesis_list)):
            print(f'{num + 1}. {hypothesis_list[num]}')
            user_input = input('Enter Y if you accept this hypothesis, N if you do not.')
            while user_input not in ['Y', 'N']:
                print('Invalid input. Please enter Y if you accept this hypothesis, N if you do not.')
                user_input = input()
            if user_input == 'Y':
                selected_hypotheses.append(hypothesis_list[num])
        return selected_hypotheses

    # main.pyで最初に呼び出される。ゴールを規定する機能
    def redefine_goal(self):
        tokens = 0
        selected_hypotheses = None
        generate_hypothesis = None  
        while True:
            new_intnt = ""
            del generate_hypothesis
            # 仮説を生成
            generate_hypothesis = GenerateHypothesis(
                openai_api_key=self.openai_api_key,
                goal=self.goal,
                information=self.information,
                hypothesis_list = selected_hypotheses,
                user_intent=self.user_intent_for_hypothesis,
                token = tokens
            )
            print('Please wait a moment.')
            #ミネルバが出した仮説を取捨選択する機能
            hypothesis_list, tokens = generate_hypothesis.generate_hypothesis()
            print(f'total tokens: {tokens}')
            # ユーザーに仮説を選択させる
            selected_hypotheses = self.select_hypothesis(hypothesis_list)
            
            # 新しい仮説が必要ならば追加情報を入力させる
            new_intnt = input('追加の要望を入力して新しい仮説を生成するか、満足している場合は Enter を押してください:')
            #追加情報が入力されなかったら、サマライズに進む
            if not new_intnt:
                #仮説が一つも選択されていなかったら、エラーを返し、最初から仮説を作り直す
                if not selected_hypotheses:
                    print('少なくとも1つは意図にあった仮説が出てくるまで情報をください')
                    continue
                else:
                    break
            # 情報が入力されたら、選択された仮説と追加情報をuser intentに入れて新たに仮説を生成するループに戻る
            else:
                user_intent_for_hypothesis = new_intnt + ', '.join(selected_hypotheses)
            print(f"user_intent_for_hypothesis: {user_intent_for_hypothesis}")
            continue
        
        # 選択された仮説を要約して明確な目標を作成
        while True:
            summarize_hypothesis = SummarizeHypothesis(
                openai_api_key=self.openai_api_key,
                goal=self.goal,
                information=self.information,
                hypothesis_list=selected_hypotheses,
                user_intent=self.user_intent_for_summarize,
                token = tokens
            )
            print('情報の提供ありがとうございます！\n')
            print('最終的なアウトプットのイメージを考えていますので、少々お待ちください。\n')
            summarize_result, tokens  = summarize_hypothesis.create_summarize()

            print('こちらが、私が今考えているアウトプットのイメージです:')
            print(f'{summarize_result}\n')
            print(f'total tokens: {tokens}')

            user_answer = input('このアウトプットの形で大丈夫な場合は 0 を入力し、そうでない場合は 1 を入力してください')
            # 最終的にはここをマニュアルで編集も可能にしたい
            while user_answer not in ['0', '1']:
                user_answer = input('Invalid input. このアウトプットの形で大丈夫な場合は 0 を入力し、そうでない場合は 1 を入力してください')
            if user_answer == '0':
                break
            del summarize_hypothesis
            # 新たな目標を生成するための追加情報を入力させる
            self.user_intent_for_summarize =input('より正確なアウトプットイメージを作るために追加情報を入力してください:')
        
        return summarize_result, tokens
