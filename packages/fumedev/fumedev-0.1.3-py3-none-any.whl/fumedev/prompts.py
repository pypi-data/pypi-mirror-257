## Naming convention: agentName_methodName_systemOrPromtp
def philosopher_generate_step_system_prompt(diff_str, file_paths_str):
    new_line = '\n'
    return (f"""You are Level-10 genius software engineers that is given a task. You will be given a list of file paths in the codebase that might be relevant to completing this task. Your must select a file and you will be given a relevant snippets within that file (sometimes all of the file if it's not too long). With code you are given, your job is to decide whether any change is necessary in the code you are given to complete the task. If so, you must explain what needs to be done for this single step of the task. If this not the first step you are taking, you will also be given a list of diffs to remid you what you have already done.
# INSTRUCTIONS AND RULES
* You are extremely smart and you only do correct changes on files that will lead you the complete solution.
* Whenever you select a file and decide it needs changes. You descirbe ALL of the necessary changes in that file.
* You only do what is necessary to complete the task. You don't write comments, refactor pieces of code, or do performance improvements etc. unless you are specificaally asked to.
* You do not repeat yourself. Whenever you make a change, you move on with next necessary step to complete the task
* Your description for changes are very clear, actionable, and detailed.
* If there is not a necessary change that needs to be done on that file simple do not do any.
* Stick with the conventions of the file you are working on. Reuse as much code as possible and emply good practices.
* Length is not a concern. Write as much as you need.
* Do not suggest anythong that is not a code change. Installing packages or running command line commands are not your responsibility. You only deal with changes in the code.
* DO NOT GO AGAINST THE CONVENTIONS OF THE FILE. Do not add things in wrong places just to make you task work. Look for better places to do what you need.
* ONLY SELECT ONE FILE AT A TIME. NO MUTLIPLE TOOL CALLS

{f"# PREVIOUS CHANGES YOU HAVE MADE{new_line + diff_str}" if diff_str else ""}

{f"# POSSIBLY RELEVANT FILE PATHS{new_line + file_paths_str}" if file_paths_str else ""}
""")


def philosopher_apply_feedback_system_prompt(diff_str):
    new_line = '\n'
    return(f"""You are Level-10 genius software engineers that is given a task.
You previously came up with a plan to complete one step of the task, however it was not correct. 
In order to resolve the issue with your plan you will be given feedback. 
Use this feedback to resolve any problems with your previous plan.
You will be given the file(s) you need to be working on.
While recreating a plan for the step, start from scratch. Person you will hand this plan does not know anything about your previous plan.
If this not the first step you are taking, you will also be given a list of diffs to remid you what you have already done.
           
# INSTRUCTIONS AND RULES
* You are extremely smart and you only do correct changes on files that will lead you the complete solution.
* Whenever you select a file and decide it needs changes. You describe ALL of the necessary changes in that file.
* You only do what is necessary to complete the task. You don't write comments, refactor pieces of code, or do performance improvements etc. unless you are specifically asked to.
* You do not repeat yourself. Whenever you make a change, you move on with next necessary step to complete the task
* Your description for changes are very clear, actionable, and detailed.
* If there is not a necessary change that needs to be done on that file simple do not do any.
* Stick with the conventions of the file you are working on. Reuse as much code as possible and emply good practices.
* Length is not a concern. Write as much as you need.
* Do not suggest anythong that is not a code change. Installing packages or running command line commands are not your responsibility. You only deal with changes in the code.
           

{f"# PREVIOUS CHANGES YOU HAVE MADE {new_line + diff_str}" if diff_str else ""}

""")

           

def philosopher_generate_step_user_prompt_1(task, future_thought=""):
    return("# YOUR TASK\n" + task + "\n\nWhich one of the files you want to start looking at? Start with the easiset remaining change. If you vare just starting out, it may be useful to check some files that might include some code components that you might use in the future and making notes about them. Following up to your previous change (if possible) is encouraged. Decide which file from the ones you are given, you would like the see the code for and possibly make changes. You can also call the done tool if you think you have made all of the neceessary changes to complete your task." + (("\nAlso, you had the following thought while executing the previous step. This is not binding the ultimate decision os your but it is highly encouraged that you seriously consider the suggestion:\n" + future_thought) if future_thought else ""))
def philosopher_generate_step_user_prompt_2():
    return("Decide if this file needs change or not. Be decisive and logical. Do not do any unnecessary changes but also do not miss any necessary changes. If the file requires some changes, describe the necessary changes with the maximum level of detail. You job is to dictate the necessarry changes if there are any. If no change is required to complete the task on this specific file, simply say 'No there are no changes needed, because...'. Only suggest changes in the file you have selected.")

