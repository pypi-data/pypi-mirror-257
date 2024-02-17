import inquirer
from supabase import create_client, Client
import json
from fumedev.env import relative_path
from fumedev.auth.keys import decrypt_message, encrypt_message, load_or_generate_key
from fumedev import env


supabase_url = 'https://ftjimequrvncmgwbzcsh.supabase.co'
supabase_public = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImZ0amltZXF1cnZuY21nd2J6Y3NoIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MDM3Nzc5NjYsImV4cCI6MjAxOTM1Mzk2Nn0.qOQYWOM9wLrFtQYDVWAf59P3_1zkbmw-FeGrDL_U-kw'

supabase = create_client(supabase_url, supabase_public)



def save_credentials(email, password, api_key, key):
    encrypted_email = encrypt_message(email, key)
    encrypted_password = encrypt_message(password, key)
    encrypted_api_key = encrypt_message(api_key, key)
    with open(relative_path('credentials.json'), 'w') as creds_file:
        json.dump({'email': encrypted_email, 'password': encrypted_password, 'openai_api_key': encrypted_api_key}, creds_file)

def try_auto_login(key):
    try:
        with open(relative_path('credentials.json'), 'r') as creds_file:
            creds = json.load(creds_file)
            email = decrypt_message(creds['email'], key)
            password = decrypt_message(creds['password'], key)
            result = supabase.auth.sign_in_with_password({'email': email, 'password': password})
            if 'error' not in result:
                print("Welcome,", email)
                env.OPENAI_API_KEY = decrypt_message(creds['openai_api_key'], key)
                return True
    except Exception as e:
        return False
    return False


def login():
    key = load_or_generate_key()
    if try_auto_login(key):
        return

    questions = [
        inquirer.Text('email', message="Please enter your email"),
        inquirer.Password('password', message="Please enter your password"),
    ]

    answers = inquirer.prompt(questions)

    email = answers['email']
    password = answers['password']

    api_key = input('Please enter your OpenAI API key: ')

    env.OPENAI_API_KEY = api_key

    try:
        supabase.auth.sign_in_with_password({'email': email, 'password': password})
        print("\nLogin successful, Welcome!\n")
        save_credentials(email, password, api_key, key)

    except Exception as e:
        print("\nLogin failed please try again.\n")
        login()