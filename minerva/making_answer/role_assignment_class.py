from dotenv import load_dotenv
import os
import openai
import re

env_path = os.path.join(os.path.dirname(__file__), '../../.env')
load_dotenv(env_path)
openai.api_key = os.environ.get("OPENAI_API_KEY")


def create_questions(goal, task, user_intent, questions):
    # Prepare input for ChatGPT API
    system_input = f"""
{goal} is what the user ultimately wants to accomplish.
Now you are doing the task that {task}
{user_intent} is user's intent, so  keep this request in mind when answering
{needed_info} is what you have to get information to perform the task that {task}.
"""
    assistant_prompt = f"""
1. As an ~
2. As an ~
3. As an ~
4. As an ~
...
"""

    user_prompt = f"""
## you are greatest manager
Add in what capacity the person should [task]
example: [1, As ~ n\ 2, As ~ ...]
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

# 必要な情報を定義します
goal = "Find the best programming language for a project"
task = "collecting information about programming languages"
user_intent = "to understand the benefits and drawbacks of each programming language"
information = "knowledge about various programming languages"
needed_information = ["popularity", "performance", "ease of use"]
tools = [
    ("GPT-3.5", "fast and accurate but can be expensive"),
    ("GPT-2", "less accurate but cheaper"),
    ("web scraping", "time-consuming and potentially inaccurate"),
    ("APIs", "quick and reliable but may have costs and usage limits")
]

# インスタンスを作成し、selectメソッドを呼び出す
selector = ToolSelector(goal, task, user_intent, information, needed_information, tools)
recommended_tools, tokens = selector.select()

# 結果を表示
print("Recommended tools:", recommended_tools)
print("Tokens used:", tokens)

"""
tools = [[name1, name1's description], [name2, name2's description], ...]
tools[0][1] == name1's description
"""
##使えるツールと、そのツールの説明

tools = [["gpt-3.5",\
          "Advantages:\
          Comprehensive knowledge on various topics.\
          Quick responses and 24/7 availability.\
          Multidisciplinary expertise.\
          Disadvantages:\
          Possibility of outdated information.\
          Misinterpretation or irrelevant answers.\
          Limited context and potential ethical concerns."],\
          ["user input",\
           "Advantages:\
           Better contextual understanding.\
           Relevant and targeted information.\
           Personalized guidance.\
           Improved rapport and communication.\
           Disadvantages:\
           Limited availability.\
           Restricted knowledge scope.\
           Risk of inaccurate or biased information.\
           Dependence, limiting problem-solving skills."]]

needed_information= ["Current state of the company's recruitment process",
 'Budget allocated for recruitment purposes',
 'Demographics and characteristics of the targeted candidates',
 "Competitors' recruitment strategies and strengths",
 'Unique selling points of the company to attract new graduates',
 'Availability of internal resources to support recruitment efforts',
 'Industry trends and best practices in new graduate recruitment ',
 'Past recruitment performance metrics, such as time-to-hire, cost-per-hire, and retention rates.']

goal = "新卒採用の戦略を作りたい"
task = f"Understand the organization's hiring needs and goals: What kind of candidates the organization is looking for? What are the organization's goals for hiring new graduates?"
information = ""
user_intent = "Users may seek to develop new channels and partnerships to reach a wider pool of high-quality candidates."

selector = ToolSelector(goal, task, user_intent, information, needed_information, tools)
recommended_tools, tokens = selector.select()

# 結果を表示
print("Recommended tools:", recommended_tools)
print("Tokens used:", tokens)
