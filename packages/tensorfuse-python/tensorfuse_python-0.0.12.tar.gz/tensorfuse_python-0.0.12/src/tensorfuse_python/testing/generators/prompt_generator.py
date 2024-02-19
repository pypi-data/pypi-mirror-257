import logging
from typing import Optional

from colorama import Fore
from openai import OpenAI

from tensorfuse_python.oss_telemtery import track_event

logger = logging.getLogger(__name__)

def generate_candidate_prompt(openai_api_key: str, prompt: str):
    system_message = '''
    You're helping a scientist who is tuning a prompt for a large language model.
    You will receive messages, and each message is a full prompt.  Generate a candidate
    variation of the given prompt.This variation will be tested for quality in order to
    select a winner.
    
    Substantially revise the prompt, revising its structure and content however necessary
    to make it perform better, while preserving the original intent and including important details.
    
    Your output is going to be copied directly into the program. It should contain the prompt ONLY.
    '''

    client = OpenAI(api_key=openai_api_key)
    response = client.chat.completions.create(model="gpt-3.5-turbo",
                                              messages=[{"role": "system", "content": system_message}, {"role": "user",
                                                                                                        "content": 'Generate a variant for the following prompt:'},
                                                        {"role": "user", "content": prompt}, ], temperature=1)
    track_event('prompt_generated')
    return response.choices[0].message.content


def generate_prompt_variations(openai_api_key: str, prompt: str, num_variations: int):
    logging.info(Fore.GREEN + 'Generating %d variations for prompt:\n %s', num_variations, prompt)
    variations = []
    for i in range(num_variations):
        variation = generate_candidate_prompt(openai_api_key, prompt)
        variations.append(variation)
        print(Fore.GREEN + 'Generated variation %d.', i)
    return variations


def generate_and_save_prompt_variations(openai_api_key: str, prompt: str, num_variations: int,
                                        file_path: Optional[str] = None):
    if num_variations > 10:
        raise ValueError('Number of variations cannot be more than 10')
    if num_variations < 1:
        raise ValueError('Number of variations cannot be less than 1')
    if file_path is None:
        file_path = 'prompt_variations.txt'
    variations = generate_prompt_variations(openai_api_key, prompt, num_variations)
    with open(file_path, 'w') as f:
        for idx, variation in enumerate(variations):
            f.write(f'===========Variation {idx + 1}===========\n')
            f.write(variation + '\n\n\n')
