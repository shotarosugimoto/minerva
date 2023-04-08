from .create_outline import create_outline
from ..task_tree_element import TaskTreeElement


class CreateTask:

    def __init__(self, openai_api_key, goal, tree_element_list: list[TaskTreeElement],
                 processed_task_number: int):
        self.openai_api_key = openai_api_key
        self.goal = goal
        self.tree_element_list = tree_element_list
        self.processed_task_number = processed_task_number

    def create_task(self):
        selected_tasks = []
        while 1:
            outline_list = create_outline(openai_api_key=self.openai_api_key, goal=self.goal,
                                          tree_element_list=self.tree_element_list,
                                          processed_task_number=self.processed_task_number,
                                          selected_tasks = selected_tasks)
            print(f"確認用、リスト化後:{outline_list}")
            print(f'\nThe current task: {self.tree_element_list[self.processed_task_number].task}')
            print('These are the tasks into which the current task is divided.')
            print('The divided tasks:')
            for i in range(len(outline_list)):
                print(f'{i + 1}. {outline_list[i]}')

            user_input = input('1から作り直してほしい場合は "1" を入力してくださ\n'
                               'タスクを取捨選択したり、このまま行きたい場合は、Enterを押してください')
            if user_input == "1":
                continue

            print("-----select_tasks")
            selected_tasks = select_tasks(outline_list)

            user_input = input('満足している場合は "1"'
                               '\n追加の要望を入力して新しいタスクを生成したい場合は "2"')
            # 追加情報が入力されなかったら、サマライズに進む
            while user_input not in ['1', '2']:
                user_input = input('満足している場合は "1"'
                                   '\n追加の要望を入力して新しいタスクを生成したい場合は "2"')
            # 追加情報が入力されなかったら、サマライズに進む
            # 情報が入力されたら、選択された仮説と追加情報をuser intentに入れて新たに仮説を生成するループに戻る
            if user_input == "2":
                user_input = input('追加の要望を入力してください: ')
                self.tree_element_list[self.processed_task_number].user_intent = user_input

            elif user_input == "1":
                # 仮説が一つも選択されていなかったら、エラーを返し、最初から仮説を作り直す
                if not selected_tasks:
                    print('少なくとも1つは意図にあったタスクが出てくるまで情報をください')
                    continue
                else:
                    print("それでは、以下のタスクで進めます")
                    for i in range(len(selected_tasks)):
                        print(f'{i + 1}. {selected_tasks[i]}')
                    return selected_tasks
            continue


def select_tasks(outline_list):
    # ただ選択するだけじゃなくて、一つ一つに文句を言わせてほしい、いいんだけど...みたいなのあるから、
    # それを踏まえて、最初から作り直すのでもいいかもしれない
    selected_tasks = []
    print("意図に合うものを選択して下さい\nここで選択されなかった内容は破棄され、選択された内容をもとに最終的なアウトプットイメージを考えます")
    for num in range(len(outline_list)):
        print(f'{num + 1}. {outline_list[num]}')
        user_input = input('Enter 1 if you accept this hypothesis, 2 if you do not.')
        while user_input not in ['1', '2']:
            print('Invalid input. Please enter 1 if you accept this hypothesis, 2 if you do not.')
            user_input = input()
        if user_input == '1':
            selected_tasks.append(outline_list[num])
    return selected_tasks
