import openai
from minerva.token_class import Token


class SummarizeHypothesis:
    def __init__(self, openai_api_key: str, goal: str, information: str, hypothesis_list: list[str], user_intent: str,):
        openai.api_key = openai_api_key
        information_prompt = ''
        if information != '':
            information_prompt = f'you have {information}.'
        user_intent_prompt = ''
        if user_intent != '':
            user_intent_prompt = f'{user_intent} is user\'s intent, so keep this request in mind when answering.'
        print(f"user intent:{user_intent_prompt}")
        self.system_input = f"""
Your name is Minerva, and you're an AI that helps the user do their jobs.
The task is to match the outputs that the user wants with the outputs that Minerva will produce 
before starting the project.
{goal} 
{information_prompt}
{user_intent_prompt}
# output lang: jp
"""
        self.user_prompt = f"""
From the {hypothesis_list}, please provide an outline of the outputs that Minerva should create.
# output lang: jp
"""
        
        self.assistant_prompt = f"""
        1. (title): (contents)
        2. (title): (contents)
        3. (title): (contents)
        4. (title): (contents)
        5. (title): (contents)
        ...
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
        token = response["usage"]["total_tokens"]  # インスタンス変数を使って加算する
        print(f'usage tokens:{token}')
        use_token = Token(token)
        use_token.output_token_information('create_summarize')

        return ai_response
