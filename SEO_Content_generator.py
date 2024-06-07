import pandas as pd
from openpyxl import Workbook
from datetime import datetime
import requests
import os
from keys import API_KEY  # Ensure you have this module with API_KEY defined

def read_city_pairs(file_path):
    """Reads city pairs from a CSV file with comma delimiter."""
    try:
        data = pd.read_csv(file_path, delimiter=',')
        required_columns = [
            'Lead Departure City', 'Lead Destination City',
            'Lead Departure City code', 'Lead Destination City code'
        ]
        for column in required_columns:
            if column not in data.columns:
                print(f"Error: '{column}' column not found in the CSV file.")
                return pd.DataFrame()  # Return an empty DataFrame
        return data[required_columns]
    except FileNotFoundError:
        print(f"FileNotFoundError: The specified file does not exist at {file_path}")
        return pd.DataFrame()  # Return an empty DataFrame
    except pd.errors.ParserError as e:
        print(f"ParserError: {e}")
        return pd.DataFrame()  # Return an empty DataFrame
    except Exception as e:
        print(f"Exception: An error occurred while reading the file: {e}")
        return pd.DataFrame()  # Return an empty DataFrame

def call_openai_api(prompt):
    """Call the OpenAI API to generate an answer to the given prompt."""
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }
    data = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "system", "content": "You are a helpful travel consultant."},
            {"role": "system", "content": "Do not use the word 'vibrant'."},
            {"role": "system", "content": "Include popular SEO words in your responses"},
            {"role": "system", "content": "Focus only on travelling by plane."},
            {"role": "system", "content": "Do not mention any travel companies, except ASAPtickets.com"},
            {"role": "system", "content": "Don't address me."},
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 400,
        "temperature": 0.8
    }
    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 200:
        return response.json()['choices'][0]['message']['content']
    else:
        print("Failed to fetch response:", response.text)
        return "No answer available."

def create_excel_with_promos(city_pairs, file_prefix="Content_table"):
    now = datetime.now()
    formatted_date_time = now.strftime("%Y%m%d_%H%M")
    directory = "Promos"
    if not os.path.exists(directory):
        os.makedirs(directory)
    output_file = f"{directory}/{file_prefix}_{formatted_date_time}.xlsx"

    wb = Workbook()
    ws = wb.active
    ws.title = "Promotions"

    headers = [
        "Lead Departure City", "Lead Destination City",
        "Lead Departure City code", "Lead Destination City code",
        "BOTTOM: Definitive guide to travel from Lead Departure City to Lead Destination City",
        "LEFT: What should I know about Lead Destination City?",
        "RIGHT: Cheap flights from Lead Departure City to Lead Destination City",
        "BOTTOM:How to get from Lead Departure City to Lead Destination City by plane?",
        "FAQ 1: When is the best time to visit Lead Destination City?",
        "FAQ 2: What 5 phrases should I know when visiting Lead Destination City?",
        "FAQ 3: Do I need a VISA?"
    ]
    ws.append(headers)

    for index, row in city_pairs.iterrows():
        departure_city = row['Lead Departure City']
        destination_city = row['Lead Destination City']
        departure_city_code = row['Lead Departure City code']
        destination_city_code = row['Lead Destination City code']

        prompts = [
            f"""Definitive guide to travel from {departure_city} to {destination_city}. 1000 words. Must include topics like: 
            How to get from {departure_city} to {destination_city} by plane?, 
            Transfers to the city and surroundings from the airport to {destination_city},
            Where to stay in {destination_city}?,
            The best tourist places in {destination_city} that you should know?,
            Words to know in {destination_city},
            Things you should know before traveling to {destination_city},
            Curious facts about {destination_city},
            Prepare for your trip to {destination_city}""",
            f"What should I know about {destination_city}?",
            f"Cheap flights from {departure_city} to {destination_city}",
            f"How to get from {departure_city} to {destination_city} by plane?",
            f"When is the best time to visit {destination_city}?",
            f"What 5 phrases should I know when visiting {destination_city}?",
            f"Do I need a visa for traveling from {departure_city} to {destination_city}?"
        ]

        responses = [call_openai_api(prompt) for prompt in prompts]

        row_data = [
            departure_city, destination_city,
            departure_city_code, destination_city_code
        ] + responses

        ws.append(row_data)

    wb.save(output_file)
    print("Excel file saved as:", output_file)
    print("Done")

if __name__ == "__main__":
    script_directory = os.path.dirname(os.path.abspath(__file__))
    city_pairs_file_path = os.path.join(script_directory, 'departures_destinations.csv')
    city_pairs = read_city_pairs(city_pairs_file_path)
    if not city_pairs.empty:
        create_excel_with_promos(city_pairs)
    else:
        print("No city pairs found or unable to read the file. Please check your CSV file.")