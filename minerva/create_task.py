from dotenv import load_dotenv
import os
import openai
import re

env_path = os.path.join(os.path.dirname(__file__), '../.env')
load_dotenv(env_path)
openai.api_key = os.environ.get("OPENAI_API_KEY")
# Set up OpenAI API key
openai.api_key = os.environ['OPENAI_API_KEY']

class OutlineCreator:
    def __init__(self, task, position, goal, user_intent, information):
        self.goal = goal
        self.task = task
        self.position = position
        self.user_intent = user_intent
        self.information = information

    def create_task(self):
        # Prepare input for ChatGPT API
        system_input = f"""
{self.goal} is what the user ultimately wants to accomplish.
Now you are doing the task that {self.task}.
The current {self.task} is located at {self.position} in the whole. Answer the question with the whole picture.
{self.user_intent} is user's intent, so keep this request in mind when answering.
You have {self.information}.
"""

        assistant_prompt = f"""
1. ~~
2. ~~
3. ~~
4. ~~
...
"""

        user_prompt = f"""
create an outline for solving {self.task}
example: [1. ~~ \n2. ~~ ...]
"""

        # Build the list of messages for the API
        messages = [
            {"role": "system", "content": system_input},
            {"role": "assistant", "content": assistant_prompt},
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

        output = re.findall(r'^\d+\.\s(.+)', ai_response, re.MULTILINE)

        return output
