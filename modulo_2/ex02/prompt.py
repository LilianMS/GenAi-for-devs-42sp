from dotenv import load_dotenv
import sys
import os
from google import genai

API_CONFIG = {
    "model_name": "gemini-1.5-flash",
    "temperature": 1.0
}

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


# def get_ia_response(ask, model_name, temp=1.0):
#     try:
#         chave_api = os.getenv("GEMINI_API_KE")
#         if not chave_api:
#             return "Error: API key not set."
#         genai.configure(api_key=chave_api)
#         modelo = genai.GenerativeModel(model_name)
#         modelo.generation_config = genai.GenerationConfig(temperature=temp)
#         resposta = modelo.generate_content(ask)
#         return resposta.text

#     except Exception as e:
#         return f"An error occurred: {e}"

def get_temperature(temp_str, default=1.0):
    try:
        temp = float(temp_str.replace(',', '.'))
        if 0.0 <= temp <= 2.0:
            return temp
        else:
            print("Temperature must be between 0.0 and 2.0. Using default value.")
            return default
    except ValueError:
        print(f"Invalid temperature '{temp_str}'. Using default ({default}).")
        return default

def print_result(ask, response, model_name, temp):
    print(f"Question: {ask}")
    if not response.startswith("An error occurred") and not response.startswith("Error:"):
        print(f"Response from {model_name}:")
    print("-" * 50)
    print(response)
    print("-" * 50)
    print(f"Model: {model_name}, Temperature: {temp}")


if __name__ == "__main__":
    load_dotenv()
    if len(sys.argv) < 2:
        print("Usage: python prompt.py '<question>' [temperature:0.0-2.0]")
        sys.exit(1)
    ask = sys.argv[1]
    model_name = API_CONFIG["model_name"]
    temp = get_temperature(sys.argv[2]) if len(sys.argv) > 2 else 1.0
    response = get_ia_response(ask, model_name, temp)

    print_result(ask, response, model_name, temp)

    
    # --------------------------------------------------------------------
    # Dependências necessárias para rodar este script:
    #
    # pip install python-dotenv google-genai
    #
    # Certifique-se de ativar o ambiente virtual antes de instalar e rodar.
    #