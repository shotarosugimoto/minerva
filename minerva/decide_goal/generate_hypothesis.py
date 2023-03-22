import openai
import re


class GenerateHypothesis:

    def __init__(self, openai_api_key: str, goal: str, information: str, user_intent: str):
        openai.api_key = openai_api_key
        information_prompt = ''
        if information != '':
            information_prompt = f'you have {information}.'
        user_intent_prompt = ''
        if user_intent != '':
            user_intent_prompt = f'{user_intent} is user\'s intent, so keep this request in mind when answering.'

        self.system_input = f'''
{goal} is what the user ultimately wants to accomplish.
{information_prompt}
{user_intent_prompt}
##
ensure that there is no discrepancy between what the user wants and what you are ultimately trying to accomplish.'''

        self.assistant_prompt = '''
1. ~~
2. ~~
3. ~~
4. ~~
5. ~~
'''

        self.user_prompt = f'''
make 5 hypotheses about the outputs that users are looking for, based on {goal}
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
        hypothesis = re.findall(r'^\d+\.\s(.+)', ai_response, re.MULTILINE)

        if len(hypothesis) == 5:
            return hypothesis
        else:
            raise ValueError(f"Expected 5 hypotheses, but found {len(hypothesis)}")
