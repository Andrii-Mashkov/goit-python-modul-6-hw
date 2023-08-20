"""
Скрипт проходит по указанной во время вызова папке и сортирует все файлы по группам:
    изображения ('JPEG', 'PNG', 'JPG', 'SVG');
    видео файлы ('AVI', 'MP4', 'MOV', 'MKV');
    документы ('DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX');
    музыка ('MP3', 'OGG', 'WAV', 'AMR');
    архивы ('ZIP', 'GZ', 'TAR');
    неизвестные расширения.

В результате работы есть:
    Список файлов в каждой категории (музыка, видео, фото и пр.)
    Перечень всех известных скрипту расширений, которые встречаются в целевой папке.
    Перечень всех расширений, которые скрипту неизвестны.
"""

import sys
from pathlib import Path

# Определяем списки файлов каждой категории (для анализа обработанных файлов)
IMAGES    = []
VIDEO     = []
DOCUMENTS = []
AUDIO     = []
ARCHIVES  = []
MY_OTHER  = []

# Определяем соответствие типа файла и группы (целевой папки - container)
REGISTER_EXTENSION = {
    'JPEG': IMAGES,
    'PNG' : IMAGES,
    'JPG' : IMAGES,
    'SVG' : IMAGES,
    'AVI' : VIDEO, 
    'MP4' : VIDEO, 
    'MOV' : VIDEO, 
    'MKV' : VIDEO,
    'DOC' : DOCUMENTS, 
    'DOCX': DOCUMENTS, 
    'TXT' : DOCUMENTS, 
    'PDF' : DOCUMENTS, 
    'XLSX': DOCUMENTS, 
    'PPTX': DOCUMENTS,
    'MP3' : AUDIO,    
    'OGG' : AUDIO, 
    'WAV' : AUDIO, 
    'AMR' : AUDIO,
    'ZIP' : ARCHIVES,
    'GZ'  : ARCHIVES,
    'TAR' : ARCHIVES
}

# Определяем множества (set) для фиксирования неизвестных расширений файлов и обработанных известных
# (для анализа обработанных файлов)
UNKNOWN = set()
EXTENSION = set()

# Определяем список папок
FOLDERS = []

# Определяем расширение файла и перефодим в верхний регистр для последующего определения целевой папки
# например, jpg -> JPG
def get_extension(filename: str) -> str:
    return Path(filename).suffix[1:].upper() # [1:] - в суфиксе отсекаем точку

# Сканируем текущую папку и если встречаем папку, то проверяем ее на исключения, 
# и если она не в исключении, то проваливаемся в нее (рекурсия)
def scan(folder: Path) -> None:
    
    for item in folder.iterdir(): # проходимся по каждому элементу папки
        
        if item.is_dir(): # если элемент папка
            # Работа с папкой
            # Проверяем, чтобы папка не была целевой (исключение)
            if item.name not in ('images', 'video', 'documents', 'audio', 'archives', 'MY_OTHER'):
                FOLDERS.append(item) # добавляем в список папок
                scan(item)  # сканируем вложенную папку - рекурсия
            continue  # переходим к следующему элементу в сканированной папке
        
        else: # если элемент файл
            #  Работа с файлом
            ext = get_extension(item.name)  # расширение файла
            fullname = folder / item.name   # путь к файлу
            
            # Если расширение файла неизвесно или отсутствует, то добавляем к неизвестным,
            # иначе к добавляем к обработанным известным,
            if not ext:                   # если файл без расширения
                MY_OTHER.append(fullname) # добавляем в список неизвестных
            
            else:
                try:                                     # может упасть если нет в списке (можно сделать через get)
                    EXTENSION.add(ext)                   # добавляем расширение в список обработанных
                    container = REGISTER_EXTENSION[ext]  # определяем группу файлов
                    container.append(fullname)           # добавляем "путь к файлу" к группе файлов
                except KeyError:
                    # Если расширение не зарегистрировано в REGISTER_EXTENSION, то добавляем к неизвестным
                    UNKNOWN.add(ext)
                    MY_OTHER.append(fullname)

# Старт программы если запускаем отсюда
if __name__ == "__main__":
    # Если есть параметр с наименованием папки, которую надо обработать, то ...
    if len(sys.argv) > 1:
        # Определяем из параметров папку для сканирования
        folder_to_scan = sys.argv[1]
        # Информируем пользователя
        print(f'Start in folder {folder_to_scan}')
        # Запускаем сканирование (никаких действий по изменению не происходит)
        scan(Path(folder_to_scan))
        # Информируем пользователя о результатах
        print(f'Result:')
        print(f'   Images: {IMAGES}')
        print(f'   Video: {VIDEO}')
        print(f'   Documents: {DOCUMENTS}')
        print(f'   Audio: {AUDIO}')
        print(f'   Archives: {ARCHIVES}')
        print(f'   Other: {MY_OTHER}')
        print(f'   Known ​file extensions: {EXTENSION}')
        print(f'   Unknown files extensions: {UNKNOWN}')
