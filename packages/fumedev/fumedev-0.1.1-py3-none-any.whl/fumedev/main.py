import os
import sys
import shutil
import subprocess
from pathlib import Path

import logging
from fumedev import env

env.FILE_FOLDER = os.path.dirname(os.path.abspath(__file__))
os.makedirs(env.USER_HOME_PATH.joinpath('FumeData'), exist_ok=True) 

# Get the FAISS logger and set its level to WARNING
logger = logging.getLogger('faiss')
logger.setLevel(logging.ERROR)

from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter

from dotenv import load_dotenv
from fumedev.agents.coderMinion import CoderMinion
from fumedev.auth.auth import login
from fumedev.lllm_utils.generate_search_phrases import generate_search_phrases
from fumedev.index.Documentation import Documentation
from fumedev.lllm_utils.if_changes_needed import if_changes_needed
from fumedev.lllm_utils.split_complex_task import split_complex_task
from fumedev.utils.create_diff import create_diff
from fumedev.utils.fliter_snippets_list import filter_snippets_list
from fumedev.utils.process_snippets import process_snippets
from fumedev.utils.find_closest_file_path import list_all_file_paths
from fumedev.utils.run_with_spinner import run_with_spinner



load_dotenv()
import inquirer
from rich import print
from rich.console import Console

from fumedev.utils.stream_message import stream_message
from fumedev.agents.philosopher import Philosopher

import logging
import warnings

logging.getLogger().setLevel(logging.ERROR)
warnings.filterwarnings("ignore")

login()

# Ask for the project path
project_path = os.getcwd()
env.PROJECT_PATH = project_path

# Define the destination directory
destination_dir = env.relative_path('./codebase')

console = Console()

# Create the destination directory if it does not exist
if not os.path.exists(destination_dir):
    os.makedirs(destination_dir)
else:
    for filename in os.listdir(destination_dir):
        file_path = os.path.join(destination_dir, filename)
        try:
            # If it is a file, delete it
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            # If it is a directory, delete it and all its contents
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print(f'Failed to delete {file_path}. Reason: {e}')

# Function to copy contents into an existing directory, excluding .git
def copy_to_existing_directory(source, destination):
    source_path = Path(source)
    destination_path = Path(destination)

    if not source_path.exists() or not destination_path.exists():
        raise ValueError("Source or destination directory does not exist.")

    for item in source_path.iterdir():
        if item.name == '.git':  # Skip the .git directory
            continue

        destination_item = destination_path / item.name
        try:
            if item.is_dir():
                shutil.copytree(item, destination_item, dirs_exist_ok=True)
            else:
                shutil.copy2(item, destination_item)
        except Exception as e:
            print(f"Error copying {item}: {e}")

