import os

class Agent:
    def __init__(self) -> None:
        self.total_tokens = 0
        self.messages = []

        summary_exists = os.path.isfile('./summary.md')
        if summary_exists:
            with open('./summary.md', 'r') as file:
                self.project_summary = file.read()
        else:
            self.project_summary = ''
    
    def print_token_count(self,response):

        token_count = response.usage.total_tokens
        self.total_tokens += token_count
        agent = self.__class__.__name__
        print(f"Tokens use by {agent} Agent for this call: {token_count}\nTotal tokens used by {agent} Agent: {self.total_tokens}")
        




        
