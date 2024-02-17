import json

from openai import OpenAI

from fumedev import env

from fumedev.prompts import generate_search_phrases_system, generate_search_phrases_user
from fumedev.utils.get_dir_structure import get_dir_structure_bfs
from fumedev.utils.get_unique_extensions import get_unique_extensions

def generate_search_phrases(task):
        
        extensions = get_unique_extensions(env.relative_path('./codebase'))

        extension_str = ''
        for ext in extensions:
            extension_str += f"- {ext}\n"
        
        system_prompt = generate_search_phrases_system(task, get_dir_structure_bfs())

        messages = [
            {'role': 'system', 'content': system_prompt},
            {'role': 'user', 'content': generate_search_phrases_user()}
        ]

        client = OpenAI(api_key=env.OPENAI_API_KEY)
        response = client.chat.completions.create(
            model=env.BASE_MODEL,
            messages=messages,
            response_format={"type": "json_object"},
        )

        return json.loads(response.choices[0].message.content)['search']