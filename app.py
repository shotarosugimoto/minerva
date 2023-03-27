import sys
sys.path.append('/Users/tasuku/SALT2/minerva')

from flask import Flask, render_template, request
from dotenv import load_dotenv
import os
from decide_goal.decide_goal import DecideGoal
from making_answer.making_answer import MakingAnswer

app = Flask(__name__)

# APIKeyの取得
env_path = os.path.join(os.path.dirname(__file__), '../.env')
load_dotenv(env_path)
openai_api_key: str = os.environ.get("OPENAI_API_KEY")

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        initial_goal = request.form['initial_goal']
        initial_information = request.form['initial_information']

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

        # decide_goal関数から返された値を取得
        decision = making_answer.get_decision()
        task_description = making_answer.get_task_description()

        return render_template('result.html', decision=decision, task_description=task_description)

    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