def create_git(destination_path):
        # Initialize and commit using subprocess for better error handling
    try:
        subprocess.run(['git', '-C', str(destination_path), 'init'], check=True,stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.run(['git', '-C', str(destination_path), 'add', '.'], check=True,stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.run(['git', '-C', str(destination_path), 'commit', '-m', 'Initial commit'], check=True,stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except subprocess.CalledProcessError as e:
        print(f"Error during Git operations: {e}")
    

def run_documentation():
    dc = Documentation()
    dc.document()

def search_snippet(query, extension):
    doc = Documentation()
    snip_lst = doc.search_code(query=query, extension=extension, k=2)
    return snip_lst, [snip.get('file_path').replace('codebase/', '') for snip in snip_lst]

console = Console()

# Copy the project directory to the new location
# If the destination directory is empty, use copytree directly with exclusion
print('Reading the workspace...')
if not os.listdir(destination_dir):
    shutil.copytree(project_path, destination_dir, ignore=shutil.ignore_patterns('.git'), dirs_exist_ok=True)
    create_git(destination_dir)
else:
    # If destination directory exists and is not empty, copy contents manually excluding .git
    copy_to_existing_directory(project_path, destination_dir)
    create_git(destination_dir)
        
print(f"[blue]Welcome to FumeLX (BETA)[/blue]\nOpening up the workspace...\n")

os.system(f'ls {env.relative_path("./codebase")}')
print('\n')
    
workspace_onboarding = [
inquirer.List('confirmation',
                message="Is this the correct workspace?",
                choices=['Yes', 'No'],
                ),
]

answers = inquirer.prompt(workspace_onboarding)
confirmation = 'yes' in answers['confirmation'].lower()

if not confirmation:
    print('[bold red]Please cd to the directory you want to work on and try again[/bold red]')
    sys.exit()

stream_message("What are we working on today? You can write multiple lines. Markdown format is better. Press Enter + done + Enter to finish", speed=1.5)
task = ""
while True:
    line = input()
    if line == "done":
        break
    task += line + "\n"

globals()['TASK'] = task

def solve_task(task):
    run_with_spinner(function=run_documentation, message="Processing your codebase...(This may take 5-10 minutes the first time you are running Fume on a workspace)")
    
    phrases = run_with_spinner(generate_search_phrases, "Thinking of files to search", task)
    phrases_str = '\n- ' + '\n- '.join([obj.get('phrase') for obj in phrases])
    stream_message(phrases_str, speed=2)
    print('\n')

    snippets = []
    file_paths = []

    for phrase in phrases:

        query = phrase.get('phrase')
        extension = phrase.get('file_extension')

        doc = Documentation()
        snip_lst, files = run_with_spinner(search_snippet, f"Searching '{query}'", query, extension)

        snippets += snip_lst
        file_paths += files

    file_paths = list(set(file_paths))
    new_line = '\n'

    stream_message(f"Here are the files that I desiced to take a look at: ")

    questions = [
    inquirer.Checkbox('files', 
                        message="Please deselect the ones you think obviously are unrelated to the task (press the space bar to toggle)", 
                        choices=file_paths,
                        default=file_paths,  # All options selected by default
                    ),
                ]

    file_answers = inquirer.prompt(questions)
    file_paths = file_answers['files']

    stream_message('\nDo you want to add something to this list? (optional)')
    file_path_completer = WordCompleter(list_all_file_paths(), ignore_case=True)
    additional_phrases_str = prompt("Enter a a file path or description: ", completer=file_path_completer)
    additional_phrases = [phrase.strip() for phrase in additional_phrases_str.split(',')]

    extra_search_phrases = []
    new_paths = []

    for p in additional_phrases:
        if (os.path.exists(p) or os.path.exists(env.relative_path('./codebase/' + p))) and len(p) > 0:
            doc = Documentation()
            with open(env.relative_path('codebase/' + p)) as file:
                lines = file.readlines()
                lines = lines[:2300]
                code = ''.join(lines)
                snip = {'code': code, 'file_path': env.relative_path('codebase/' + p)}
                snippets.append(snip)

            file_paths.append(p)
            new_paths.append(p)
                
        else:
            extra_search_phrases.append(p)

    for phrase in extra_search_phrases:

        if not phrase:
            continue

        doc = Documentation()
        snip_lst, files = run_with_spinner(search_snippet, f"Searching '{phrase}'", phrase, None)

        snippets += snip_lst
        file_paths += files
        new_paths += files

    file_paths = list(set(file_paths))

    print('\n[bold]Updated list of files:[/bold]')

    for path in file_paths:
        if path in new_paths:
            print(f'[bold green]* {path}\n[/bold green]')
        else:
            print(f'* {path}\n')


    snippets = filter_snippets_list(snippets=snippets, file_paths=file_paths)     

    processed_snippets = process_snippets(snippets=snippets)

    didFinish = False
    future = ""
    diffs = []

    while not didFinish:
        ## REFACTOR THE DIFFS TO BE MORE ACCURATE
        phil = Philosopher(task=globals()['TASK'], snippets=processed_snippets, short_snippets=snippets, diffs=diffs)
            
        func = phil.generate_step
        res = run_with_spinner(func, "Thinking about what to do...", future)

        if res:
            action, future, file_paths, current_snippets = res


            aproved = False
            while not aproved:

                    
                plan_approval = [
                    inquirer.List('confirmation',
                    message="Does this plan look good to you?",
                    choices=['Yes', 'No'],
                    ),
                ]

                answers = inquirer.prompt(plan_approval)

                aproved = 'yes' in answers['confirmation'].lower()

                if not aproved:
                        
                    stream_message("Can you tell me what I should change about the plan? Press Enter + done + Enter to finish", speed=1.5)
                    feedback = ""
                    while True:
                        line = input()
                        if line == "done":
                            break
                        feedback += line + "\n"
                        
                    phil = Philosopher(task=globals()['TASK'], snippets=processed_snippets, short_snippets=snippets)

                    func = phil.apply_feedback
                    action ,future = run_with_spinner(func, "Thinking about what to do...", action,future ,file_paths , current_snippets)

            stream_message('I will continue with this plan', speed=1.5)
            changes = if_changes_needed(speech=action)
            decision = changes.get('decision')
            is_multiple = changes.get('is_multiple')
            if decision:
                if is_multiple:

                    old_files = []
                    for path in file_paths:
                        with open(path, 'r') as file:
                            old_files.append(file.read())

                    sub_tasks_dict = run_with_spinner(split_complex_task, 'Preparing the steps', action)
                    sub_tasks = sub_tasks_dict.get('sub_tasks')
                    for t in sub_tasks:
                            
                        task = '# ' + t.get('title') + '\n' + '* ' + '\n'.join(t.get('steps'))

                        coder = CoderMinion(task=task, file_paths=file_paths)
                        run_with_spinner(coder.code, 'Writing the code')

                    counter = 0
                    for path in file_paths:
                        with open(path, 'r') as file:
                            new_file = file.read()
                            diff = create_diff(old_content=old_files[counter], new_content=new_file)
                            diffs += (diff)
                else:
                    old_files = []
                    for path in file_paths:
                        with open(path, 'r') as file:
                            old_files.append(file.read())

                    # Assuming 'action' is defined elsewhere and appropriate for 'task'
                    coder = CoderMinion(task=action, file_paths=file_paths)
                    run_with_spinner(coder.code, 'Writing the code')
                        
                    counter = 0
                    for path in file_paths:
                        with open(path, 'r') as file:
                            new_file = file.read()
                            diff = create_diff(old_content=old_files[counter], new_content=new_file)
                            diffs += diff

            else:
                for path in file_paths:
                    diffs.append('# ' + path + '\n' + action)
        else:
            didFinish = True

            stream_message("What's next?", speed=1.5)
            new_task = ""
            while True:
                line = input()
                if line == "done":
                    break
                new_task += line + "\n"

            globals()['TASK'] = new_task
            solve_task(task=globals()['TASK'])  

solve_task(task=globals()['TASK'])        


def main():

    pass

if __name__ == "__main__":
    main()