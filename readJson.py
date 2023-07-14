def encode_string(string):
    from urllib.parse import unquote, quote
    return quote(string, encoding='cp1251')


if __name__ == '__main__':
    string = input('введите текст')
    print(encode_string(string))
