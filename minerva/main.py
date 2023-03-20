from dotenv import load_dotenv
import os
from decide_goal.decide_goal import DecideGoal

# APIKeyの取得
env_path = os.path.join(os.path.dirname(__file__), '../.env')
load_dotenv(env_path)
openai_api_key = os.environ.get("OPENAI_API_KEY")


# 最初のユーザーインプット
initial_goal = input('Write your goal(This is required):')
while 1:
    if initial_goal != '':
        break
    initial_goal = input('Write your goal(This is required):')

initial_information = input('Write your information:')


# decide_goalの処理
decide_goal = DecideGoal(openai_api_key=openai_api_key, goal=initial_goal, information=initial_information)
new_goal = decide_goal.redefine_goal()
