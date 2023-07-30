"""
Скрипт проходит по указанной во время вызова папке и обрабатывает содержимое.
В процессе работы:
    Переносит:
        изображения в папку images;
        видео файлы в video;
        документы в папку documents;
        звуковые файлы в audio;
        архивы (распаковываются и их содержимое) в папку archives.
    Все файлы и папки переименовываются при помощи функции normalize
    Расширения файлов не изменяются после переименования.
    Пустые папки удаляются.
    Скрипт игнорирует папки archives, video, audio, documents, images.
    Распакованное содержимое архива переносится в папку archives в подпапку, 
    названную точно так же, как и архив, но без расширения в конце.
    Файлы, расширения которых неизвестны, остаются без изменений.
"""

from pathlib import Path
import shutil
import sys
import file_parser as parser
from normalize import normalize

def handle_media(filename: Path, target_folder: Path) -> None:
    # Создаем папку для известного если ее нет
    target_folder.mkdir(exist_ok=True, parents=True)             # не падать, если такая папка есть; папка может содержать вложенные папки
    # Нормализуем наименование и перезаписываем по новому пути
    filename.replace(target_folder / normalize(filename.name))

# Изменено согласно условию "Файлы, расширения которых неизвестны, остаются без изменений."
"""
# обрабатываем неизвестное 
def handle_other(filename: Path, target_folder: Path) -> None:
    # создаем папку для неизвестного если ее нет
    target_folder.mkdir(exist_ok=True, parents=True)
    # Нормализуем наименование и перезаписываем по новому пути
    filename.replace(target_folder / normalize(filename.name))
"""

# Обрабатываем архив (создаем папку и распаковываем)
def handle_archive(filename: Path, target_folder: Path) -> None:
    # создаем папку для архивов если ее нет
    target_folder.mkdir(exist_ok=True, parents=True)
    # определяем и нормализуем наименование папки без разширения для текущего архива
    folder_for_file = target_folder / normalize(filename.name.replace(filename.suffix, '')) 
    # создаем папку для текущего архива (если ее нет)
    folder_for_file.mkdir(exist_ok=True, parents=True)
    # Пробуем распаковать архив
    try:
        # распаковываем архив в папку с таким же именем без расштрения
        shutil.unpack_archive(filename, folder_for_file)
    except shutil.ReadError:    # если неудача
        folder_for_file.rmdir() # удаляем папку 
    filename.unlink()           # удаляем архив

# Обрабатываем папку (удаляем пустую)
def handle_folder(folder: Path):
    try:
        folder.rmdir()          # удаляем папку
    except OSError:             # если неудача
        print(f"Can't delete folder: {folder}") # сообщение пользователю

# Основная часть скрипта
def main(folder: Path):
    # Сканируем папку
    parser.scan(folder)
    # если расширение файла пападает в список расширений изображений
    for file in parser.IMAGES:
        handle_media(file, folder / 'images')
    # если расширение файла пападает в список расширений видео
    for file in parser.VIDEO:
        handle_media(file, folder / 'video')
    # если расширение файла пападает в список расширений документов
    for file in parser.DOCUMENTS:
        handle_media(file, folder / 'documents')
    # если расширение файла пападает в список расширений звуковых файлов
    for file in parser.AUDIO:
        handle_media(file, folder / 'audio')
    # если расширение файла пападает в список расширений архивов
    for file in parser.ARCHIVES:
        handle_media(file, folder / 'archives')
    
    # Изменено согласно условию "Файлы, расширения которых неизвестны, остаются без изменений."
    """
    # если расширение файла пападает в список файлов с неизвестными расширениями
    for file in parser.MY_OTHER:
        handle_media(file, folder / 'MY_OTHER')
    """

    # пройтись по папкам и обработать их (удалить пустые)
    for folder in parser.FOLDERS[::-1]:
        handle_folder(folder)

# Старт скрипта
if __name__ == "__main__":
    # Если есть параметр с наименованием папки, которую надо обработать, то ...
    if sys.argv[1]:
        # Определяем путь папки для сканирования
        folder_for_scan = Path(sys.argv[1])
        # Информируем пользователя
        print(f'Start in folder: {folder_for_scan.resolve()}')
        # Запускаем основную часть скрипта
        # resolve - делает путь абсолютным, разрешая все символические ссылки на пути, а также нормализует его
        main(folder_for_scan.resolve())
