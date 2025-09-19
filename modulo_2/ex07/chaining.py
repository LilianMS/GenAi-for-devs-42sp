import os
from dotenv import load_dotenv
import sys
from google import genai
from google.genai import types

API_CONFIG = {
    "model_name": "gemini-1.5-flash",
    "temperature": 1.0,
    "instruction": "Responda de forma concisa e clara.",
    "instruction_1": """Gere uma descrição detalhada do produto de interesse do usuário recebido no input.""",
    "instruction_2": """Seja criativo, inteligente e crie um único anúncio publicitário, usando como referência a descrição do produto recebida. Não inclua explicações, comentários ou outras opções.""",
    "instruction_3": """Traduza o anúncio publicitário recebido para o inglês."""
}

def get_ia_response(ask, instruction=API_CONFIG["instruction"],
                         model_name=API_CONFIG["model_name"],
                         temp=API_CONFIG["temperature"]):
    try:
        chave_api = os.getenv("GEMINI_API_KEY")
        client = genai.Client(api_key=chave_api)
        response = client.models.generate_content(
            model=model_name,
            contents=ask,
            config=types.GenerateContentConfig(
            system_instruction=instruction,
            temperature=temp, max_output_tokens=1024
            )
        )
        return response.text.strip()
    except Exception as e:
        return f"Ocorreu um erro: {e}"

def print_response(response="", title=""):
    if not response:
        print("Nenhuma resposta recebida.")
        return 1
    if response.startswith("Ocorreu um erro"):
        return 2
    if title:
        print(f"\n{title}")
    print("-" * 50)
    print(response)
    print("-" * 50)
    return 0

def set_data_instructions(ask):
    if not ask:
        print("Por favor, forneça um produto para gerar as respostas.")
        return
    response1 = get_ia_response(ask, API_CONFIG["instruction_1"])
    print_response(response1, "Descrição detalhada do produto")

    response2 = get_ia_response(response1, API_CONFIG["instruction_2"]) if response1 and not response1.startswith("Ocorreu um erro") else None
    print_response(response2, "Anúncio publicitário")

    response3 = get_ia_response(response2, API_CONFIG["instruction_3"]) if response2 and not response2.startswith("Ocorreu um erro") else None
    print_response(response3, "Tradução para o inglês")
 

if __name__ == "__main__":
    load_dotenv()
    if len(sys.argv) < 2:
        print("Usage: python chaining.py <Um produto>")
        sys.exit(1)
    ask = " ".join(sys.argv[1:])
    set_data_instructions(ask)