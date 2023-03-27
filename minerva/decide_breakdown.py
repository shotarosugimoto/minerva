from dotenv import load_dotenv
import os
import openai
import re

env_path = os.path.join(os.path.dirname(__file__), '../.env')
load_dotenv(env_path)
openai.api_key = os.environ.get("OPENAI_API_KEY")

class ProblemBreakdown:
    def __init__(self, task, position, goal, user_intent, information):
        self.goal = goal
        self.task = task
        self.position = position
        self.user_intent = user_intent
        self.information = information

    def should_split_problem(self):
        # Prepare input for ChatGPT API
        system_input = f"""
{self.goal} is what the user ultimately wants to accomplish.
Now you are doing the task that {self.task}
The current {self.task} is located at {self.position} in the whole. Answer the question with the whole picture.
{self.user_intent} is user's intent, so keep this request in mind when answering.
You have {self.information}.
"""

        user_prompt = f"""
Determine whether or not you need to split the problem into separate issues in order to solve {self.task}.
Print "F" if you need to split the problem, 
or print "T" if you do not need to split the problem.
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

        # Check the content of ai_response and return the appropriate response
        if ai_response.strip() == "T":
            return True
        elif ai_response.strip() == "F":
            return False
        else:
            return "Error: Invalid response"

