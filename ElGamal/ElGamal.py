# за основу взятий код з https://www.geeksforgeeks.org/elgamal-encryption-algorithm/?ref=lbp # noqa
import random


def gcd(a, b):
    """
    Функція Обчислює найбільший спільний дільник (НСД) двох чисел
    за евклідовим алгоритмом
    :param a: переше число
    :param b: друге число
    :return: НСД чисел a та b
    """
    if a < b:
        return gcd(b, a)
    elif a % b == 0:
        return b
    else:
        return gcd(b, a % b)


def gen_key(q):
    """
    Функція генерує випадковий ключ, який є співпростим з заданим числом 'q'
    :param q: натуральне число
    :return: Випадковий ключ, який є співмножником q
    """
    key = random.randint(2, q - 1)
    while gcd(q, key) != 1:
        key = random.randint(2, q - 1)
    return key


def power(a, b, c):
    """
    Функція обчислює модульне піднесення до степеня (a^b mod c),
    використовуючи алгоритм двійкового піднесення до степеня.
    :param a: основа
    :param b: показник степеня
    :param c: модуль
    :return: Результат a^b mod c
    """
    x = 1
    y = a

    while b > 0:
        if b % 2 != 0:
            x = (x * y) % c
        y = (y * y) % c
        b = int(b / 2)

    return x % c


def save_key_to_file(filename, key):
    """
    Функція зберігання ключа
    :param filename: назва файлу, куди зберегти ключ
    :param key: ключ
    """
    with open(filename, 'w') as file:
        file.write(str(key))


def read_key_from_file(filename):
    """
    Функція завантаження з файлу  ключа
    :param filename: назва файлу, з якого завантажується ключ
    :return: ключ
    """
    with open(filename, 'r') as file:
        return int(file.read())


def encrypt(msg, q, h, g):
    """
    Функція шифрує задане повідомлення за допомогою алгоритму
    шифрування ElGamal
    :param msg: повідомлення, яке потрібно зашифрувати
    :param q: просте число
    :param h: компонент публічного ключа
    :param g: генератор для циклічної групи за модулем q
    :return: кортеж, що містить зашифроване повідомлення та проміжне значення
    """
    en_msg = []

    k = gen_key(q)
    s = power(h, k, q)
    p = power(g, k, q)

    for i in range(0, len(msg)):
        en_msg.append(msg[i])

    print("g^k used:", p)
    print("g^ak used:", s)

    encrypted_msg = [s * ord(char) for char in en_msg]

    return encrypted_msg, p


def decrypt(en_msg, p, key, q):
    """
    Функція розшифровує зашифроване повідомлення за допомогою
    алгоритму ElGamal
    :param en_msg: зашифроване повідомлення
    :param p: проміжне значення
    :param key: закритий ключ
    :param q: просте число
    :return: розшифроване повідомлення у вигляді списку символів
    """
    dr_msg = []
    h = power(p, key, q)

    for i in range(0, len(en_msg)):
        dr_msg.append(chr(int(en_msg[i] / h)))

    return dr_msg


def main():
    """
    Основна функція, яка організовує процес шифрування та дешифрування ElGamal.
    """
    msg = input("Введіть відкритий текст: ")
    print("Початковий текст:", msg)

    q = random.randint(2 ** 24, 2 ** 25)
    g = random.randint(2, q)

    key_filename = "public_key.txt"
    private_key_filename = "private_key.txt"

    key = gen_key(q)
    h = power(g, key, q)

    save_key_to_file(key_filename, h)
    save_key_to_file(private_key_filename, key)

    print("g used:", g)
    print("g^a used:", h)

    en_msg, p = encrypt(msg, q, h, g)

    line_length = 50
    encrypted_str = ' '.join([str(num) for num in en_msg])
    encrypted_lines = [encrypted_str[i:i + line_length] for i in
                       range(0, len(encrypted_str), line_length)]

    print("Зашифрований текст - ")
    for line in encrypted_lines:
        print(line)
    en_msg = input('Введіть зашифроване повідомлення: ')
    en_msg_list = [int(num) for num in en_msg.split()]
    decrypted_msg = decrypt(en_msg_list, p,
                            read_key_from_file(private_key_filename), q)
    dmsg = ''.join(decrypted_msg)
    print("Розшифрований текст - ", dmsg)


if __name__ == '__main__':
    main()

