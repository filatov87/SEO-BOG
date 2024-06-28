import os
import csv
import requests
import datetime
import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from keys import GOOGLE_MAPS_API_KEY

# Настройка логирования
logging.basicConfig(filename='log.txt', level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')

# Создание директорий для HTML и PNG файлов
html_dir = 'Results/html_map'
png_dir = 'Results/html_map_png'
os.makedirs(html_dir, exist_ok=True)
os.makedirs(png_dir, exist_ok=True)

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

# Чтение CSV-файла и генерация HTML-файлов и PNG-изображений
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
            html_filename = f'{html_dir}/{departure_city}_{destination_city}_map_{date_str}.html'
            png_filename = f'{png_dir}/{departure_city}_{destination_city}_map_{date_str}.png'

            # Генерация HTML-контента
            html_content = f'''
            <!DOCTYPE html>
            <html lang="es">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Mapa de Vuelo: {departure_city} a {destination_city}</title>
                <style>
                    .map-container {{
                        width: 1000px;
                        height: 1000px;
                        margin-bottom: 20px;
                    }}
                    body, html {{
                        margin: 0;
                        padding: 0;
                        height: 100%;
                        overflow: hidden;
                    }}
                </style>
                <script src="https://maps.googleapis.com/maps/api/js?key={GOOGLE_MAPS_API_KEY}&language=es"></script>
            </head>
            <body>
                <div id="map" class="map-container"></div>
                <script>
                    function initMap() {{
                        var map = new google.maps.Map(document.getElementById('map'), {{
                            mapTypeId: 'roadmap',
                            disableDefaultUI: true
                        }});
                        var bounds = new google.maps.LatLngBounds();
                        var depLatLng = new google.maps.LatLng({dep_lat}, {dep_lng});
                        var destLatLng = new google.maps.LatLng({dest_lat}, {dest_lng});
                        bounds.extend(depLatLng);
                        bounds.extend(destLatLng);
                        map.fitBounds(bounds);

                        var flightPlanCoordinates = [
                            {{ lat: {dep_lat}, lng: {dep_lng} }},
                            {{ lat: {dest_lat}, lng: {dest_lng} }}
                        ];
                        var flightPath = new google.maps.Polyline({{
                            path: flightPlanCoordinates,
                            geodesic: true,
                            strokeColor: '#0000FF',
                            strokeOpacity: 1.0,
                            strokeWeight: 2
                        }});
                        flightPath.setMap(map);
                    }}
                    document.addEventListener('DOMContentLoaded', initMap);
                </script>
            </body>
            </html>
            '''

            try:
                # Сохранение HTML-файла
                with open(html_filename, 'w', encoding='utf-8') as html_file:
                    html_file.write(html_content)
                    logging.info(f'HTML файл создан: {html_filename}')

                # Настройка Selenium для рендеринга HTML и создания скриншота
                options = Options()
                options.headless = True
                options.add_argument("--window-size=1000,1000")  # Устанавливаем размер окна 1000x1000

                driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
                driver.get(f"file://{os.path.abspath(html_filename)}")

                # Ждем загрузки карты
                wait = WebDriverWait(driver, 20)
                wait.until(EC.presence_of_element_located((By.ID, 'map')))

                # Wait for the polyline to be drawn
                wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'path')))

                # Увеличиваем масштаб карты, чтобы маршрут был полностью виден
                driver.execute_script("map.fitBounds(map.getBounds());")

                # Добавляем небольшую задержку для полной прорисовки карты
                driver.implicitly_wait(1)  # Ждем 1 секунду

                # Сохранение скриншота
                driver.save_screenshot(png_filename)
                logging.info(f'PNG файл создан: {png_filename}')

                # Добавление логотипа (в нижний левый угол)
                logo_path = 'logo.png'  # Путь к вашему логотипу
                if os.path.exists(logo_path):
                    img = mpimg.imread(png_filename)
                    logo = mpimg.imread(logo_path)

                    fig, ax = plt.subplots()
                    ax.imshow(img)
                    ax.imshow(logo, extent=(0, logo.shape[1], 0, logo.shape[0]), alpha=1, zorder=1)
                    ax.axis('off')
                    plt.savefig(png_filename, bbox_inches='tight', pad_inches=0)
                    plt.close()
                    logging.info(f'Логотип добавлен на карту: {png_filename}')

                driver.quit()

            except Exception as e:
                logging.error(f'Ошибка при обработке пары {departure_city} - {destination_city}: {e}')
                print(f'Ошибка при обработке пары {departure_city} - {destination_city}: {e}')

        else:
            logging.error(f'Ошибка геокодирования для пары: {departure_city} - {destination_city}')
            print(f'Ошибка геокодирования для пары: {departure_city} - {destination_city}')