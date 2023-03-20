from dotenv import load_dotenv
import os
import openai
import re

env_path = os.path.join(os.path.dirname(__file__), '../.env')
load_dotenv(env_path)
openai.api_key = os.environ.get("OPENAI_API_KEY")


class ToolSelector:
    def __init__(self, goal, task, user_intent, information, needed_information, tools):
        self.goal = goal
        self.task = task
        self.user_intent = user_intent
        self.information = information
        self.needed_information = needed_information
        self.tools = tools
        openai.api_key = os.environ['OPENAI_API_KEY']

    def select(self):
        available_tools = [tool[0] for tool in self.tools]
        available_tools_str = ", ".join(available_tools)

        tool_info_str = "".join([f"Advantage and disadvantage of {tool[0]} is {tool[1].strip()}.\n"
                                 for tool in self.tools])

        system_input = f"""
{self.goal} is what the user ultimately wants to accomplish.
Now you are doing the task that {self.task}
{self.user_intent} is user's intent, so  keep this request in mind when answering
You have {self.information}
{self.needed_information} is what you have to get information to perform the task that {self.task}.
you can use {available_tools_str}
{tool_info_str}
"""
        print(system_input)
        assistant_prompt = f"""
1. ~~
2. ~~
3. ~~
4. ~~
...
"""

        user_prompt = f"""
With reference to {tool_info_str},
Choose from {available_tools_str} which means you should use to get each information in {self.needed_information}.
If the method to get the first information is gpt-3.5, output as 1. gpt-3.5
"""

        messages = [
            {"role": "system", "content": system_input},
            {"role": "assistant", "content": assistant_prompt},
            {"role": "user", "content": user_prompt}
        ]

        response = openai.ChatCompletion.create(
            temperature=1,
            max_tokens=1000,
            model="gpt-3.5-turbo",
            messages=messages
        )

        ai_response = response['choices'][0]['message']['content']
        print(ai_response)
        tokens = response["usage"]["total_tokens"]
        # Extract the recommended tools from the AI response
        recommended_tools = re.findall(r'^\d+\.\s(.+)', ai_response, re.MULTILINE)

        # Check if the number of elements in needed_information matches the number of elements in recommended_tools
        if len(self.needed_information) == len(recommended_tools):
            return recommended_tools, tokens
        else:
            error_message = f"Error: The number of elements in needed_information ({len(self.needed_information)}) does not match the number of elements in recommended_tools ({len(recommended_tools)})."
            print(error_message)
            return self.needed_information, recommended_tools


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

#使えるツールと、そのツールの説明
tools = [["gpt-3.5",
          "Advantages:\
          Comprehensive knowledge on various topics.\
          Quick responses and 24/7 availability.\
          Multidisciplinary expertise.\
          Disadvantages:\
          Possibility of outdated information.\
          Misinterpretation or irrelevant answers.\
          Limited context and potential ethical concerns."],
          ["user input",
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