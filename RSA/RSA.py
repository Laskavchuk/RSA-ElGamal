import json
import math
import random
from sympy import isprime, mod_inverse
from collections import namedtuple

# Оголошення іменованого кортежу для публічного та приватного ключів
KeyPair = namedtuple('KeyPair', ['public_key', 'private_key'])
PublicKey = namedtuple('PublicKey', ['e', 'n'])
PrivateKey = namedtuple('PrivateKey', ['d', 'n'])


def generate_keypair(bits=2048):
    """
    Функція генерує приватний і публічний ключі
    :param bits: довжина ключа в бітах
    :return: приватний і публічний ключ
    """
    # Генеруємо два великі прості числа
    p = generate_large_prime(bits)
    q = generate_large_prime(bits)

    # Обчислюємо модуль n
    n = p * q

    # Обчислюємо функцію Ейлера (φ(n))
    phi_n = (p - 1) * (q - 1)

    # Вибираємо відкритий ключ e
    e = choose_public_exponent(phi_n)

    # Обчислюємо закритий ключ d
    d = mod_inverse(e, phi_n)

    # Створюємо і повертаємо іменований кортеж публічного та приватного ключів
    public_key = PublicKey(e=e, n=n)
    private_key = PrivateKey(d=d, n=n)

    return KeyPair(public_key=public_key, private_key=private_key)


def generate_large_prime(bits):
    """
    Функція генерує велике просте число з бібліотекою sympy
    :param bits: двожина числа в бітах
    :return: число
    """
    while True:
        number = random.getrandbits(bits)
        if isprime(number):
            return number


def choose_public_exponent(phi_n):
    """
    Функція вибирає відкритий ключ e, такий що 1 < e < φ(n) та gcd(e, φ(n)) = 1
    :param phi_n: Функція Ейлера для модуля n
    :return: Відкритий ключ e
    """
    while True:
        e = random.randint(2, phi_n - 1)
        if is_coprime(e, phi_n):
            return e


def is_coprime(a, b):
    """
    Функція реревіряє, чи є a та b взаємно простими
    :param a: число
    :param b: число
    :return: істину або хибність
    """
    return math.gcd(a, b) == 1


def rsa_encrypt(public_key, plain_text): # взято з https://dou.ua/forums/topic/43026/ # noqa
    """
    Функція шифрування тексту за допомогою вхідних параметрів
    :param public_key: публічний ключ
    :param plain_text: відкритий текст
    :return: зашифроване повідомлення
    """
    e, n = public_key
    return [pow(ord(char), e, n) for char in plain_text]


def rsa_decrypt(private_key, encrypted_text):  # взято з https://dou.ua/forums/topic/43026/ # noqa
    """
     Функція розшифрування тексту за допомогою вхідних параметрів
    :param private_key: приватний ключ
    :param encrypted_text: зашифроване повідомлення
    :return: розшифроване повідомлення
    """
    d, n = private_key
    decrypted_text = [chr(pow(char, d, n)) for char in encrypted_text]
    return ''.join(decrypted_text)


def save_keys():
    """
    Функція зберігання ключів
    """
    public_file = 'Public_key.json'
    with open(public_file, 'w') as fp:
        json.dump({'e': key_pair.public_key.e, 'n': key_pair.public_key.n}, fp)
    private_file = 'Private_key.json'
    with open(private_file, 'w') as fp:
        json.dump({'d': key_pair.private_key.d, 'n': key_pair.private_key.n}, fp)


def load_public_key():
    """
    Функція завантаження з файлу публічного ключа
    :return: публічний ключ
    """
    public_file = 'Public_key.json'
    with open(public_file, 'r') as fp:
        loaded_public_key = json.load(fp)
    return PublicKey(e=loaded_public_key['e'], n=loaded_public_key['n'])


def load_private_key():
    """
    Функція завантаження з файлу приватного ключа
    :return: приватний ключ
    """
    public_file = 'Private_key.json'
    with open(public_file, 'r') as fp:
        loaded_private_key = json.load(fp)
    return PrivateKey(d=loaded_private_key['d'], n=loaded_private_key['n'])


def save_encrypted_text(encrypt_text):
    """
    Функція збереження у файл зашифрованого повідомлення
    """
    encrypted_file = 'encrypted_text'
    with open(encrypted_file, 'w') as fp:
        for elem in encrypt_text:
            fp.write(str(elem) + '\n')


def read_encrypted_text(encrypted_file):
    """
    Функція зчитування з файлу зашифрованого повідомлення
    :param encrypted_file: файл із зашифрованим повідомленням
    :return: зашифроване повідомлення
    """
    with open(encrypted_file, 'r') as fp:
        encrypted = [int(line.strip()) for line in fp]
        return encrypted


def split_into_chunks(text, chunk_size):
    """
    Функція розбиття шифротексту на частини фіксованої довжини.
    :param text:зашифрований текст
    :param chunk_size: розмір фіксованого рядка
    :return:розбитий текст на частини
    """
    return [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]


# робота програми
key_pair = generate_keypair()
save_keys()
public_key = load_public_key()
private_key = load_private_key()
initial_text = input("Введіть відкритий текст: ")

encrypted_text_ = rsa_encrypt(public_key, initial_text)
save_encrypted_text(encrypted_text_)

encrypted_text = read_encrypted_text('encrypted_text')
chunk_size = 10
for chunk in split_into_chunks(encrypted_text, chunk_size):
    print("Зашифрований текст - ", chunk)

decrypted_text = rsa_decrypt(private_key, encrypted_text)
print("Початковий текст - ", initial_text)
print("Розшифрований текст - ", decrypted_text)
