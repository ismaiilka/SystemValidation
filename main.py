from hashlib import sha256
import string

ALPHABET_PASSWORD = string.ascii_letters + string.digits
MIN_LENGTH_PASSWORD = 8
# Функция для наличия необходимых символов в пароле
AT_LEAST_ONE = lambda x: x.isdigit()


class BadCharacterError(Exception):
    pass


class StartsWithDigitError(Exception):
    pass


class CyrillicError(Exception):
    pass


class CapitalError(Exception):
    pass


class MinLengthError(Exception):
    pass


class PossibleCharError(Exception):
    pass


class NeedCharError(Exception):
    pass


def user_validation(*args, **kwargs):
    """Система валидации пользователя"""
    # Данная функция принимает только три аргумента: фамилию, имя и username
    # Проверка, есть ли неименованные аргументы, их нужно отрабасывать

    if len(args) > 0:
        raise KeyError()

    # Вытаскиваем именованные нужные аргументы, если есть лишнее или нет необходимого, кидаем исключение

    for key, value in kwargs.items():
        if key not in ('last_name', 'first_name', 'username'):
            raise KeyError()
    last_name, first_name, username = kwargs['last_name'], kwargs['first_name'], kwargs['username']

    # Все аргументы должны быть строками

    if not isinstance(last_name, str) or not isinstance(first_name, str) or not isinstance(username, str):
        raise TypeError()

    # Фамилия и имя должны состоять из кириллицы и начинаться с заглавной буквы

    alphabet_name = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
    alphabet_username = string.ascii_letters + string.digits + '_'
    for symbol in last_name.lower():
        if symbol not in alphabet_name:
            raise CyrillicError
    if not last_name.istitle():
        raise CapitalError
    for symbol in first_name.lower():
        if symbol not in alphabet_name:
            raise CyrillicError
    if not first_name.istitle():
        raise CapitalError

    # username должен состоять из буквы латинского алфавита либо из цифр, но не начинаться с цифры

    for char in username:
        if char not in alphabet_username:
            raise BadCharacterError()
    if username[0].isdigit():
        raise StartsWithDigitError()

    # Возвращаем результат в виде словаря

    return {'last_name': last_name, 'first_name': first_name, 'username': username}


def password_validation(password):
    """Система валидации пароля"""
    if not isinstance(password, str):
        raise TypeError()
    if len(password) < MIN_LENGTH_PASSWORD:
        raise MinLengthError()
    for char in password:
        if char not in ALPHABET_PASSWORD:
            raise PossibleCharError()
    for char in password:
        if AT_LEAST_ONE(char):
            return sha256(password.encode('utf-8')).hexdigest()
    raise NeedCharError()
