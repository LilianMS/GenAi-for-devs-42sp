# Exemplo de definição e chamada de função com argumento em Python.
import sys

def greeting(name: str) -> None:
    print(f"Hello {name}")

if __name__ == "__main__":
    argc = len(sys.argv)

    if argc == 2:
        name = sys.argv[1]
        greeting(name)
    else:
        print("Usage: an argument is required.")
