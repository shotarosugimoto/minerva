import openai
from minerva.making_answer.task_tree_element import TaskTreeElement


class EnoughInformation:

    def __init__(self, openai_api_key: str, goal: str, tree_element_list: list[TaskTreeElement],
                 processed_task_number: int):
        openai.api_key = openai_api_key
        # goal = "What the user wants to create with Minerva is" + initial_goal , "Minerva's output is used to" + initial_purpose
        if len(tree_element_list) == 1:
            information_prompt = tree_element_list[0].information
            print(f"tree_element_list[0].information = {tree_element_list[0].information}")

            self.system_input = f'''
            Your name is Minerva, and you're an AI that helps the user do their jobs.
            {goal}
            Now you are doing the task that create the best output outline to achieve {goal}
            {information_prompt}'''

            self.user_prompt = f'''
            If more information about {goal} is needed to create the best output outline to achieve {goal}, print "1Q".
            If enough information about {goal} is available to create the best output outline to achieve {goal}, print "1".
            Be sure to output only "iQ" or "1".
            Please do not write any other explanations, notes, or circumstances that led to the output.
            just write "iQ" or "1".'''

        else:
            current_task = tree_element_list[processed_task_number]
            parents_task: TaskTreeElement = current_task.parent
            children_task: list[TaskTreeElement] = parents_task.children

            # 何をしたいのかがよくわからないから保留
            self.system_input = f'''

            '''
            self.user_prompt = f'''
            If more information about {goal} is needed to {task}, print "1Q".
            If enough information about {goal} is available to {task}, print "1"
            Be sure to output only "iQ" or "1".
            Please do not write any other explanations, notes, or circumstances that led to the output.
            just write "iQ" or "1".'''

        self.messages = [
            {"role": "system", "content": self.system_input},
            {"role": "user", "content": self.user_prompt},
        ]

    def response_result(self):
        response = openai.ChatCompletion.create(
            temperature=1,
            max_tokens=1000,
            model="gpt-3.5-turbo",
            messages=self.messages
        )
        ai_response = response['choices'][0]['message']['content']
        if ai_response.strip() == "1":
            print("enough information")
            return True
        elif ai_response.strip() == "1Q":
            print("need more information")
            return False
        else:
            return "Error: Invalid response"
