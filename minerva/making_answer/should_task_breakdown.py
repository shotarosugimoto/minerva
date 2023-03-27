from minerva.making_answer.task_tree_element import TaskTreeElement
import openai


def should_task_breakdown(openai_api_key: str, goal: str, tree_element_list: list[TaskTreeElement],
                          processed_task_number: int):
    openai.api_key = openai_api_key

    criteria = '''
「assistantがステップに分けずに[task]の答えを出せる場合」
    ・ステップを踏まなくても、答えが出る場合
    ・ステップを踏んだとしても、ステップを踏まなかった場合と答えが変わらない場合
「assistantがステップを踏んだ方が、{task}を分解する方がいい場合」
    ・ステップを踏まないと答えが出ない場合
    ・ステップを踏んだ方が、ステップを踏まなかった時よりも、深く示唆深く正確な答えが出せる場合'''

    if len(tree_element_list) == 1:
        # 後々のために分けたけど今は書き分けしてないからかき分けて
        system_input = f'''
[goal]:最終的に解きたい課題です
[task]:現在解きたい課題です
[position]:現在、[goal]を解くうえで[task]が現在どこに位置しているのかを表しています
[user-intent]:[task]をassistantが解くときの、userからの要望
[info]:[task]を解くときに必要な情報です

goal: {goal}
task: {tree_element_list[processed_task_number]}
position: ゴールを{tree_element_list[processed_task_number].depth}分割した場所に位置しています
user-intent: {tree_element_list[processed_task_number].user_intent}
info: {tree_element_list[processed_task_number].information}'''

        assistant_prompt = ''''''

        user_prompt = f'''
現在、assistantが[info]を用いて[task]を解く段階です。
この時、assistantが[task]をステップに分けずに実行できるか、ステップに分けないと実行できないのか、{criteria}を参考にして判断してください。
「assistantがステップに分けずに[task]の答えを出せる場合」、'0'のみ出力してください。
「assistantがステップを踏んだ方が、[task]を分解する方がいい場合」、'1'のみ出力してください。
言語は書かず、数字のみ記載してください
数字のみの記載です。'''

    else:
        current_task = tree_element_list[processed_task_number]
        parents_task: TaskTreeElement = current_task.parent
        children_task: list[TaskTreeElement] = parents_task.children
        # 保留
        system_input = f'''
        [goal]:最終的に解きたい課題です
        [task]:現在解きたい課題です
        [position]:現在、[goal]を解くうえで[task]が現在どこに位置しているのかを表しています
        [user-intent]:[task]をassistantが解くときの、userからの要望
        [info]:[task]を解くときに必要な情報です

        goal: {goal}
        task: {tree_element_list[processed_task_number]}
        position: ゴールを{tree_element_list[processed_task_number].depth}分割した場所に位置しています
        user-intent: {tree_element_list[processed_task_number].user_intent}
        info: {tree_element_list[processed_task_number].information}'''

        assistant_prompt = '''
        「assistantがステップに分けずに[task]の答えを出せる場合」、0のみ出力してください。
        「assistantがステップを踏んだ方が、[task]を分解する方がいい場合」、1のみ出力してください。
        言語は書かず、数字のみ記載してください
        数字のみの記載です。'''

        user_prompt = f'''
        現在、assistantが[info]を用いて[task]を解く段階です。
        この時、assistantが[task]をステップに分けずに実行できるか、ステップに分けないと実行できないのか、{criteria}を参考にして判断してください。
        「assistantがステップに分けずに[task]の答えを出せる場合」、'0'のみ出力してください。
        「assistantがステップを踏んだ方が、[task]を分解する方がいい場合」、'1'のみ出力してください。
        言語は書かず、数字のみ記載してください
        数字のみの記載です。'''

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
    if ai_response == '0':
        return False
    return True
