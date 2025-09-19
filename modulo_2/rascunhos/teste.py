from dotenv import load_dotenv
import os
import google.generativeai as genai

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
print(f"API KEY carregada: {api_key is not None}")

if not api_key:
    print("Erro: GEMINI_API_KEY não encontrada no ambiente.")
    exit(1)

try:
    genai.configure(api_key=api_key)
    modelo = genai.GenerativeModel("gemini-2.5-flash")
    resposta = modelo.generate_content("Diga olá, Gemini!")
    print("Resposta da API:", resposta.text)
except Exception as e:
    print("Erro ao chamar a API:", e)