import os
from PIL import Image

# Директория с исходными изображениями карт
input_dir = 'Results/html_map_png'

# Директория для сохранения изображений с логотипом
output_dir = 'Results/static_map_png_with_logo'  # Добавили "Results/" в начало пути
os.makedirs(output_dir, exist_ok=True)

# Путь к логотипу
logo_path = 'logo.png'

# Настройка отступов для логотипа (в пикселях)
logo_lift_height = 30  # Отступ по высоте
logo_left_offset = 30  # Отступ от левого края

# Высота, которую нужно обрезать снизу (в пикселях)
crop_height = 25

# Загрузка логотипа
logo = Image.open(logo_path).convert("RGBA")

# Проход по всем изображениям в input_dir
for filename in os.listdir(input_dir):
    if filename.endswith(".png"):
        map_path = os.path.join(input_dir, filename)
        map_image = Image.open(map_path).convert("RGBA")

        # Обрезка нижней части изображения
        map_image = map_image.crop((0, 0, map_image.width, map_image.height - crop_height))

        # Добавление логотипа с отступами
        position = (logo_left_offset, map_image.height - logo.height - logo_lift_height)
        map_image.paste(logo, position, logo)

        # Сохранение изображения с логотипом в output_dir
        output_path = os.path.join(output_dir, filename)
        map_image.save(output_path)

        print(f'Логотип добавлен на карту: {output_path}')
