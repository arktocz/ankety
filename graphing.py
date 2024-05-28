import plotly.express as px
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def Bargraph(data):
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

def excel_pivot_table(data):
    df = pd.DataFrame(data)
    pivot_table = df.pivot_table(index='user_id', columns='question_name', values='value', aggfunc='first')
    pivot_table.to_excel('pivot_table.xlsx', na_rep='NA')
  

    # Display pivot table
    print(pivot_table)

def Sunburstgraph(data):
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