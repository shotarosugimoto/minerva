import openai
from minerva.token_class import Token


class SummarizeHypothesis:
    def __init__(self, openai_api_key: str, goal: str, information: str, contents_list: list[str], user_intent: str,):
        openai.api_key = openai_api_key
        information_prompt = ''
        if information != '':
            information_prompt = f'you have {information}.'
        user_intent_prompt = ''
        if user_intent != '':
            user_intent_prompt = f'{user_intent} is user\'s intent, so keep this request in mind when answering.'

        self.system_input = f"""
        Your name is Minerva, and you're an AI that helps the user do their jobs.
        [goal] = {goal} 
        [information] = {information_prompt}
        [user intent] = {user_intent_prompt}
        [contents] = {contents_list}
        [contents] is the content that the user has determined needs to be included in the document
        # output lang: jp
        """

        self.user_prompt = f"""
        Set the goal of the work that Minerva will do appropriately 
        by summarizing what kind of documentation Minerva will produce to accomplish [goal] 
        and include the reason why Minerva set such a goal in japanese.
        <constraints>
        Briefly describe the document that should be produced in Minerva.
        # output lang: jp
        """
        self.messages = [
            {"role": "system", "content": self.system_input},
            {"role": "user", "content": self.user_prompt}
        ]

    def create_summarize(self):

        response = openai.ChatCompletion.create(
            temperature=0,
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
