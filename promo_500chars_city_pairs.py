import pandas as pd
from openpyxl import Workbook
from datetime import datetime
import requests
import os
from keys import API_KEY  # Ensure you have this module with API_KEY defined

def read_city_pairs(file_path):
    """Reads city pairs from a CSV file with semicolon delimiter."""
    try:
        data = pd.read_csv(file_path, delimiter=';')
        if 'Lead Departure City' not in data.columns or 'Lead Destination City' not in data.columns:
            print("Error: 'Lead Departure City' or 'Lead Destination City' column not found in the CSV file.")
            return []
        return data[['Lead Departure City', 'Lead Destination City']].values.tolist()
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
        "messages": [
            {"role": "system", "content": "You are a helpful travel consultant. Include popular SEO words in your answers."},
            {"role": "system", "content": "Each answer should be less than 500 characters. Do not use the word 'vibrant'."},
            {"role": "user", "content": question}
        ],
        "max_tokens": 200,
        "temperature": 0.8
    }
    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 200:
        return response.json()['choices'][0]['message']['content']
    else:
        print("Failed to fetch response:", response.text)
        return "No answer available."

def create_excel_with_promos(city_pairs, file_prefix="Promo_pairs"):
    now = datetime.now()
    formatted_date_time = now.strftime("%Y%m%d_%H%M")
    directory = "Promos"
    if not os.path.exists(directory):
        os.makedirs(directory)
    output_file = f"{directory}/{file_prefix}_{formatted_date_time}.xlsx"

    wb = Workbook()
    ws_en = wb.active
    ws_en.title = "Promotions"

    headers = ["Departure", "Destination", "Promotional Text"]
    ws_en.append(headers)

    for departure, destination in city_pairs:
        question = f"I am traveling from {departure} to {destination}. Write a promotional text for this journey."
        promo_text = call_openai_api(question)
        ws_en.append([departure, destination, promo_text])

    wb.save(output_file)
    print("Excel file saved as:", output_file)
    print("Done")

if __name__ == "__main__":
    script_directory = os.path.dirname(os.path.abspath(__file__))
    city_pairs_file_path = os.path.join(script_directory, 'D&D_most_popular.csv')
    city_pairs = read_city_pairs(city_pairs_file_path)
    if city_pairs:
        create_excel_with_promos(city_pairs)
    else:
        print("No city pairs found or unable to read the file. Please check your CSV file.")