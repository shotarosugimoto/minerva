from ..task_tree_element import TaskTreeElement
import openai

from ...token_class import Token


def create_questions(openai_api_key: str, goal: str, now_task_element: TaskTreeElement,
                     tree_element_list: list[TaskTreeElement],
                     processed_task_number: int, needed_information_list: list[str]):

    openai.api_key = openai_api_key
    if len(tree_element_list) == 1:
        system_input = f'''
        Your name is Minerva, and you're an AI that helps the user do their jobs.
        <Definition>
        [goal] = {goal}
        [current task] = Divide into the rough steps to complete the document as defined by the user's [goal].
        [owned information] = {tree_element_list[0].information}
        [needed information list] = {needed_information_list}
        Now you are doing [current task].
        [owned information] is information that Minerva already has.
        [needed information list] is needed to solve [current task] other than [owned information].
        <Description>
        The Minerva system consists of several AIs.
        Each AI is required to fulfill a given role. 
        You are assigned the role of "create question to get [needed information list]".
        # output lang: jp
        '''

        user_prompt = f'''
        According to instructions, let's work this out in a step by step way to be sure we have the right answer.
        <note>
        # Understand the Description and your role and have clear your responsibility.
        #　keep the questions you list to a minimum.
        <Instruction>
        Create question to get the [needed information list].
        <constraints>
        Delete unnecessary questions for [current task].
        Delete questions that can be answered with information in [owned information] and [goal].
        Never create a question that will get the same answer.
        # output lang: jp
        # output style: [1. ~ \n2. ~ \n...]
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
        <Definition>
        [goal] = {goal}
        [current task] = {current_task.task}
        [parent task] = {parents_task.task}
        [owned information] = {all_information}
        [same layer task and answer] = {task_and_answer_prompt}
        Now you are doing [current task].
        [parent task] is divided into [same layer task and answer].
        [owned information] is information that Minerva already has.
        [needed information list] is needed to solve [current task] other than [owned information].
        <Description>
        The Minerva system consists of several AIs.
        Each AI is required to fulfill a given role. 
        You are assigned the role of "create questions to get [needed information list]".
        # output lang: jp
        '''

        user_prompt = f'''
        According to instructions, let's work this out in a step by step way to be sure we have the right answer.
        <note>
        # Understand the Description and your role and have clear your responsibility.
        #　keep the questions you list to a minimum.
        <Instruction>
        Create question to get the [needed information list].
        <constraints>
        Delete unnecessary questions for [current task].
        Delete questions that can be answered with information in [owned information] and [goal].
        Delete questions related to tasks in [same layer task and answer].
        Never create a question that will get the same answer.
        # output lang: jp
        # output style: [1. ~ \n2. ~ \n...]
        '''

    assistant_prompt = '''
    1. ~~
    ...
    '''

    messages = [
        {"role": "system", "content": system_input},
        {"role": "assistant", "content": assistant_prompt},
        {"role": "user", "content": user_prompt}
    ]

    # Call the ChatCompletion API
    response = openai.ChatCompletion.create(
        temperature=0,
        max_tokens=1000,
        model="gpt-3.5-turbo",
        messages=messages
    )
    # トークン数のアウトプットの処理
    token = response["usage"]["total_tokens"]
    # print(f'usage tokens:{token}')
    use_token = Token(token)
    use_token.output_token_information('create_questions')

    ai_response = response['choices'][0]['message']['content']
    return ai_response



