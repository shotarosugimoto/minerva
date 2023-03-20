from dotenv import load_dotenv
import os
import openai
import re

env_path = os.path.join(os.path.dirname(__file__), '../.env')
load_dotenv(env_path)
openai.api_key = os.environ.get("OPENAI_API_KEY")


def enough_information(goal, task, user_intent, information):
    # Prepare input for ChatGPT API
    system_input = f"""
    {goal} is what the user ultimately wants to accomplish
    Now you are doing the task that {task}
    user_intent
    you have {information}
    """
    user_prompt = f"""
    If more information about {goal} is needed to {task}, print "1Q".
    If enough information about {goal} is available to {task}, print "1".
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
    if ai_response.strip() == "1":
        return True
    elif ai_response.strip() == "1Q":
        return False
    else:
        return "Error: Invalid response"


# 一番最初の時
goal = "新卒採用の戦略を作りたい"
task = f"create the best output outline to achieve {goal}"
information = "Users may seek to develop new channels and partnerships to reach a wider pool of high-quality candidates."

enough_information(goal, task)
