# Exemplo de dicionário e iteração sobre chaves e valores em Python.
my_dict = {
    "item1": 1,
    "item2": 2,
    "item3": 3,
    "item4": 4
}

def print_dict():
    for i, n in my_dict.items():
        print(i, n)

if __name__ == "__main__":
    print_dict()