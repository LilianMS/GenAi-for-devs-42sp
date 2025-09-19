import os
from dotenv import load_dotenv
import sys
from google import genai
from google.genai import types

API_CONFIG = {
    "model_name": "gemini-1.5-flash",
    "temperature": 1.0,
    "instructions": f"""
    <instructions>
    Assuma o papel de um consultor de viagens, objetivo e especializado no destino solicitado.
    Retorne 5 nomes das melhores atrações para o destino recebido como input. Faça como no exemplo abaixo:
    </instructions>
    <examples>
    <input>Londres</input>
    <output>
    1. London Eye
    2. Torre de Londres
    3. Museu Britânico
    4. Palácio de Buckingham
    5. Big Ben
    </output>
    </examples>"""
}


def get_ia_response(ask,
                         model_name=API_CONFIG["model_name"],
                         temp=API_CONFIG["temperature"]):
    try:
        chave_api = os.getenv("GEMINI_API_KEY")
        client = genai.Client(api_key=chave_api)
        response = client.models.generate_content(
            model=model_name,
            contents=ask,
            config=types.GenerateContentConfig(
            system_instruction=API_CONFIG["instructions"],
            temperature=temp)
        )
        return response.text.strip()
    except Exception as e:
        return f"Ocorreu um erro: {e}"


if __name__ == "__main__":
    load_dotenv()
    if len(sys.argv) < 2:
        print("Usage: python roleplay.py <Qual o destino turístico?>")
        sys.exit(1)
    ask = " ".join(sys.argv[1:])
    response = get_ia_response(ask)
    print(response)