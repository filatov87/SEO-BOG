# SEO BOG

## Project Description
SEO BOG generates data for promotional Travel SEO pages. The data includes FAQs, short and long articles, O&D route maps. This project includes various scripts for handling Excel and CSV files, generating HTML maps, and more.

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
- [Scripts](#scripts)
- [Dependencies](#dependencies)
- [Configuration](#configuration)
- [Contribution](#contribution)
- [License](#license)
- [Contact](#contact)

## Installation
1. Clone the repository:
    ```sh
    git clone https://github.com/filatov87/SEO-BOG.git
    cd SEO-BOG
    ```
2. Set up a virtual environment and activate it:
    ```sh
    python3 -m venv myenv
    source myenv/bin/activate
    ```
3. Install the required dependencies:
    ```sh
    pip install pandas openpyxl selenium urllib3 google-api-python-client requests pillow
    ```

## Usage
### Running the Scripts
1. **Generate Text Data**: 
    - For English content: 
        ```sh
        python SEO_Content_generator.py
        ```
    - For Spanish content: 
        ```sh
        python Spanish_SEO_Content_generator.py
        ```

2. **Parse to JSON if needed**:
    ```sh
    python bilingual_parser_to_JSON.py
    ```

3. **Generate Static Maps**:
    ```sh
    python Static_maps_generator.py
    ```

4. **Add Logos to Maps**:
    ```sh
    python add_logos_to_maps.py
    ```

5. **Generate HTML Maps (if needed)**:
    ```sh
    python html_map_generator.py
    ```

## Scripts
- `SEO_Content_generator.py`: Generates English SEO content.
- `Spanish_SEO_Content_generator.py`: Generates Spanish SEO content.
- `bilingual_parser_to_JSON.py`: Parses Excel files and converts them to JSON format.
- `Static_maps_generator.py`: Generates static maps.
- `add_logos_to_maps.py`: Adds logos to generated maps.
- `html_map_generator.py`: Generates HTML maps based on provided data.

## Dependencies
- pandas
- openpyxl
- selenium
- urllib3
- google-api-python-client
- requests
- pillow

Install these dependencies using:
```sh
pip install pandas openpyxl selenium urllib3 google-api-python-client requests pillow
```
## Configuration

Ensure the following files are prepared and placed in the appropriate directories:

- `departures_destinations.csv`: Contains data with columns Lead Departure City code, Lead Departure City, Lead Departure Country, Lead Destination City code, Lead Destination City, Lead Destination Country.
- `Logo.png`: Logo file to be used in the maps.

The input files should be placed in the Source directory, and the output files will be saved in the JSON-output directory.

## Contribution

	1.	Fork the repository.
	2.	Create a new branch (git checkout -b feature-branch).
	3.	Make your changes.
	4.	Commit your changes (git commit -am 'Add new feature').
	5.	Push to the branch (git push origin feature-branch).
	6.	Create a new Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contact

For any questions or issues, please open an issue in the repository or contact filatov87.