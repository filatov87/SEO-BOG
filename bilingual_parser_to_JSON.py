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
    print(f"Columns in file {file_path}: {df.columns.tolist()}")
    json_data = []

    for _, row in df.iterrows():
        dep_city_code = row['Lead Departure City code']
        dest_city_code = row['Lead Destination City code']
        dep_city = row['Lead Departure City']
        dest_city = row['Lead Destination City']

        # FAQ section in array format
        faq_block = []
        if 'F.A.Q.' in df.columns:
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
        else:
            print("Warning: 'F.A.Q.' column not found in the Excel file.")

        # Article sections
        article_blocks = []

        # Define article keys for both languages
        article_keys = {
            "spanish": {
                f"Guía definitiva para viajar de {dep_city} a {dest_city}": "articleBlock1",
                f"¿Qué debo saber de {dest_city}?": "articleBlock2",
                f"Vuelos baratos desde {dep_city} a {dest_city}": "articleBlock3",
                f"Cómo llegar desde {dep_city} a {dest_city} en avion": "articleBlock4",
                f"Traslados a la ciudad y alrededores desde el aeropuerto a {dest_city}": "articleBlock5",
                f"Dónde alojarse en {dest_city}?": "articleBlock6",
                f"Los mejores lugares turísticos de {dest_city} que debes conocer": "articleBlock7",
                f"Palabras para saber en {dest_city}": "articleBlock8",
                f"Cosas que debes saber antes de viajar a {dest_city}": "articleBlock9",
                f"Datos curiosos sobre {dest_city}": "articleBlock10",
                f"Prepárate para tu viaje a {dest_city}": "articleBlock11"
            },
            "english": {
                f"Your ultimate guide for {dep_city} to {dest_city} travel": "articleBlock1",
                f"What you need to know about {dest_city}?": "articleBlock2",
                f"Unlocking the best {dep_city} to {dest_city} flight deals": "articleBlock3",
                f"Best {dep_city} to {dest_city} itineraries": "articleBlock4",
                f"Transportation to {dest_city} from Airport": "articleBlock5",
                f"Where to stay in {dest_city}?": "articleBlock6",
                f"Top sights and attractions in {dest_city}": "articleBlock7",
                f"Words to know in {dest_city}": "articleBlock8",
                f"What to remember before traveling to {dest_city}": "articleBlock9",
                f"Fun Facts about {dest_city}": "articleBlock10",
                f"Get ready for your trip to {dest_city}": "articleBlock11"
            }
        }

        # Determine the language of the document by checking the column names
        if any(key in df.columns for key in article_keys['spanish'].keys()):
            articles = article_keys['spanish']
            print("Detected language: Spanish")
        else:
            articles = article_keys['english']
            print("Detected language: English")

        for key, value in articles.items():
            if key in df.columns:
                print(f"Found column for key: {key}")
                if pd.notna(row[key]):
                    print(f"Processing text for key: {key}")
                    text_with_line_breaks = row[key].replace('\n', '<br>')
                    if '<li>' in text_with_line_breaks:
                        text_with_line_breaks = text_with_line_breaks.replace('<br>', '</li><li>')
                        text_with_line_breaks = f"<ul><li>{text_with_line_breaks}</li></ul>"

                    article_blocks.append({
                        "id": value,
                        "title": key.replace('{departure_city}', dep_city).replace('{destination_city}', dest_city),
                        "text": text_with_line_breaks
                    })
            else:
                print(f"Column not found for key: {key}")

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