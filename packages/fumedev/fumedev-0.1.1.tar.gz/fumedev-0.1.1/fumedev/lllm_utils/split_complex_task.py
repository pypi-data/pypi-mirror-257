import json

from openai import OpenAI
from fumedev import env

from fumedev.prompts import split_complex_task_system, split_complex_task_user

def split_complex_task(task):
        messages = [
            {'role': 'system', 'content': split_complex_task_system()},
            {'role': 'user', 'content': split_complex_task_user(task=task)}
        ]

        client = OpenAI(api_key=env.OPENAI_API_KEY)
        response = client.chat.completions.create(
            model=env.BASE_MODEL,
            messages=messages,
            response_format={"type": "json_object"},
        )

        return json.loads(response.choices[0].message.content)