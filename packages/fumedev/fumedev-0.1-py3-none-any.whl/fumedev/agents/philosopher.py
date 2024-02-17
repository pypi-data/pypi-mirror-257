import json
from openai import OpenAI
from fumedev.prompts import philosopher_apply_feedback_prompt_1, philosopher_apply_feedback_system_prompt, philosopher_generate_step_system_prompt, philosopher_generate_step_user_prompt_1, philosopher_generate_step_user_prompt_2, philosopher_generate_step_user_prompt_3
from fumedev import env
from fumedev.agents.agent import Agent
from fumedev.utils.find_closest_file_path import find_closest_file_path

class Philosopher (Agent):
    def __init__ (self, task, snippets=[], diffs=[], short_snippets=[]):
        super().__init__()
        self.messages = []
        self.task = task
        self.snippets = snippets
        self.diffs = diffs
        self.short_snippets = short_snippets
        self.client = OpenAI(api_key=env.OPENAI_API_KEY)
        self.tools = []
        

    def generate_step(self, future_thought):
        diff_str = '\n'.join(self.diffs)
        self.messages = [{"role": "system", "content": philosopher_generate_step_system_prompt(diff_str=diff_str, file_paths_str=self._format_files_str(snippets=self.short_snippets))},
                         {"role": "user", "content": philosopher_generate_step_user_prompt_1(task=self.task, future_thought=future_thought)}]
        
        self.tools = [{
                        "type": "function",
                        "function": {
                            "name": "select_file",
                            "description": "Call this function when you want to select a file to make changes on it. As a result, you will be given the relevant snippets inside this file.",
                            "parameters": {
                                "type": "object",
                                "properties": {
                                    "file_path": {
                                        "type": "string",
                                        "description": "The exact file path you want to select",
                                    },
                                },
                                "required": ["file_path"],
                            },
                        },
                    },
                    {
                        "type": "function",
                        "function": {
                            "name": "done",
                            "description": "Call this function when you are sure you have covered all of necessary steps and completed the entirety of the task. He does not know anything about your current progress. He does not have memory of your previous questions or your actions.",
                            "parameters": {
                                "type": "object",
                                "properties": {
                                    "confidence": {
                                        "type": "string",
                                        "description": "How confident are you with your respone out of 10?",
                                    },
                                },
                                "required": ["confidence"],
                            },
                        },
                    },
                ]
        
        response = self.client.chat.completions.create(
            model=env.BASE_MODEL,
            messages=self.messages,
            tools=self.tools
        )

        response_message = response.choices[0].message
        self.messages.append(response_message)
        tool_calls = response_message.tool_calls

        while True:
            didSelectFile = False
            file_paths = []
            selected_snippets = []
            if tool_calls:
                for tool_call in tool_calls:
                    function_name = tool_call.function.name
                    args = json.loads(tool_call.function.arguments)

                    if function_name == 'select_file':
                        file_path = find_closest_file_path(args['file_path'])
                        file_paths.append(file_path)
                        print(f"\nLooking at {file_path}")
                        snip_str = self._format_snippets_str(self.snippets, file_path=file_path)
                        self.messages.append({'role': 'tool', 'tool_call_id': tool_call.id, 'name': function_name,'content': snip_str})
                        selected_snippets.append({'file_path': file_path, 'code': snip_str})
                        didSelectFile = True
                      
                    elif function_name == 'done':
                        print('I decided that the task is complete.')
                        return False
                    else:
                        print('Unknown tool call. Terminating the proccess. Please try again')
                        return False
                
                if didSelectFile:
                    self.messages.append({'role': 'user', 'content': philosopher_generate_step_user_prompt_2()})
                    stream = self.client.chat.completions.create(
                        model=env.BASE_MODEL,
                        messages=self.messages,
                        stream=True,
                    )
                    collected_messages = []
                    for chunk in stream:
                        if chunk.choices[0].delta.content is not None:
                            chunk_message = chunk.choices[0].delta.content  # extract the message
                            collected_messages.append(chunk_message) 
                            print(chunk_message, end="")

                    collected_messages = [m for m in collected_messages if m is not None]
                    full_reply_content = ''.join([m for m in collected_messages])

                    self.messages.append({'role': 'assistant', 'content': full_reply_content})
                    self.messages.append({'role': 'user', 'content': philosopher_generate_step_user_prompt_3()})

                    response = self.client.chat.completions.create(
                        model=env.BASE_MODEL,
                        messages=self.messages,
                    )

                    response_message = response.choices[0].message
                    future = response_message.content

                    return full_reply_content, future, file_paths , selected_snippets
            else:
                response_message = response.choices[0].message
                self.messages.append(response_message)
                tool_calls = response_message.tool_calls


    def apply_feedback(self , action, feedback ,file_path, current_snippets):
        self.tools = []
        
        #@TODO parse the current snippets list in to a string
        self.messages = [{"role": "system", "content": philosopher_apply_feedback_system_prompt('')},
                         {"role": "user", "content": philosopher_apply_feedback_prompt_1(task=self.task, action=action, feedback=feedback, snippets_str=self._format_all_snippets_str(current_snippets))}]
        
        stream = self.client.chat.completions.create(
            model=env.BASE_MODEL,
            messages=self.messages,
            stream=True,
        )
        collected_messages = []
        for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                chunk_message = chunk.choices[0].delta.content  # extract the message
                collected_messages.append(chunk_message) 
                print(chunk_message, end="")

        collected_messages = [m for m in collected_messages if m is not None]
        full_reply_content = ''.join([m for m in collected_messages])

        self.messages.append({'role': 'assistant', 'content': full_reply_content})
        self.messages.append({'role': 'user', 'content': philosopher_generate_step_user_prompt_3()})

        response = self.client.chat.completions.create(
            model=env.BASE_MODEL,
            messages=self.messages,
            )


        response_message = response.choices[0].message
        future = response_message.content

        return full_reply_content, future


    def _format_snippets_str(self, snippets, file_path=None):
        res = ""
        if file_path:
            for s in snippets:
                if s.get('file_path') == file_path:
                    if not res:
                        res = f"# {file_path}\n{s.get('code')}"
                    else:
                        pass
            
            return res
        else:
            return "Error: No File Path Provided"
        
    def _format_all_snippets_str(self, snippets):
        res = ""
        for s in snippets:
            res += f"## {s.get('file_path')}\n{s.get('code')}\n\n"
        return res
        
    def _format_files_str(self, snippets):
        res = ""
        files = [s.get('file_path') for s in snippets]

        for file in files:
            res += '\n\n' + self._format_snippets_str(snippets, file)

        return res
    
        