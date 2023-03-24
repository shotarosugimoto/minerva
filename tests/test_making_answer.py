from dotenv import load_dotenv
import os
from minerva.making_answer.making_answer import MakingAnswer

# APIKeyの取得
env_path = os.path.join(os.path.dirname(__file__), '../.env')
load_dotenv(env_path)
openai_api_key: str = os.environ.get("OPENAI_API_KEY")


new_goal = 'Users desire a reliable and safe car that can provide long-term security without extensive repairs or ' \
           'breakdowns. Additionally, some users prioritize fuel efficiency and eco-friendliness, ' \
           'while others prioritize specific technological features such as advanced infotainment systems, ' \
           'smartphone integration, high-quality sound systems, and ' \
           'driver-assistance features like backup cameras or parking sensors.'

making_answer = MakingAnswer(openai_api_key=openai_api_key, initial_goal=new_goal,
                             initial_information='')

processed_task_number: int = 0
step_number: int = 0

while 1:
    process_location = making_answer.task_process(processed_task_number=processed_task_number, step_number=step_number)
    processed_task_number = process_location[0]
    step_number = process_location[1]
    if process_location == 0 and step_number == 3:
        break

making_answer.print_final_answer()
