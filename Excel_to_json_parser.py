import pandas as pd
import json
import os

def process_excel_files_in_folder(folder_path, output_folder):
    """Process all Excel files in the specified folder and convert them to JSON."""
    for filename in os.listdir(folder_path):
        if filename.endswith(".xlsx"):
            file_path = os.path.join(folder_path, filename)
            try:
                print(f"Processing {filename}...")
                json_data = create_json_from_excel(file_path)
                output_file_path = os.path.join(output_folder, f"{os.path.splitext(filename)[0]}.json")
                with open(output_file_path, 'w') as json_file:
                    json.dump(json_data, json_file, indent=4)
                print(f"Successfully processed and saved JSON for {filename}")
            except Exception as e:
                print(f"An error occurred while processing {filename}: {e}")

def create_json_from_excel(file_path):
    """Create JSON data from an Excel file."""
    df = pd.read_excel(file_path)
    df.columns = df.columns.str.strip()
    json_data = []

    for _, row in df.iterrows():
        dep_city_code = row['Lead Departure City code']
        dest_city_code = row['Lead Destination City code']
        dep_city = row['Lead Departure City']
        dest_city = row['Lead Destination City']

        # FAQ section in array format
        faq_block = []
        faq_data = row['F.A.Q.']
        if pd.notna(faq_data):
            faq_entries = [entry.strip().replace('\n', '<br>') for entry in faq_data.strip().split('\n\n')]
            for entry in faq_entries:
                try:
                    parts = entry.split('<br>')
                    if len(parts) == 2:
                        question = parts[0].split(': ', 1)[1]
                        answer = parts[1].split(': ', 1)[1]
                        faq_block.append({"question": question, "answer": answer})
                    else:
                        print(f"Error processing FAQ entry '{entry}': incorrect format")
                except IndexError:
                    print(f"Error processing FAQ entry '{entry}': list index out of range")

        # Article sections
        article_blocks = []
        articles = {
            f"Top things to do in {dest_city}": "articleBlock1",
            "Sample day-by-day itinerary in {destination_city}": "articleBlock2",
            "Experience the {destination_city} lifestyle": "articleBlock3",
            "Best dining options in {destination_city}": "articleBlock4",
            "Shopping in {destination_city}": "articleBlock5",
            "Nightlife and entertainment in {destination_city}": "articleBlock6",
            "Cultural and historical experiences in {destination_city}": "articleBlock7",
            "Nature and outdoor activities in {destination_city}": "articleBlock8",
            "Travel tips for {destination_city}": "articleBlock9",
            "Fun Facts about {destination_city}": "articleBlock10",
            "Get ready for your trip to {destination_city}": "articleBlock11"
        }
        for key, value in articles.items():
            if key in df.columns and pd.notna(row[key]):
                text_with_line_breaks = row[key].replace('\n', '<br>')
                if '<li>' in text_with_line_breaks:
                    text_with_line_breaks = text_with_line_breaks.replace('<br>', '</li><li>')
                    text_with_line_breaks = f"<ul><li>{text_with_line_breaks}</li></ul>"

                article_blocks.append({
                    "id": value,
                    "title": key.replace('{departure_city}', dep_city).replace('{destination_city}', dest_city),
                    "text": text_with_line_breaks
                })

        # Create imageBlock with default placeholders
        image_block = {
            "title": "Placeholder Title",
            "text": "Placeholder Text"
        }

        # Append the structured JSON data to the list
        json_data.append({
            "depCity": dep_city_code,
            "destCity": dest_city_code,
            "imageBlock": image_block,
            "faqBlock": faq_block,
            "articleBlocks": article_blocks
        })
    return json_data

if __name__ == "__main__":
    script_directory = os.path.dirname(os.path.abspath(__file__))
    source_folder = os.path.join(script_directory, 'Source')
    output_folder = os.path.join(script_directory, 'JSON-output')
    # Ensure the output directory exists
    os.makedirs(output_folder, exist_ok=True)
    process_excel_files_in_folder(source_folder, output_folder)