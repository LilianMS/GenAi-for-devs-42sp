import os
from dotenv import load_dotenv
import sys
from google import genai

API_CONFIG = {
    "model_name": "gemini-1.5-flash",
    "temperature": 1.0,
    "instructions": "Resuma o texto a seguir em no máximo 20 palavras, mantendo o sentido principal.",
    "input": "Durante a Idade Média, as universidades europeias surgiram como centros de conhecimento, reunindo estudiosos de diversas áreas. Elas desempenharam papel essencial na preservação e transmissão de saberes clássicos, além de estimular debates filosóficos e científicos que moldaram o pensamento ocidental e prepararam terreno para o Renascimento.",
    "output": "Universidades medievais preservaram saber clássico, promoveram debates e criaram base intelectual que impulsionou o Renascimento europeu."
}

def make_prompt(text, config=API_CONFIG):
    prompt = f"""<instructions>
    {config["instructions"]}
    </instructions>
    <examples>
    <input>
    {config["input"]}
    </input>
    <output>
    {config["output"]}
    </output>
    </examples>
    <text>
    {text}
    </text>"""
    return prompt

def get_ia_response(ask, model_name, temp=API_CONFIG["temperature"]):
    try:
        chave_api = os.getenv("GEMINI_API_KEY")
        client = genai.Client(api_key=chave_api)
        response = client.models.generate_content(
            model=model_name,
            contents=ask,
            config={"temperature": temp}
        )
        return response.text.strip()
    except Exception as e:
        return f"Ocorreu um erro: {e}"


if __name__ == "__main__":
    load_dotenv()
    if len(sys.argv) < 2:
        print("Usage: python xml.py <texto a ser resumido>")
        sys.exit(1)
    text = " ".join(sys.argv[1:])
    prompt = make_prompt(text)
    response = get_ia_response(prompt, API_CONFIG["model_name"])
    print(response)