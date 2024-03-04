import openai
import os
import data.config as config
from retrying import retry
from dotenv import load_dotenv

load_dotenv(dotenv_path=os.path.join('secrets', '.env'))

openai.api_key = os.environ['API_KEY']

@retry(stop_max_attempt_number=3, wait_fixed=2000)
def create_prompt(prompt, command=False):
    print('attempting to create a prompt')
    if command:
        return openai.chat.completions.create(model=config.model, messages=[{"role": "user", "content": f"In the personality of {config.personality}, reply to {prompt} as if it were a twitch command in less than 50 words."}], temperature = 1.2, max_tokens = 125)
    else:
        return openai.chat.completions.create(model=config.model, messages=[{"role": "user", "content": f"In the personality of {config.personality}, reply to {prompt} in less than 50 words."}], temperature = 1.2, max_tokens = 125)