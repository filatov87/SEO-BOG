import pandas as pd
from openpyxl import Workbook
from datetime import datetime
import requests
import os
from keys import API_KEY  # Ensure you have this module with API_KEY defined

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
    """Call the OpenAI API to generate an answer to the given question."""
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }
    data = {
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "system", "content": "You are a helpful travel consultant. Include popular SEO words in your answers."},
                     {"role":"system", "content": "Each answer should be less than 500 characters. Do not use word 'vibrant'."},
                     {"role": "user", "content": question}],
        "max_tokens": 200,
        "temperature": 0.8
    }
    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 200:
        return response.json()['choices'][0]['message']['content']
    else:
        print("Failed to fetch response:", response.text)
        return "No answer available."

def translate_text(text):
    """Translate text from English to Spanish using a similar API call."""
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }
    data = {
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "system", "content": "You are a helpful translator."},
                     {"role": "user", "content": f"Translate to Spanish: {text}"}],
        "max_tokens": 150,
        "temperature": 0.5
    }
    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 200:
        return response.json()['choices'][0]['message']['content']
    else:
        print("Failed to translate text:", response.text)
        return ""

def create_excel_with_questions_answers(cities, file_prefix="promos"):
    now = datetime.now()
    formatted_date_time = now.strftime("%Y%m%d_%H%M")
    directory = "Promos"
    if not os.path.exists(directory):
        os.makedirs(directory)
    output_file = f"{directory}/{file_prefix}_{formatted_date_time}.xlsx"

    wb = Workbook()
    ws_en = wb.active
    ws_en.title = "English"
    ws_es = wb.create_sheet("SPANISH TXT")

    questions = [
        "Why should I visit {city}?",
    ]

    headers = ["City"] + [q.format(city="{city}") for q in questions]
    ws_en.append(headers)
    ws_es.append(headers)

    for city in cities:
        row_en = [city]
        row_es = [city]
        for question_template in questions:
            question = question_template.format(city=city)
            answer_en = call_openai_api(question)
            row_en.append(answer_en)
            answer_es = translate_text(answer_en)
            row_es.append(answer_es)

        ws_en.append(row_en)
        ws_es.append(row_es)

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
