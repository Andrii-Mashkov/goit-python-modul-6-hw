"""
Функция normalize:
    Проводит транслитерацию кириллического алфавита на латинский.
    Заменяет все символы кроме латинских букв, цифр на '_'.

Требования к функции normalize:
    Принимает на вход строку и возвращает строку;
    Проводит транслитерацию кириллических символов на латиницу;
    Транслитерация может не соответствовать стандарту, но быть читабельной;
    Большие буквы остаются большими, а меленькие — маленькими после транслитерации;
    Заменяет все символы, кроме букв латинского алфавита и цифр, на символ '_'.
"""
import re

# Строка с алфавитом (исходные значения) для транслитерации
CYRILLIC_SYMBOLS = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ'
# Кортеж (tuple) для целевых значений транслитерации
TRANSLATION = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
               "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "u", "ja", "je", "ji", "g")
# Словарь для значений
TRANS = {}
# Итерируемся одновременно по двум последовательностям и заполняем словарь
for c, l in zip(CYRILLIC_SYMBOLS, TRANSLATION):
    TRANS[ord(c)] = l                   # для нижнего регистра
    TRANS[ord(c.upper())] = l.upper()   # для верхнего регистра

def normalize(name: str) -> str:
    t_name = name.translate(TRANS)       # переводим по нашему словарю кирилицу на латиницу
    t_name = re.sub(r'[^a-zA-Z0-9.]', '_', t_name)  # заменяем все кроме латиницы, цифр и точки на подчеркивание
    return t_name

