

from typing import List, Union, Dict
import typing
# import strawberry as strawberryA
import uuid
from collections import defaultdict


async def aggregate_survey_dataset(survey_json: Dict) -> List:
    user_questions = []
    questions = survey_json['surveyPage'][0]['questions']

    for question in questions:
        question_info = {
            'question_id': question['id'],
            'question_name': question['name'],
            'order': question['order'],
            'type_name': question['type']['name']
        }
        
        for answer in question['answers']:
            if answer['user']:
                answer_info = {
                    'answer_id': answer['id'],
                    'value': answer['value'],
                    'answered': answer['answered'],
                    'user_id': answer['user']['id']
                }

                question_answer_detail = {**question_info, **answer_info}
                user_questions.append(question_answer_detail)
                
    return user_questions



import json
import aiofiles
import pprint

async def load_json_data(file_path):
    """
    Load data from a JSON file.

    :param file_path: str - Path to the JSON file.
    :return: dict or list - The data loaded from the JSON file.
    """
    try:
        # Use aiofiles to open the file asynchronously
        async with aiofiles.open(file_path, 'r') as file:
            data = await file.read()  # Read data asynchronously
            return json.loads(data)  # Deserialize JSON to a Python object
    except FileNotFoundError:
        print(f"The file {file_path} does not exist.")
        return None
    except json.JSONDecodeError:
        print(f"Error decoding JSON from the file {file_path}.")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

# Example usage:
# Replace 'path_to_file.json' with the path to your JSON file

import asyncio
import pprint

async def main():
    pp = pprint.PrettyPrinter(depth=4)
    data = await load_json_data('fake_data.json')
    pp.pprint(await aggregate_survey_dataset(data))

asyncio.run(main())