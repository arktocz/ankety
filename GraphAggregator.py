

from typing import Dict,Iterator
import typing
# import strawberry as strawberryA
import uuid
from collections import defaultdict


def aggregate_survey_dataset(survey: Dict) -> Iterator[Dict]:
    questions = survey['questions']

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
                yield question_answer_detail
                
    



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
        async with aiofiles.open(file_path, 'r',encoding='utf-8') as file:
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

    for survey in data['surveyPage']:
        processed_data = list(aggregate_survey_dataset(survey))
        pp.pprint(processed_data)
############################################

##########################################
    import matplotlib.pyplot as plt
    import numpy as np

    # Your list of dictionaries
    data = processed_data

    # Create a dictionary to store the sum and count for each question
    question_sum = {}
    question_count = {}

    for item in data:
        question_id = item['question_id']
        value = float(item['value'])  # Convert value to float for calculation
        
        # If the question_id is not in the dictionary, initialize it
        if question_id not in question_sum:
            question_sum[question_id] = value
            question_count[question_id] = 1
        else:
            question_sum[question_id] += value
            question_count[question_id] += 1

    # Calculate the mean for each question
    question_means = {question_id: question_sum[question_id] / question_count[question_id] for question_id in question_sum}

    # Extract question names and corresponding means
    question_names = [item['question_name'] for item in data if item['question_id'] in question_means]
    means = [question_means[item['question_id']] for item in data if item['question_id'] in question_means]

    # Plotting
    plt.figure(figsize=(10, 6))
    bars=plt.bar(question_names, means, color='skyblue')
    plt.xlabel('Question Name')
    plt.ylabel('Mean Value')
    plt.title('Mean Value of Each Question')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    for bar, mean in zip(bars, means):
        plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height(), round(mean, 2), ha='center', va='bottom')

    plt.show()

##########################################
    import plotly.express as px

    # Create a DataFrame from the data
    import pandas as pd
    ##################################
    df = pd.DataFrame(data)

# Create pivot table
    pivot_table = df.pivot_table(index='user_id', columns='question_name', values='value', aggfunc='first')
    pivot_table.to_excel('pivot_table.xlsx', na_rep='NA')
  

    # Display pivot table
    print(pivot_table)
    ################################
    df = pd.DataFrame(data)

    # Group by question and value, and count the occurrences
    grouped = df.groupby(['question_name', 'value']).size().reset_index(name='count')

    # Create a sunburst chart
    fig = px.sunburst(grouped, path=['question_name', 'value'], values='count')

    # Update layout
    fig.update_layout(title="Sunburst Chart of Responses",
                    sunburstcolorway=["#636efa","#EF553B","#00cc96","#ab63fa","#FFA15A","#19d3f3","#FF6692","#B6E880","#FF97FF","#FECB52"],
                    margin=dict(t=0, l=0, r=0, b=0))
    fig.show()


############################################

asyncio.run(main())