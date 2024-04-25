import pandas as pd
from openpyxl import Workbook
from datetime import datetime
import requests
import os
from keys import API_KEY

def read_cities(file_path):
    """Reads city names from a CSV file."""
    try:
        data = pd.read_csv(file_path)
        if 'City' not in data.columns:
            print("Error: 'City' column not found in the CSV file.")
            return []
        return data['City'].tolist()
    except FileNotFoundError:
        print("FileNotFoundError: The specified file does not exist at", file_path)
        return []
    except Exception as e:
        print(f"Exception: An error occurred while reading the file: {e}")
        return []

def call_openai_api(question):
    """Call the OpenAI API to generate an answer to the given question with specific constraints."""
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }
    max_tokens = 150
    data = {
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "system", "content": "You are a helpful travel consultant."},
                     {"role": "system", "content": "answer should be less than 500 characters"},
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
    directory = "Answers"
    if not os.path.exists(directory):
        os.makedirs(directory)
    output_file = f"{directory}/{file_prefix}_{formatted_date_time}.xlsx"
    
    wb = Workbook()
    ws = wb.active
    questions = [
        "What should I do in {city}?",
        "What local dishes should I try in {city}?",
        "What 5 phrases should I know when visiting {city}?"
    ]
    
    headers = ["City"] + [q.format(city="{city}") for q in questions]
    ws.append(headers)
    for city in cities:
        row = [city]
        for question_template in questions:
            question = question_template.format(city=city)
            answer = call_openai_api(question)
            row.append(answer)
        ws.append(row)
    
    wb.save(output_file)
    print("Excel file saved as:", output_file)
    print("Done")

if __name__ == "__main__":
    # Ensure the path here is correctly set to where your 'cities.csv' is located relative to this script.
    cities_file_path = 'cities.csv'
    cities = read_cities(cities_file_path)
    if cities:
        create_excel_with_questions_answers(cities)
    else:
        print("No cities found or unable to read the file. Please check your CSV file.")
