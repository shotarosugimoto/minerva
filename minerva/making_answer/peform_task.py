from dotenv import load_dotenv
import os
import openai
import re

env_path = os.path.join(os.path.dirname(__file__), '../../.env')
load_dotenv(env_path)
openai.api_key = os.environ.get("OPENAI_API_KEY")


def peform_task(goal, task, user_intent, information):
    # Prepare input for ChatGPT API
    system_input = f"""
    {goal} is what the user ultimately wants to accomplish
    Now you are doing the task that {task}
    {user_intent} is user's intent, so  keep this request in mind when answering
    you have {information}
    """
    assistant_prompt = f"""
    1. ~~
    2. ~~
    3. ~~
    4. ~~
    ...
    """

    user_prompt = f"""
    peform {task}
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

    # Extract the output from the AI response
    output = re.findall(r'^\d+\.\s(.+)', ai_response, re.MULTILINE)

    return output


goal = "新卒採用の戦略を作りたい"
task = f"create the best output outline to achieve {goal}"
information = "Users may seek to develop new channels and partnerships to reach a wider pool of high-quality candidates."
peform_task(goal, task, information)