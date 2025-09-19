from dotenv import load_dotenv
import os
import sys
from google import genai
import inspect

chave_api = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=chave_api)

# Pegue a referência para o método
get_method = client.models.get

# Veja a assinatura do método
print(inspect.signature(get_method))


help(client.models.get)

# Veja todos os métodos e atributos disponíveis
print(dir(client))

# Cheque se o método existe
if hasattr(client, "models") and hasattr(client.models, "generate_content"):
    print("O método generate_content está disponível!")
else:
    print("O método generate_content NÃO está disponível.")