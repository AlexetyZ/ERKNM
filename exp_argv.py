from sys import argv


def use_dict(_dict):
    import json
    _dict = json.loads(str(_dict).replace("'", '"'))
    for k, v in _dict.items():
        print(k, v)


if __name__ == '__main__':
    argv1 = "{'some': 'some1'}"
    print(argv1)
    print(type(argv[1]), argv[1])
    use_dict(argv[1])

