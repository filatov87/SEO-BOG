from openpyxl.styles import Alignment, Font
from openai import OpenAI
import csv
from openpyxl import Workbook
import os
import datetime
import keys

# Set your OpenAI API key
client = OpenAI(
  api_key= keys.API_KEY  # this is also the default, it can be omitted
)

# Define the questions
questions = [
    "What are the must-visit places in {destination}?",
    "What phrases should I know in local language in {destination}?",
    "What 3 local dishes should I try in {destination}?",
    # Add more questions as needed
]

def generate_text(prompt):
    response = client.completions.create(
        model= "gpt-3.5-turbo-instruct",
        prompt=prompt,
        max_tokens=100
    )
    return response.choices[0].text.strip()

# Function to load destinations from a CSV file
def load_destinations_from_csv(csv_file):
    destinations = []
    with open(csv_file, "r", newline="", encoding="utf-8") as file:
        reader = csv.reader(file)
        for row in reader:
            destinations.append(row[0])
    return destinations

# Get the path to the cities CSV file
current_dir = os.path.dirname(os.path.abspath(__file__))
cities_file = os.path.join(current_dir, "cities.csv")

# Load destinations from the CSV file
destinations = load_destinations_from_csv(cities_file)

# Function to generate combinations of questions and destinations
def generate_combinations(questions, destinations):
    combinations = []
    for question in questions:
        for destination in destinations:
            prompt = question.replace("{destination}", destination)
            answer = generate_text(prompt)
            combinations.append((question, destination, answer))
    return combinations

# Generate combinations
combinations = generate_combinations(questions, destinations[:2])  # Take the first X cities

# Create a new Excel file with timestamp in the filename
timestamp = datetime.datetime.now().strftime("%d%m_%H%M")
filename = f"Answers_{timestamp}.xlsx"
wb = Workbook()
ws = wb.active

# Write the header row with questions as column titles
ws.append(["Destination"] + questions)

# Write the data rows
for destination in destinations:
    row_data = [destination]  # Start with the destination name
    
    # Write answers for each question
    for question in questions:
        # Get the answer for the current question and destination
        answer = [combinations[j][2] for j in range(len(combinations)) if combinations[j][1] == destination and combinations[j][0] == question][0] if combinations else ""
        
        # Add the answer to the row_data
        row_data.append(answer)
    
    # Write the row_data to the worksheet
    ws.append(row_data)

# Apply text wrapping for all cells
for row in ws.iter_rows():
    for cell in row:
        cell.alignment = Alignment(wrap_text=True)

# Save the results to the Excel file
wb.save(filename)

print("done!")