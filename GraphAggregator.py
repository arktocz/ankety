

from typing import List, Union, Dict
import typing
# import strawberry as strawberryA
import uuid
from collections import defaultdict


# @strawberryA.type(description="""Type for query root""")
# class Query:
#     @strawberryA.field(description="""Aggregate survey questions and corresponding answers""")
async def aggregate_survey_dataset( survey_json: Dict) -> List:
    user_questions = defaultdict(list)
    questions = survey_json['surveyPage'][0]['questions']
    # print(survey_json['surveyPage'][0]['questions'])
    for question in questions:
    # Extract question details that are common to all answers
        question_info = {
            'question_id': question['id'],
            'question_name': question['name'],
            'order': question['order'],
            'type_name': question['type']['name']
        }
        
        # Iterate over each answer in the current question
        for answer in question['answers']:
            # Check if there is a user associated with the answer
            if answer['user']:
                # Prepare the answer details
                answer_info = {
                    'answer_id': answer['id'],
                    'value': answer['value'],
                    'answered': answer['answered']
                }
                
                # Combine question and answer details
                question_answer_detail = {**question_info, **answer_info}
                print(question_answer_detail)
                
                # Append the combined question and answer detail to the user's list of questions in the dictionary
                user_questions[answer['user']['id']].append(question_answer_detail)
    print(user_questions)
    # Convert the defaultdict to a regular dictionary for the output
    return dict(user_questions)



import json
import aiofiles

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
async def main():
    data = await load_json_data('fake_data.json')
    print(await aggregate_survey_dataset(data))

asyncio.run(main())