from ..task_tree_element import TaskTreeElement
import openai

from ...token_class import Token


def select_tool(openai_api_key: str, goal: str, now_task_element: TaskTreeElement, needed_information: list[str],
                questions: list[str]):
    openai.api_key = openai_api_key

    loop_num = 0

    while True:
        tools = []
        for question in questions:
            tool_character = '''
            <gpt-3.5>
            Advantages: Comprehensive knowledge on various topics, Multidisciplinary expertise
            Disadvantages: Possibility of outdated information, Misinterpretation or irrelevant answers, Limited context and potential ethical concerns
            note: gpt-3.5 can answer questions that can be answered with information you already have, such as [owned information]
            <user input>
            Advantages: Better contextual understanding, Relevant and targeted information, Personalized guidance, Improved rapport and communication.
            Disadvantages: Limited availability, Restricted knowledge scope, Risk of inaccurate or biased information, Dependence, limiting problem-solving skills
            '''

            if now_task_element.information != '':
                system_input = f'''
                Your name is Minerva, and you're an AI that helps the user do their jobs.
                <Definition>
                [goal] = {goal}
                [current task] = {now_task_element.task}
                [owned information] = {now_task_element.information}
                [needed information] = {needed_information}
                [question] = {question}
                [tool character] = {tool_character}
                Now you are doing [current task].
                [owned information] is information that Minerva already has.
                [needed information] is needed to solve [current task] other than [owned information].
                [question] is one of the questions to get [needed information].
                [tool character] is a description of the tools from which the information can currently be retrieved.
                <Description>
                The Minerva system consists of several AIs.
                Each AI is required to fulfill a given role. 
                You are assigned the role of "Determine which tools to use to acquire [needed information]".
                '''

            # informationが空の時
            else:
                system_input = f'''
                Your name is Minerva, and you're an AI that helps the user do their jobs.
                <Definition>
                [goal] = {goal}
                [current task] = {now_task_element.task}
                [needed information] = {needed_information}
                [question] = {question}
                [tool character] = {tool_character}
                Now you are doing [current task].
                [needed information] is needed to solve [current task].
                [question] is one of the questions to get [needed information].
                [tool character] describes the advantages and disadvantages of each tool.
                <Description>
                The Minerva system consists of several AIs.
                Each AI is required to fulfill a given role.    
                You are assigned the role of "Determine which tools to use to acquire [needed information]".
                '''

            user_prompt = f'''
            According to instructions, let's work this out in a step by step way to be sure we have the right answer.
            Output only the final result.
            <note>
            # Refer to [tool character] for a better understanding of the tool
            # Keep in mind [needed information] is needed to solve [current task]
            <Instruction>
            If [question] should be asked to the user, output only "U".
            If [question] should be asked to GPT-3.5", output only "G".
            <constraints>
            Always ask the user if user-specific information is needed, not generalities.
            Be sure to output only "U" or "G".
            Do not write any other explanations, notes, or circumstances that led to the output.
            just write "U" or "G"."""
            '''

            messages = [
                {"role": "system", "content": system_input},
                {"role": "user", "content": user_prompt}
            ]
            response = openai.ChatCompletion.create(
                temperature=0,
                max_tokens=1000,
                model="gpt-3.5-turbo",
                messages=messages
            )
            ai_response = response['choices'][0]['message']['content']
            print(f"question: {question}, tool: {ai_response}")
            if "G" in ai_response:
                tools.append("G")
            if "U" in ai_response:
                tools.append("U")
            # トークン数のアウトプットの処理
            token = response["usage"]["total_tokens"]
            # print(f'usage tokens:{token}')
            use_token = Token(token)
            use_token.output_token_information('select_tool')

        loop_num += 1
        if len(tools) == len(questions):
            return tools

        elif loop_num == 3:
            print("大変申し訳ございません。"
                  "未熟者のため、タスクをこなすことができませんでした。")
            break
        else:
            print("ごめんなさい。ツールの選択を上手くできなかったので"
                  "もう一度ツール選択をさせていただきます。"
                  "少々お待ちください...")
            continue
