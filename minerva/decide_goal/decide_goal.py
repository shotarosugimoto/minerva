from .generate_hypothesis import GenerateHypothesis
from .summarize_hypothesis import SummarizeHypothesis


class DecideGoal:
    openai_api_key = ''
    goal = ''
    information = ''
    user_intent_for_hypothesis = ''
    user_intent_for_summarize = ''

    def __init__(self, openai_api_key, goal, information):
        self.openai_api_key = openai_api_key
        self.goal = goal
        self.information = information

    def redefine_goal(self):
        generate_hypothesis = GenerateHypothesis(
            openai_api_key=self.openai_api_key,
            goal=self.goal,
            information=self.information,
            user_intent=self.user_intent_for_hypothesis,
        )
        print('Please wait a moment.')
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
            print('There are hypothesis\n')
            for num in range(len(hypothesis_list)):
                print(f'{num + 1}. {hypothesis_list[num]}')
            print('\nIf you are satisfied with these hypotheses, press enter.'
                  'If not, please write additional information to generate new hypotheses')
            self.user_intent_for_hypothesis = input('Press enter or write additional information')

        while 1:
            summarize_hypothesis = SummarizeHypothesis(
                openai_api_key=self.openai_api_key,
                goal=self.goal,
                information=self.information,
                hypothesis_list=hypothesis_list,
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
