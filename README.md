# SEO BOG

## Project Description
SEO BOG generates data for promotional Travel SEO pages, including FAQs, short and long articles, and O&D route maps. This project contains various scripts for handling Excel and CSV files, generating HTML maps, and more.

> **Important Notice**  
> This repository and its contents are proprietary to Aleksejs Filatovs (filatov87). Unauthorized use or distribution of this code is prohibited. For any questions, contact the repository owner.

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
    pip install -r requirements.txt
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
Dependencies for this project are listed in the `requirements.txt` file and can be installed with:
```sh
pip install -r requirements.txt

## Configuration
Ensure the following files are prepared and placed in the appropriate directories:
- `departures_destinations.csv`: Contains data with columns:  
  Lead Departure City code, Lead Departure City, Lead Departure Country, Lead Destination City code, Lead Destination City, Lead Destination Country.
- `Logo.png`: Logo file to be used in the maps.

Input files should be placed in the `Source` directory, and the output files will be saved in the `JSON-output` directory.

## Contribution
Contributions to this project are welcome but must adhere to the following:
1. Fork the repository.
2. Create a new branch for your feature:
    ```sh
    git checkout -b feature-branch
    ```
3. Make your changes.
4. Commit your changes with a descriptive message:
    ```sh
    git commit -am 'Add new feature'
    ```
5. Push your changes:
    ```sh
    git push origin feature-branch
    ```
6. Open a Pull Request.

## License
This project is licensed under the MIT License.  
See the [LICENSE](LICENSE) file for details.

> **Note:** All contributors must agree to the licensing terms of this project.

## Contact
For any questions, issues, or requests, please open an issue in the repository or contact **[filatov87]** directly.
