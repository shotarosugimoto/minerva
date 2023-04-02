from minerva.making_answer.task_tree_element import TaskTreeElement
import openai

from minerva.token_class import Token


def should_task_breakdown(openai_api_key: str, goal: str, tree_element_list: list[TaskTreeElement],
                          processed_task_number: int):
    openai.api_key = openai_api_key

    criteria = '''
    Decision Criteria
    ・When it is considered that Minerva can perform the task without decomposing the task.
    ・If Minerva's answer is considered to be the same even if the task is decomposed as if the task is not decomposed.
    →Do not decompose the task, but perform the current task.
    ・If Minerva cannot complete the task without decomposing the task
    ・If Minerva is able to give a more suggestive and accurate answer when the task is broken down than when the task 
    is not broken down
    →Decompose the task
    '''

    if len(tree_element_list) == 1:
        system_input = f'''
    Your name is Minerva, and you're an AI that helps the user do their jobs.
    [goal] = {goal}
    [current task] = create the best output outline to achieve [goal]
    [Owned information] = {tree_element_list[0].information}
    [user intent] = {tree_element_list[0].user_intent}
    Keep in mind [goal].
    Now you are doing [current task].
    [Owned information] is information that is needed and available for reference when solving [current task].
    [user intent] is user\'s intent, so keep this request in mind when answering.
    Currently, [current task] is divided {tree_element_list[processed_task_number].depth} times from the final output.
            '''
    else:
        current_task = tree_element_list[processed_task_number]
        parents_task = current_task.parent
        children_task_list = parents_task.children
        all_information = ''
        task_and_answer_prompt = ''
        all_information += current_task.information + ', '
        all_information += parents_task.information + ', '
        for element in children_task_list:
            all_information += element.information + ', '
            if element.answer:
                task_and_answer_prompt += f'task:{element.task}, answer:{element.answer}'
            else:
                task_and_answer_prompt += f'task:{element.task}, answer: not yet, '

        system_input = f'''
    Your name is Minerva, and you're an AI that helps the user do their jobs.
    [goal] = {goal}
    [current task] = {tree_element_list[processed_task_number].task}
    [owned information] = {all_information}
    [user intent] = {parents_task.user_intent}
    Keep in mind [goal].
    Now you are doing [current task].
    [owned information] is information that is needed and available for reference when solving [current task].
    [user intent] is user\'s intent, so keep this request in mind when answering.
    {task_and_answer_prompt} are tasks and their answers on the same layer as [current task]
    , which are decomposed tasks to solve {parents_task.task}.
    Currently, [current task] is divided {tree_element_list[processed_task_number].depth} times from the final output.
        '''
        print(f"system_input: {system_input}")
    assistant_prompt = '''
    0
        '''

    user_prompt = f'''
    Determine whether Minerva can execute [current task] without decomposing it or without decomposing it with reference 
    to {criteria}.
    If Minerva does not need to decompose [current task], output only '0'.
    If Minerva should decompose [current task], please output only '1'.
    Please do not write the language, only numbers.
    Only numbers are written.'''

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

    # トークンアウトプットの処理
    token = response["usage"]["total_tokens"]
    print(f'usage tokens:{token}')
    use_token = Token(token)
    use_token.output_token_information('should_task_breakdown')

    print(ai_response)
    if ai_response == '0':
        return False
    elif ai_response == '1':
        return True
    else:
        raise ValueError(f"0、1以外の回答が返ってきました")
