import openai
import re
from minerva.token_class import Token


class GenerateHypothesis:

    def __init__(self, openai_api_key: str, goal: str, information: str, hypothesis_list: list[str], user_intent: str,):
        openai.api_key = openai_api_key
        # 一周目
        if not user_intent:
            self.system_input = f'''
            Your name is Minerva, and you're an AI that helps the user do their jobs.
            [goal] = {goal}
            [information] = {information}
            [information] is information provided by the user and should be referenced.
            <constraints>
            Never create multiple tiers.
            Never output anything that is not related to the content of the document, such as the procedure for creating the document.
            # output lang: jp
            '''

            self.user_prompt = f'''
            Hypothesize what content Minerva should include in the document, based on [goal] and [information].
            List all the contents you think should be included.
            Use bullet points and make your hypothesis user-readable.
            <constraints>
            list only what should be included in the document
            # output example: [1. ~\n2. ~\n3. ~\n...]
            # output lang: jp
            '''
        # 2周目以降
        else:
            user_intent_prompt = f'{user_intent} is information that the user has gone to the trouble of entering additionally, so it should always be included in the document.'
            self.system_input = f'''
            Your name is Minerva, and you're an AI that helps the user do their jobs.
            [goal] = {goal}
            [information] = {information}
            [user intent] = {user_intent_prompt}
            [hypothesis prompt] = {hypothesis_list}
            [information] is information provided by the user and should be referenced.
            <constraints>
            Never create multiple tiers.
            Never output anything that is not related to the content of the document, such as the procedure for creating the document.
            The contents of [hypothesis prompt] have already been deemed necessary by the user, so be sure to include them in the documentation
            # output lang: jp
            '''
            self.user_prompt = f'''
            Hypothesize what content Minerva should include in the document, based on [goal] and [information] and [user intent].
            [user intent]
            Use bullet points and make your hypothesis user-readable.
            <constraints>
            list only what should be included in the document.
            # output example: [1. ~\n2. ~\n3. ~\n...]
            # output lang: jp
            '''

        self.assistant_prompt = '''
        1. ~
        2. ~
        3. ~
        ...
        '''

        self.messages = [
            {"role": "system", "content": self.system_input},
            {"role": "assistant", "content": self.assistant_prompt},
            {"role": "user", "content": self.user_prompt}
        ]

    def generate_hypothesis(self):
        response = openai.ChatCompletion.create(
            temperature=0,
            max_tokens=1000,
            model="gpt-3.5-turbo",
            messages=self.messages
        )
        ai_response = response['choices'][0]['message']['content']
        print(f"仮説: {ai_response}")
        token = response["usage"]["total_tokens"]  # インスタンス変数を使って加算する
        print(f'tokens:{token}')
        use_token = Token(token)
        use_token.output_token_information('generate_hypothesis')
        ai_response = ai_response.replace(" ", "")
        raw_hypothesis = re.findall(r'^(?:\d+\..+|-.+)$', ai_response, re.MULTILINE)
        # 数字とピリオドを削除
        hypothesis = [re.sub(r'^\d+\.|-', '', line) for line in raw_hypothesis]
        return hypothesis
