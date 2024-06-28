import os
import csv
import requests
import datetime
import logging
from keys import GOOGLE_MAPS_API_KEY

# Настройка логирования
logging.basicConfig(filename='static_map_log.txt', level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')

# Создание директорий для PNG файлов
output_dir = 'Results/html_map_png'
os.makedirs(output_dir, exist_ok=True)

# Функция для геокодирования города
def geocode_city(city, country):
    try:
        response = requests.get(
            'https://maps.googleapis.com/maps/api/geocode/json',
            params={'address': f'{city}, {country}', 'key': GOOGLE_MAPS_API_KEY}
        )
        if response.status_code == 200:
            results = response.json().get('results')
            if results:
                location = results[0]['geometry']['location']
                logging.info(f'Геокодирование успешно для {city}, {country}: {location["lat"]}, {location["lng"]}')
                return location['lat'], location['lng']
        logging.error(f'Ошибка геокодирования для {city}, {country}: {response.status_code}')
    except Exception as e:
        logging.error(f'Исключение при геокодировании для {city}, {country}: {e}')
    return None, None

# Чтение CSV-файла и генерация PNG-изображений
with open('departures_destinations.csv', newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        departure_city_code = row["Lead Departure City code"]
        departure_city = row["Lead Departure City"]
        departure_country = row["Lead Departure Country"]
        destination_city_code = row["Lead Destination City code"]
        destination_city = row["Lead Destination City"]
        destination_country = row["Lead Destination Country"]

        logging.info(f'Обработка пары: {departure_city} - {destination_city}')

        dep_lat, dep_lng = geocode_city(departure_city, departure_country)
        dest_lat, dest_lng = geocode_city(destination_city, destination_country)

        if dep_lat and dep_lng and dest_lat and dest_lng:
            date_str = datetime.datetime.now().strftime('%d%m')
            png_filename = f'{output_dir}/{departure_city}_{destination_city}_map_{date_str}.png'

            # Генерация URL для Google Maps Static API
            static_map_url = (
                f"https://maps.googleapis.com/maps/api/staticmap?size=1000x1000&maptype=roadmap"
                f"&path=color:0x0000ff|weight:5|geodesic:true|{dep_lat},{dep_lng}|{dest_lat},{dest_lng}"
                f"&key={GOOGLE_MAPS_API_KEY}"
            )

            # Скачивание изображения карты
            try:
                response = requests.get(static_map_url)
                if response.status_code == 200:
                    with open(png_filename, 'wb') as img_file:
                        img_file.write(response.content)
                    logging.info(f'PNG файл создан: {png_filename}')
                    print(f'PNG файл создан: {png_filename}')  # Сообщение в терминал
                else:
                    logging.error(f'Ошибка при скачивании карты: {response.status_code}')
                    print(f'Ошибка при скачивании карты: {response.status_code}')
            except Exception as e:
                logging.error(f'Исключение при скачивании карты для пары {departure_city} - {destination_city}: {e}')
                print(f'Исключение при скачивании карты для пары {departure_city} - {destination_city}: {e}')

        else:
            logging.error(f'Ошибка геокодирования для пары: {departure_city} - {destination_city}')
            print(f'Ошибка геокодирования для пары: {departure_city} - {destination_city}')
