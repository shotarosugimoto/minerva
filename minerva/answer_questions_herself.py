from dotenv import load_dotenv
import os
import openai
import re

env_path = os.path.join(os.path.dirname(__file__), '../.env')
load_dotenv(env_path)
openai.api_key = os.environ.get("OPENAI_API_KEY")


class QuestionAnswerer:
    def __init__(self, goal, task, user_intent):
        self.goal = goal
        self.task = task
        self.user_intent = user_intent

    def answer_questions(self, questions, role):
        # Prepare input for ChatGPT API
        system_input = f"""
{self.goal} is what the user ultimately wants to accomplish.
Now you are doing the task that {self.task}
{self.user_intent} is user's intent, so  keep this request in mind when answering
"""

        assistant_prompt = f"""
1. ~~
2. ~~
3. ~~
4. ~~
...
"""

        user_prompt = f"""
Answer the {questions} following the instructions in {role}
Answer in the form of [1. ~ \n2. ~ \n...]
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
        print(ai_response)
        # Extract the answers from the AI response
        answers = re.findall(r'^\d+\.\s(.+)', ai_response, re.MULTILINE)

        return answers


# Usage example
goal = "Learn about Python libraries"
task = "answering questions about Python libraries"
user_intent = "to understand the most popular Python libraries and their use cases"
questions = "What are the top 5 Python libraries and their use cases?"
role = "expert"

answerer = QuestionAnswerer(goal, task, user_intent)
answers = answerer.answer_questions(questions, role)

print("Answers:")
for idx, answer in enumerate(answers, start=1):
    print(f"{idx}. {answer}")