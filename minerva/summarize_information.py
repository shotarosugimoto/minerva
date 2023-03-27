from dotenv import load_dotenv
import os
import openai
import re

env_path = os.path.join(os.path.dirname(__file__), '../.env')
load_dotenv(env_path)
openai.api_key = os.environ.get("OPENAI_API_KEY")

class SummarizeInformation:
    def __init__(self, goal, task, user_intent, contents):
        self.goal = goal
        self.task = task
        self.user_intent = user_intent
        self.contents = contents

    def summarize(self):
        # Prepare input for ChatGPT API
        system_input = f"""
{self.goal} is what the user ultimately wants to accomplish.
Now you are doing the task that {self.task}
{self.user_intent} is user's intent, so keep this request in mind when answering
"""

        user_prompt = f"""
create a concise and information-dense summary of the information gathered in {contents}
"""

        # Build the list of messages for the API
        messages = [
            {"role": "system", "content": system_input},
            {"role": "user", "content": user_prompt}
        ]

        # Call the ChatCompletion API
        response = openai.ChatCompletion.create(
            temperature=1,
            max_tokens=1000,
            model="gpt-3.5-turbo",
            messages=messages
        )

        ai_response = response['choices'][0]['message']['content']
        return ai_response
