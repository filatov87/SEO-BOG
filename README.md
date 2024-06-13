# Travel Article SEO Content Generator

This Python script generates SEO-optimized travel content for given city pairs using the OpenAI API. The generated content is then saved in an Excel file.

## Table of Contents

- [Installation](#installation)
- [Setup](#setup)
- [Usage](#usage)
- [API Key](#api-key)
- [CSV File Format](#csv-file-format)
- [Generated Content](#generated-content)
- [License](#license)

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/travel-article-seo-generator.git
    cd travel-article-seo-generator
    ```

2. Install the required Python packages:
    ```bash
    pip install pandas openpyxl requests
    ```

## Setup

1. **OpenAI API Key**:
    - Obtain an API key from OpenAI.
    - Create a `keys.py` file in the project directory and add your API key:
        ```python
        API_KEY = 'your_openai_api_key'
        ```

## Usage

1. Prepare your CSV file with city pairs:
    - The CSV file should be named `departures_destinations.csv` and placed in the same directory as the script.
    - The format of the CSV should be:
        ```
        Lead Departure City code,Lead Departure City,Lead Departure Country,Lead Destination City code,Lead Destination City,Lead Destination Country
        ```

2. Run the script:
    ```bash
    python SEO_Content_generator.py
    ```

3. The generated content will be saved in an Excel file in the `Promos` directory.

## API Key

Ensure you have your OpenAI API key stored in a `keys.py` file:
```python
API_KEY = 'your_openai_api_key'

## **CSV File Format**
 ```
Lead Departure City code,Lead Departure City,Lead Departure Country,Lead Destination City code,Lead Destination City,Lead Destination Country
 ```

Example:
```bash
WAS,Washington,United States,SAL,San Salvador,El Salvador
NYC,New York,United States,GYE,Guayaquil,Ecuador
NYC,New York,United States,LIM,Lima,Peru
LAX,Los Angeles,United States,SAL,San Salvador,El Salvador
'''

## **Generated Content**

The script generates various sections of a travel article including:

	•	Introduction
	•	Local culture and customs
	•	Tips for cheaper travel
	•	Ideal routes and itineraries
	•	Transportation from the airport
	•	Accommodation options
	•	Top local sights and attractions
	•	Useful words to know
	•	Things to consider before traveling
	•	Fun facts about the city
	•	Conclusion
	•	FAQ

Each section is tailored to the specific city pair and includes relevant SEO keywords.

## **License**

This project is licensed under the MIT License. See the LICENSE file for details.
