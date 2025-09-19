# Exemplo de uso de biblioteca externa (cowsay) para imprimir mensagem personalizada.
import sys
import cowsay

def greeting(name: str) -> None:
    cowsay.cow(f"Hello {name}")

if __name__ == "__main__":
    argc = len(sys.argv)

    if argc == 2:
        name = sys.argv[1]
        greeting(name)
    else:
        print("Usage: an argument is required.")