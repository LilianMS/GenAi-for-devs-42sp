import json
import os
from dotenv import load_dotenv
import sys
from google import genai
from google.genai import types
from pydantic import BaseModel

API_CONFIG = {
    "model_name": "gemini-1.5-flash",
    "temperature": 1.0,
    "instructions": """
Você é um extrator de informações. Dado um texto, extraia e retorne dados em JSON, sem explicações ou comentários:

"""
}

class Person(BaseModel):
    nome: str
    idade: int
    profissão: str
    cidade: str

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
            temperature=temp, response_mime_type="application/json",
            response_schema=Person)
        )
        return response.text.strip()
    except Exception as e:
        return f"Ocorreu um erro: {e}"


def format_output(person: Person) -> str:
    return (f"Nome: {person.nome}\n"
            f"Idade: {person.idade}\n"
            f"Profissão: {person.profissão}\n"
            f"Cidade: {person.cidade}\n")


if __name__ == "__main__":
    load_dotenv()
    if len(sys.argv) < 2:
        print("Usage: python structured.py <Fatos sobre uma pessoa>")
        sys.exit(1)
    ask = " ".join(sys.argv[1:])
    response = get_ia_response(ask)

    print(response)

    # data = json.loads(response)
    # print(json.dumps(data, indent=4, ensure_ascii=False))
       
   
    # try:
    #     data = json.loads(response)
    #     person = Person.model_validate(data)
    #     output = format_output(person)
    #     print(output)
    # except Exception as e:
    #     print(f"Erro ao processar a resposta: {e}")


# Sugestão de teste: 
#     Roberto mora em sertaozinho gosta de fruta acorda cedinho para dirigir seu caminhão que é seu trabalho mas ele adorajá faz isso há 30 anos dos seus 50 anos de vida.