from dotenv import load_dotenv
import os
import openai
import re

env_path = os.path.join(os.path.dirname(__file__), '../.env')
load_dotenv(env_path)
openai.api_key = os.environ.get("OPENAI_API_KEY")


def generate_hypotheses(goal, user_intent, information):
    system_input = f"""
    {goal} is what the user ultimately wants to accomplish
    you have {information}
    {user_intent} is user's intent, so  keep this request in mind when answering
    ##
    ensure that there is no discrepancy between what the user wants and what you are ultimately trying to accomplish.
    """
    assistant_prompt = f"""
    1. ~~
    2. ~~
    3. ~~
    4. ~~
    5. ~~
    """
    user_prompt = f"""
    make 5 hypotheses about the outputs that users are looking for, based on {goal}
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

    # Extract the hypotheses from the AI response
    hypotheses = re.findall(r'^\d+\.\s(.+)', ai_response, re.MULTILINE)

    # Check if the correct number of hypotheses were found
    if len(hypotheses) == 5:
        return hypotheses
    else:
        raise ValueError(f"Expected 5 hypotheses, but found {len(hypotheses)}")



