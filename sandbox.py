import pandas as pd
from openpyxl import Workbook
from datetime import datetime
import requests
from keys import API_KEY  # Ensure this is your OpenAI API key

def call_openai_api(question):
    """Call the OpenAI API to generate an answer to the given question with specific constraints."""
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }
    # Approximate max_tokens for 500 characters
    max_tokens = 125  # Adjust based on the average character count per token observed
    data = {
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "system", "content": "You are a helpful travel consultant."},
                     {"role": "user", "content": question}],
        "max_tokens": max_tokens,
        "temperature": 0.8
    }
    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 200:
        return response.json()['choices'][0]['message']['content']
    else:
        print("Failed to fetch response:", response.text)
        return "No answer available."


def create_excel_with_questions_answers(cities, file_prefix="answers"):
    """Creates an Excel file with cities as rows and questions as columns, including answers."""
    now = datetime.now()
    formatted_date_time = now.strftime("%Y%m%d_%H%M")
    output_file = f"{file_prefix}_{formatted_date_time}.xlsx"
    
    wb = Workbook()
    ws = wb.active
    questions = [
        "What should I do in {city}?",
        "What local dishes should I try in {city}?",
        "What 5 phrases should I know when visiting {city}?"
    ]
    
    # Write header row: first cell is "City", followed by questions
    headers = ["City"] + [q.format(city="{city}") for q in questions]
    ws.append(headers)

    # Fill rows for each city
    for city in cities:
        row = [city]  # start with city name
        for question_template in questions:
            question = question_template.format(city=city)
            answer = call_openai_api(question)
            row.append(answer)
        ws.append(row)
    
    wb.save(output_file)
    print("Excel file saved as:", output_file)
    print("Done")

if __name__ == "__main__":
    cities = ["New York", "London", "Tokyo"]  # Example cities, replace with read_cities("cities.csv")
    create_excel_with_questions_answers(cities)
