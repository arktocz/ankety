import json

with open('fake_data.json', 'r', encoding='utf-8') as file:
    # Load JSON data
    data = json.load(file)



# Extract questions and answers into list of dictionaries
questions_with_answers = []
for page in data['surveyPage']:
    for question in page['questions']:
        question_with_answers = {
            'question_id': question['id'],
            'question_name': question['name'],
            'question_order': question['order'],
            'question_type_name': question['type']['name'],
            'answers': []
        }
        for answer in question['answers']:
            answer_dict = {
                'answer_id': answer['id'],
                'value': answer['value'],
                'answered': answer['answered'],
                'user_id': answer['user']['id']
            }
            question_with_answers['answers'].append(answer_dict)
        questions_with_answers.append(question_with_answers)

# Print the list of dictionaries
for question in questions_with_answers:
    print(question)