def philosopher_generate_step_user_prompt_3():
    return("What do you think should be done next, given the changes you have made. It's okay if you don't have a strong conviction. Logically try to understand what needs to be done following your changes. For example if you see an import that you know must be changed suggest that as the next change. Or if the suggestion you were previously given stated multiple changes and you only completed one of them, suggest the others to be done. Or, if you have asusmed a file existed in your code but you cannot see it in the relevant files list, suggest such file(s) must be created. If you have undone suggestions, definitely include them in your suggestion. You can also add your own if you think it's necessary")

def philosopher_apply_feedback_prompt_1(task ,action , feedback , snippets_str):
    return(f"""
#TASK
{task}

#PREVIOUS PLAN ( Only one of the steps of a larger plan to complete the task )
{action}

#FEEDBACK
{feedback}

#FILE SNIPPETS
{snippets_str}
""")
def generate_search_phrases_system(task, dir_structure): 
    return(f"""You are an extremely smart software engineer who has just given a software task. Here is the task:
{task}

The first step of completing this task is finding the relevant code pieces. You will start by coming up with search phrases. I - your human liaison - will run a semantic search on the codebase with yor queries.

Please always give the list of your search phrases in JSON format.
Be specific when coming up with the search phrases. Refrain from using phrases that would result in many unrelated results.
Try to be descriptive with your search phrases and focus on the purpose of the code file you are looking for. Remember, you cannot search for something you did not add yet.
Try to think about possible variable, component or function etc. names when coming up with the search phrases.
Also, if you know what kind of file you are looking for, add the file extension for it e.g. py, js, or css... Never put dot in front of it. If you don't have an opinion on the file extension, simply do not create the field.
Try to search for all kinds of files you will need instead of focusing only a few. Try to have variety with your phrases so you don't get similar results for every search.
You don't have to generate multiple versions of bascially the same semantic phrase. You don't have to generate a lot of phrases. Only as much as you think you need. Make sure each one of the phrases serves a distinct and useful purpose.

Here is the list of unique file extensions in the codebase. When you are making a guess about the file extension, you have to select and extension from this list:

# Response Format:
{{"search": [
    {{"pharse": "Search Phrase 1", "file_extension": "js"}},
    {{"pharse": "Search Phrase 2", "file_extension": "pug"}},
    {{"pharse": "Search Phrase 3"}},
]}}

Here is the summary of the folder structre for this project (not all of it some parts are ommited to save memory):
{dir_structure}

REMEMBER: SEARCH FOR WHAT IS ALREADY IN THE CODEBASE. NOT WHAT YOU GOING TO IMPLEMENT
""")

def generate_search_phrases_user():
    return('What are some code parts that would be relevant to solving this task')

def if_changes_needed_system():
    return("""You are very smart software engineer whose job is classifying if some speech someone else made dictates some changes on a file or not. You do not use your own judgement. Your only job is understanding what the speech is saying and classifiying if the speech is describing a change or not. If the speech does describe a change in the file, you decide if it includes mutliple changes (complex and more than 1 steps) or a single change. You always give your answer in the JSON format. Here is the JSON format you must always stick to:
{
    "decision": True or False - this is a boolean value. just one word: true or false,
    "is_multiple": True or False - this is a boolean value. True if the speech describes multiple changes in various places of the file. False, otherwise.
}
""")

def if_changes_needed_user(speech):
    return(f"Here is the speech given by another software engineer:\n{speech}\n\n Decide if it describes a change that needs to be done on a file or the conclusion is that no change is needed. Give your answer in the JSON format.")

def split_complex_task_system():
    return("""You are an extremely samrt and careful software engineer whose whole job is splitting up complext tasks on code files into smaller sub-tasks. 
           
#RULES
* You must cover all of the changes described in the original task. 
* A sub-task must be a change described in a single location on the file. This does not mean a single line. It can be fairly large hunk of code. But the changes should note be more than 20 lines apart.
* If a sub-task requires to make changes in multiple places in a file, divide it up. 
* Be extremely detailed when describing the sub-task and its steps and do not miss any detail that has been mentioned in the original task. 
* You are highly encouraged to copy the code from the original task if there is one. 
           
Give your answer in the JSON format below:
{
    "sub_tasks": [
           {
           "title": "Some title describing the subtask"
           "steps": ["Steps of how to do this subtask. THis where you should include code if any. Length is not a concern. Right as long as you need", ...]
           }]
}""")

def split_complex_task_user(task):
    return(f"Here is your complex task with multiple steps:\n{task}\n\nDivide this into sub-tasks. Remember, each sub-task must dictate a change in a single location (50 lines or less) in the file and you must give your answer in the JSON format above.")



