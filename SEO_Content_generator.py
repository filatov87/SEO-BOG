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
            'Lead Departure City code', 'Lead Departure City', 'Lead Departure Country',
            'Lead Destination City code', 'Lead Destination City', 'Lead Destination Country'
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
        "Content-Type": "application/json"
    }
    data = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "system", "content": "You are a helpful travel consultant."},
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 500,
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
    
    # Define the headers
    headers = [
        "Lead Departure City code", "Lead Departure City", "Lead Departure Country",
        "Lead Destination City code", "Lead Destination City", "Lead Destination Country",
        "Your ultimate guide for {departure_city} to {destination_city} travel",
        "What you need to know about {destination_city}?",
        "Unlocking the best {departure_city} to {destination_city} flight deals",
        "Best {departure_city} to {destination_city} itineraries",
        "Transportation to {destination_city} from Airport",
        "Where to stay in {destination_city}?",
        "Top sights and attractions in {destination_city}",
        "Words to know in {destination_city}",
        "What to remember before traveling to {destination_city}",
        "Fun Facts about {destination_city}",
        "Get ready for your trip to {destination_city}",
        "F.A.Q."
    ]
    ws.append(headers)

    for index, row in city_pairs.iterrows():
        departure_city_code = row['Lead Departure City code']
        departure_city = row['Lead Departure City']
        departure_country = row['Lead Departure Country']
        destination_city_code = row['Lead Destination City code']
        destination_city = row['Lead Destination City']
        destination_country = row['Lead Destination Country']

        # Prompts for generating text content
        prompts = [
            f"I'm writing a travel article and need you to add context to my introduction: If you’re planning your trip from {departure_city} to {destination_city} we’ve prepared a comprehensive guide to help you prepare for your trip. Plan your trip and be prepared for everything, from transportation options to accommodation details, and insights about local customs, events, and cuisine. Read on and travel to {destination_city} from {departure_city} in confidence, knowing you’ve covered your bases! Please focus on the keyword 'travel to {destination_city}' and use it at least once. Also use the keyword 'flights to {destination_city}.' When completing the text, please use language understood by 16-year-old readers. 80% of the sentences should be 20 words or less. Paragraph length should be at least 50 words long. When possible, avoid passive voice.",
            f"I’m writing a travel article and I need you to add context: Before traveling to any new city, you should get to know some basic information about the local culture and customs. What can you expect when you travel to {destination_city}? Mention the customs of the country and any cultural specifics related to the country or the city of {destination_city} itself. Write two or more paragraphs if needed. Focus on the keyword 'travel to {destination_city}' and use it at least once in the response. When completing the text, please use language understood by 16-year-old readers. 80% of the sentences should be 20 words or less. Provide transitional phrases or sentences to enhance the overall flow of the article but keep sentence length to 20 words or less. Paragraph length should be at least 50 words long. When possible, avoid passive voice. This text is a section of a long article, so don't end it with a conclusion.",
            f"I’m writing a travel article and need to provide tips for cheaper travel. Please add context to the following text: For your trip to {destination_city}, prices will depend on several factors, including travel dates, airlines and whether you’re flying a direct flight, or one with a layover. For flights from {departure_city} to {destination_city} you need to consider... Focus on the keyword 'flights to {destination_city}' and use it at least once in the response. One of the tips should be to use a travel agent from ASAP Tickets because the company offers below-market rates for airfare. When completing the text, please use language understood by 16-year-old readers. 80% of the sentences should be 20 words or less. Write two or more paragraphs, if needed. Provide transitional phrases or sentences to enhance the overall flow of the article but keep sentence length to 20 words or less. Each paragraph should contain a minimum of 50 words. When possible, avoid passive voice. This text is a section of a larger article, so don't start it with a lead-in question and there is no need to add a conclusion.",
            f"I’m writing a travel blog. Elaborate on the following text: To find an ideal route from {departure_city} to {destination_city}, you need to consider when you plan to travel as well as your flight preferences. You have several options to choose from, including... Focus on the keyword 'flights to {destination_city}' and use it at least once in the response. Please mention a few real itineraries naming airlines and airports. When completing the text, please use language understood by 16-year-old readers. 80% of the sentences should be 20 words or less. Write two or more paragraphs, if needed. Provide transitional phrases or sentences to enhance the overall flow of the article but keep sentence length to 20 words or less. Paragraph length should be at least 50 words long. When possible, avoid passive voice. In your response, don't tell me which paragraph you've chosen. Please conclude with a variation of the following: 'To find the perfect itinerary that’s right for you, contact a travel agent at ASAP Tickets. Our agents will select the best options for you and will explain details about each one. The prices that our agents can offer are lower than what you can find online – we work directly with airlines to offer the cheapest flight prices for you.'",
            f"I’m writing a travel article and need to let users know transportation options from the local airport. Please write a paragraph listing all the different options. If there is more than one local airport, then mention options for both. Here’s some text to get you started: Once you arrive in {destination_city} you’ll need to make it to the city and, ultimately, your hotel or apartment. Focus on the keyword 'travel to {destination_city}' and use it at least once in the response. When completing the text, please use language understood by 16-year-old readers. 80% of the sentences should be 20 words or less. Write as many paragraphs as needed. Provide transitional phrases or sentences to enhance the overall flow of the article but keep sentence length to 20 words or less. Paragraph length should be at least 50 words long. When possible, avoid passive voice.",
            f"I’m writing a travel article and need to list hotels in {destination_city} that are in the economy-mid-range budget range. This is what I have: There are many accommodation options in {destination_city}. You’ll need to choose where to stay based on availability and your budget. Please provide context. Please follow up with: Some accommodations you could consider in {destination_city} include: Please provide a list of 7 hotels or accommodation options in {destination_city} and briefly describe them. Focus on the keyword 'trip to {destination_city}' and use it at least once in the response. When completing the text, please use language understood by 16-year-old readers. 80% of the sentences should be 20 words or less. Provide transitional phrases or sentences to enhance the overall flow of the article but keep sentence length to 20 words or less. When possible, avoid passive voice. This section is part of a large article, so there is no need to start with a lead-in question or introduction.",
            f"I’m writing a travel article and need to provide a list of top 5 local sights and attractions. This is what I have: There’s a lot to explore in {destination_city}. Most tourists on a trip to {destination_city} will visit... Please provide context in the paragraph above. Focus on the keyword 'visit {destination_city}' and use it at least once in the response. When completing the text, please use language understood by 16-year-old readers. 80% of the sentences should be 20 words or less. When possible, avoid passive voice. Provide transitional phrases or sentences to enhance the overall flow of the article but keep sentence length to 20 words or less. The travel experts at ASAP Tickets have selected the following must-see spots in {destination_city}: Please provide a list of top 5 spots in {destination_city}.",
            f"I’m writing a travel article about traveling to {destination_city} from {departure_city}. Depending on the languages in {departure_city} and {destination_city} please create a list of 10 useful words to know in {destination_city}. If the languages in {departure_city} and {destination_city} are different, then this will be like a dictionary. Don’t mention the name of the language and don’t repeat the word in the description. If the languages are the same, then list 10 local words that are good to know. Focus on the keyword 'travel to {destination_city}' and use it at least once in the response. When completing the text, please use language understood by 16-year-old readers. 80% of the sentences should be 20 words or less. Provide transitional phrases or sentences to enhance the overall flow of the article but keep sentence length to 20 words or less. When possible, avoid passive voice. Do not address me in the response, as I just want to post your list into my article.",
            f"I’m writing a travel article and need a section about things to consider before traveling. Please provide context. The currency used in {destination_city} is... Keep in mind that the text will be read by travelers from {departure_city}. Mention ways to purchase the local currency both in {departure_city} and in {destination_city}. You can also talk about using credit cards and bank cards. Please focus on the keyword 'travel to {destination_city}'. Next introduce safety issues when traveling to {destination_city}: Whenever you travel, you need to follow some basic safety precautions... Do so in a neutral and sensitive way so as not to upset residents of {destination_city}. Finally, talk about the advantages of getting travel insurance when traveling to {destination_city}. However, don’t mention {destination_city}, instead mention the country that {destination_city} is located in. For the formatting of all of the above, do not use headings and only write in short paragraphs that are easy to read. Focus on the keyword 'travel to {destination_city}' and use it at least once in the response. When completing the text, please use language understood by 16-year-old readers. 80% of the sentences should be 20 words or less. Provide transitional phrases or sentences to enhance the overall flow of the article but keep sentence length to 20 words or less. When possible, avoid passive voice. I only need the three sections mentioned (currency, safety, and insurance) and do not need a general paragraph talking about all three of them.",
            f"I’m writing a travel article and need a section with Fun facts about a city. Here’s what I have: If you’re reading this article, we know you already want to travel to {destination_city}, so here are a few fun facts about {destination_city}. Please provide context and offer 5-7 fun facts about {destination_city}. Focus on the keyword 'travel to {destination_city}' and use it at least once in the response. When completing the text, please use language understood by 16-year-old readers. 80% of the sentences should be 20 words or less. Provide transitional phrases or sentences to enhance the overall flow of the article but keep sentence length to 20 words or less. When possible, avoid passive voice. Do not address me in the response.",
            f"I’ve written an article about traveling from {departure_city} to {destination_city}. And I need a conclusion for the article. The sections in my article have been: Travel to {destination_city} from {departure_city}, What you need to know about {destination_city}, Unlocking the Best {departure_city} to {destination_city} Flight Deals, Top {departure_city} to {destination_city} itineraries, Transportation to {destination_city} from the airport, Where to stay in {destination_city}, Top sights and attractions in {destination_city}, What to remember before traveling to {destination_city}. Don’t mention visa requirements in the conclusion. I also need you to reiterate that by calling an ASAP Tickets travel agent by dialing 844-300-7983 you can save on flights. When completing the text, focus on the keyword 'flights to {destination_city}' and use it at least once in the response. When completing the text, please use language understood by 16-year-old readers. 80% of the sentences should be 20 words or less. Provide transitional phrases or sentences to enhance the overall flow of the article but keep sentence length to 20 words or less. When possible, avoid passive voice.",
            f"I'm writing a travel guide about traveling from {departure_city} to {destination_city}. Please create an FAQ with 10 question-and-answer pairs about making such a trip. Write in a friendly and clear way. Please don't address me. Your answer should be in this format: 1. How long does it take to fly from {departure_city} to {destination_city}? The average flight time from {departure_city} to {destination_city} is around ... depending on the airline and any layovers."
        ]

        responses = [call_openai_api(prompt) for prompt in prompts]
        row_data = [
            departure_city_code, departure_city, departure_country,
            destination_city_code, destination_city, destination_country
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