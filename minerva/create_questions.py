from dotenv import load_dotenv
import os
import openai
import re

env_path = os.path.join(os.path.dirname(__file__), '../.env')
load_dotenv(env_path)
openai.api_key = os.environ.get("OPENAI_API_KEY")


def create_questions(goal, task, user_intent, needed_info, source):
    # Prepare input for ChatGPT API
    system_input = f"""
{goal} is what the user ultimately wants to accomplish.
Now you are doing the task that {task}
{user_intent} is user's intent, so  keep this request in mind when answering
{needed_info} is what you have to get information to perform the task that {task}.
Your questions will be answered by {source}
"""
    assistant_prompt = f"""
Q1. ~~
Q2. ~~
Q3. ~~
Q4. ~~
...
"""

    user_prompt = f"""
Create questions for {source} to get the information in {needed_info}
Answer in the form of [Q1. ~ \nQ2. ~ \n].
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
    return ai_response


def sort_sources_by_tool(select_tools, needed_information):
    source_GPT = []
    source_USER = []

    for index, tool in enumerate(select_tools):
        if tool == 'gpt-3.5':
            source_GPT.append(needed_information[index])
        elif tool == 'user input':
            source_USER.append(needed_information[index])

    return source_GPT, source_USER


# どこから情報を取ってくるクラスなのかをtoolで指定する
needed_information = [
    "Current state of the company's recruitment process",
    'Budget allocated for recruitment purposes',
    'Demographics and characteristics of the targeted candidates',
    "Competitors' recruitment strategies and strengths",
    'Unique selling points of the company to attract new graduates',
    'Availability of internal resources to support recruitment efforts',
    'Industry trends and best practices in new graduate recruitment',
    'Past recruitment performance metrics, such as time-to-hire, cost-per-hire, and retention rates.',
]

select_tools = [
    'gpt-3.5',
    'user input',
    'user input',
    'gpt-3.5',
    'gpt-3.5',
    'gpt-3.5',
    'user input',
    'user input',
]

#情報を取ってくる手段を指定する
needed_info = source_GPT #source_USER
source = "chat-gpt" #"user"


goal = "新卒採用の戦略を作りたい"
task = f"Understand the organization's hiring needs and goals: What kind of candidates the organization is looking for? What are the organization's goals for hiring new graduates?"
information = "Users may seek to develop new channels and partnerships to reach a wider pool of high-quality candidates."

create_questions(goal, task, information, needed_info, source)