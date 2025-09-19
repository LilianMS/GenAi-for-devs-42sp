# Exemplo de leitura e validação de argumentos de linha de comando usando sys.argv.
import sys

num_args = len(sys.argv)

if num_args == 2:
    print(sys.argv[1])
elif num_args > 2:
    print("Error: only one argument is required.")
else:
    print("Usage: an argument is required.")
