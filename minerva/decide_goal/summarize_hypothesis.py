import openai


class SummarizeHypothesis:
    def __init__(self, openai_api_key, goal, information, hypothesis_list, user_intent):
        openai.api_key = openai_api_key
        information_prompt = ''
        if information != '':
            information_prompt = f'you have {information}.'
        user_intent_prompt = ''
        if user_intent != '':
            user_intent_prompt = f'{user_intent} is user\'s intent, so keep this request in mind when answering.'

        self.system_input = f"""
{goal} is what the user ultimately wants to accomplish.
{information_prompt}
{user_intent_prompt}
"""
        self.user_prompt = f"""
create a concise and information-dense summary of the information gathered in {hypothesis_list}
"""
        self.messages = [
            {"role": "system", "content": self.system_input},
            {"role": "user", "content": self.user_prompt}
        ]

    def create_summarize(self):

        response = openai.ChatCompletion.create(
            temperature=1,
            max_tokens=1000,
            model="gpt-3.5-turbo",
            messages=self.messages
        )

        ai_response = response['choices'][0]['message']['content']
        return ai_response
