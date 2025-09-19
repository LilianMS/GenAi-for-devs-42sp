from dotenv import load_dotenv
import sys
import os
from google import genai

API_CONFIG = {
    "model_name": "gemini-1.5-flash",
    "temperature": 1.0
}

# Exemplos para few shot prompting
EXAMPLES = [
    ("CPU", "unidade central de processamento"),
    ("RAM", "memória de acesso aleatório"),
    ("HTML", "linguagem de marcação de hipertexto"),
] 

def make_prompt(term):
    prompt = "Traduza o termo técnico de informática para português. Aplicando a técnica de few-shot prompting:\n"
    for termo, traducao in EXAMPLES:
        prompt += f"{termo} -> {traducao}\n"
    prompt += f"{term} ->"
    # print(prompt) # Debugging line
    return prompt

def get_ia_response(ask, model_name, temp=API_CONFIG["temperature"]):
    # print(f"Using model: {model_name} with temperature: {temp}") # Debug line
    try:
        chave_api = os.getenv("GEMINI_API_KEY")
        if not chave_api:
            return "Error: API key not set."
        client = genai.Client(api_key=chave_api)
        response = client.models.generate_content(
            model=model_name,
            contents=ask,
            config={"temperature": temp}
        )
        return response.text.strip()
    except Exception as e:
        return f"An error occurred: {e}"

# def get_ia_response(ask, model_name):
#     try:
#         chave_api = os.getenv("GEMINI_API_KEY")
#         if not chave_api:
#             return "Error: API key not set."
#         genai.configure(api_key=chave_api)
#         modelo = genai.GenerativeModel(model_name)
#         modelo.generation_config = genai.GenerationConfig(temperature=API_CONFIG["temperature"])
#         resposta = modelo.generate_content(ask)
#         return resposta.text.strip()
#     except Exception as e:
#         return f"An error occurred: {e}"


if __name__ == "__main__":
    load_dotenv()
    if len(sys.argv) < 2:
        print("Usage: python fewshot.py <termo>")
        sys.exit(1)
    term = " ".join(sys.argv[1:])
    prompt = make_prompt(term)
    response = get_ia_response(prompt, API_CONFIG["model_name"])
    print(response)