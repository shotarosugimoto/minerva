from dotenv import load_dotenv
import os
from decide_goal.decide_goal import DecideGoal
from making_answer.making_answer import MakingAnswer

# APIKeyの取得
env_path = os.path.join(os.path.dirname(__file__), '../.env')
load_dotenv(env_path)
openai_api_key: str = os.environ.get("OPENAI_API_KEY")


# 最初のユーザーインプット
initial_goal: str = input('Write your goal(This is required):')
while 1:
    if initial_goal != '':
        break
    initial_goal = input('Write your goal(This is required):')

initial_information: str = input('Write your information:')

# decide_goalの処理
decide_goal = DecideGoal(openai_api_key=openai_api_key, goal=initial_goal, information=initial_information)
new_goal = decide_goal.redefine_goal()

making_answer = MakingAnswer(openai_api_key=openai_api_key, initial_goal=new_goal,
                             initial_information=initial_information)

processed_task_number: int = 0
step_number: int = 0

while 1:
    process_location = making_answer.task_process(processed_task_number=processed_task_number, step_number=step_number)
    processed_task_number = process_location[0]
    step_number = process_location[1]
    if process_location == 0 and step_number == 3:
        break

making_answer.print_final_answer()

