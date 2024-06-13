Travel Promotions Content Generator

This project helps in generating travel promotion content by combining city pairs from a CSV file, and using the OpenAI API to generate detailed travel content. The outputs are saved in an Excel file.
Features

Read City Pairs: Read the city pairs from a CSV file.
Generate Content: Use OpenAI's GPT-3.5 to generate travel-related content.
Create Excel: Save the generated content in an Excel file with a defined structure.
Requirements

Python 3.6+
Required Python Libraries:
pandas
openpyxl
requests
CSV file (departures_destinations.csv) with columns:
Lead Departure City code
Lead Departure City
Lead Departure Country
Lead Destination City code
Lead Destination City
Lead Destination Country
keys.py file with API_KEY defined for OpenAI API
Setup

Clone the repository:
git clone https://github.com/your-username/repo-name.git
Navigate to the project directory:
cd repo-name
Install the required libraries using pip:
pip install pandas openpyxl requests
Ensure you have the departures_destinations.csv file placed in the root of the project directory.
Create a keys.py file and define your OpenAI API key:
API_KEY = 'your_openai_api_key'
Usage

Run the script to read the city pairs from the CSV, generate the travel content, and save the results to an Excel file:
python your_script_name.py
Functions

read_city_pairs(file_path): Reads city pairs from a CSV file with the specified structure.
call_openai_api(prompt): Calls the OpenAI API to generate content for the given prompt.
create_excel_with_promos(city_pairs, file_prefix="Content_table"): Creates an Excel file with the structure defined in the code and saves generated travel content.
Example

Ensure you have a CSV file named departures_destinations.csv with columns as mentioned in the requirements.
Run the script:
python your_script_name.py
Generated Excel file will be saved inside the Promos directory with a timestamp in the filename.
Notes

Ensure the CSV file has the correct column names and data.
OpenAI API key is required for generating content.
Proper error handling for file reading and API calls is included.
License

This project is licensed under the MIT License. See the LICENSE file for details.
Contributing

Fork it!
Create your feature branch: git checkout -b my-new-feature
Commit your changes: git commit -am 'Add some feature'
Push to the branch: git push origin my-new-feature
Submit a pull request
Contact

For any issues or questions, please open an issue on this repository.
Feel free to customize further according to your project's specifics.