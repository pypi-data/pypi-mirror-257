import os
from pathlib import Path
USER_HOME_PATH = Path.home()
BASE_MODEL = 'gpt-4-0125-preview'
PROJECT_PATH = "../codebase"
EXCLUDE_DIRS = '__pycache__,.git,.idea,.vscode,node_modules,venv,build,dist,env,lib,bin,logs,log'
EXCLUDE_FILES = 'LICENSE,README.md,.gitignore,.DS_Store,.env,.env.example,.gitattributes,.gitmodules,.gitkeep,.git,package-lock.json,package.json,requirements.txt,setup.cfg,pyproject.toml,poetry.lock,poetry.toml'
EXCLUDE_FOLDERS = ['env', 'node_modules', 'cache']
NONTRVIVIAL_FILES = ['js', 'html', 'py', 'css', 'go', 'java', 'ts', 'tsx', 'c', 'cpp', 'cs', 'php', 'rb', 'rs', 'swift', 'pug']
OPENAI_API_KEY = ''
FILE_FOLDER = ''


def relative_path(path):
    file_path = str(USER_HOME_PATH) + '/FumeData/' + path
    print(file_path)
    return file_path
from pathlib import Path

def parse_gitignore():
    project_path = Path(PROJECT_PATH)  # Leveraging the existing PROJECT_PATH variable
    gitignore_path = project_path / '.gitignore'  # Constructing the full path to .gitignore
    global EXCLUDE_FILES, EXCLUDE_DIRS  # To modify the global variables

    if gitignore_path.exists():
        with gitignore_path.open('r') as f:
            for line in f:
                stripped_line = line.strip()
                # Ignoring empty lines and comments
                if stripped_line and not stripped_line.startswith('#'):
                    if stripped_line.endswith('/'):
                        # It's a directory, excluding the trailing slash for consistency
                        EXCLUDE_DIRS += ',' + stripped_line[:-1]
                    else:
                        # It's a file
                        EXCLUDE_FILES += ',' + stripped_line
    else:
        print("Warning: .gitignore file not found at", gitignore_path)
