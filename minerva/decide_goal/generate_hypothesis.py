import openai
import re


class GenerateHypothesis:

    def __init__(self, openai_api_key: str, goal: str, information: str, hypothesis_list: list[str], user_intent: str,
                 token: int = 0):
        openai.api_key = openai_api_key
        self.token = token
        user_intent_prompt = ''
        if user_intent != '':
            user_intent_prompt = f'{user_intent} is user\'s intent, so keep this request in mind when answering.'
        if hypothesis_list:
            hypothesis_list = f'{hypothesis_list} is likely to be the output that is in line with the user\'s ' \
                              f'intentions, so refer to these'

        self.system_input = f'''
Your name is Minerva, and you're an AI that helps the user do their jobs.
The task is to match the outputs that the user wants with the outputs that 
Minerva will produce before starting the project.
[goal] = {goal}
[information] = {information}
[user intent] = {user_intent_prompt}
[selected hypothesis] = {hypothesis_list}
# output lang: jp
'''

        self.assistant_prompt = '''
1. ~~
2. ~~
3. ~~
'''

        self.user_prompt = f'''
predict what output the user is looking for and come up with 3 hypotheses in japanese, with reference to [goal] 
and [information] and [user intent] and [selected hypothesis]
# output lang: jp
# output example: [1. ~\n2. ~\n3. ~\n...]
'''

        self.messages = [
            {"role": "system", "content": self.system_input},
            {"role": "assistant", "content": self.assistant_prompt},
            {"role": "user", "content": self.user_prompt}
        ]

    def generate_hypothesis(self):
        response = openai.ChatCompletion.create(
            temperature=1,
            max_tokens=1000,
            model="gpt-3.5-turbo",
            messages=self.messages
        )
        ai_response = response['choices'][0]['message']['content']
        self.token += response["usage"]["total_tokens"]  # インスタンス変数を使って加算する
        print(f'tokens:{response["usage"]["total_tokens"]}')
        hypothesis = re.findall(r'^\d+\.\s(.+)', ai_response, re.MULTILINE)

        if len(hypothesis) == 3:
            return hypothesis, self.token
        else:
            raise ValueError(f"Expected 3 hypotheses, but found {len(hypothesis)}")
