from dotenv import load_dotenv
import os
import openai
import re

env_path = os.path.join(os.path.dirname(__file__), '../../.env')
load_dotenv(env_path)
openai.api_key = os.environ.get("OPENAI_API_KEY")




class ReliabilityChecker:
    def __init__(self, goal, task, user_intent):
        self.goal = goal
        self.task = task
        self.user_intent = user_intent

    def check(self, answer):
        # Prepare input for ChatGPT API
        system_input = f"""
{self.goal} is what the user ultimately wants to accomplish.
Now you are doing the task that {self.task}
{self.user_intent} is user's intent, so  keep this request in mind when answering
{answer} is gpt generated information
"""

        user_prompt = f"""
If any errors or unverifiable parts are present in {answer}, print "F" and list those parts in bullet points.
example : [ F \n ・~~ \n ・~~ ...]
Otherwise, print “T”
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
        print(ai_response)

        if ai_response.startswith("F"):
            return ai_response

        elif ai_response.startswith("T"):
            return True

        else:
            raise ValueError("Unexpected response format from GPT-3.5. Please check the input and try again.")


# Usage example
goal = "Find the best programming language for a project"
task = "collecting information about programming languages"
user_intent = "to understand the benefits and drawbacks of each programming language"
answer = "Python is a popular, easy-to-use programming language."

checker = ReliabilityChecker(goal, task, user_intent)
result = checker.check(answer)

if result is True:
    print("The answer is reliable.")
else:
    print("The answer is not reliable:", result)