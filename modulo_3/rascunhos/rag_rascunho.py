import os
import sys
import pickle
from dotenv import load_dotenv
from google import genai
from google.genai import types
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


# Configuração da API - aproveitada do ex01/ex02
API_CONFIG = {
    "model_name": "gemini-1.5-flash",
    "temperature": 0.7,
    "instruction": """Você é um especialista em informações sobre a empresa Orbit Motordrones. 
Baseie suas respostas apenas nas informações fornecidas no contexto. 
Seja preciso, claro e direto. Se a informação não estiver disponível no contexto, 
informe que não possui essa informação específica."""
}

def get_ia_response(ask, 
                    instruction=API_CONFIG["instruction"],
                    model_name=API_CONFIG["model_name"], 
                    temp=API_CONFIG["temperature"]):
    """Função aproveitada do ex01/ex02 para gerar respostas com Gemini"""
    try:
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            return "[Erro: GEMINI_API_KEY não encontrada no arquivo .env]"
        
        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(
            model=model_name,
            contents=ask,
            config=types.GenerateContentConfig(
                system_instruction=instruction,
                temperature=temp, 
                max_output_tokens=1024
            )
        )
        return response.text.strip()
    except Exception as e:
        if "Name or service not known" in str(e) or "Temporary failure in name resolution" in str(e):
            return "[Modo offline: Sem conectividade. Apenas informações recuperadas são mostradas acima.]"
        elif "API key" in str(e).lower():
            return "[Erro: API key inválida. Verifique sua GEMINI_API_KEY no arquivo .env]"
        else:
            return f"[Erro ao gerar resposta: {e}]"


def load_knowledge_base(file_path):
    """Carrega o arquivo de base de conhecimento"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = [line.strip() for line in f.readlines() if line.strip()]
        return lines
    except FileNotFoundError:
        print(f"Erro: Arquivo {file_path} não encontrado.")
        sys.exit(1)
    except Exception as e:
        print(f"Erro ao carregar arquivo: {e}")
        sys.exit(1)


def get_embeddings(texts, cache_file='embeddings.pkl'):
    """
    Gera ou carrega embeddings com cache - inspirado no exemplo fornecido
    e na estrutura do ex03
    """
    if os.path.exists(cache_file):
        with open(cache_file, 'rb') as f:
            data = pickle.load(f)
            return data['texts'], data['embeddings']
    else:
        # Usando o mesmo modelo do ex03
        model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")
        embeddings = model.encode(texts)
        
        # Salva cache
        with open(cache_file, 'wb') as f:
            pickle.dump({'texts': texts, 'embeddings': embeddings}, f)
        
        return texts, embeddings


def retrieve_relevant_lines(query, texts, embeddings, top_k=3):
    """
    Recupera as linhas mais relevantes - baseado na lógica do ex03
    """
    model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")
    query_embedding = model.encode([query])
    
    # Calcula similaridade - mesmo método do ex03
    scores = cosine_similarity(query_embedding, embeddings)[0]
    
    # Ordena e pega os top_k - adaptado do ex03
    top_indices = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:top_k]
    
    relevant_lines = []
    for i in top_indices:
        relevant_lines.append((texts[i], scores[i]))
    
    return relevant_lines


def generate_rag_response(query, relevant_lines):
    """
    Gera resposta RAG com prompt estruturado
    """
    # Formata o contexto recuperado
    context = "\n".join([f"- {line}" for line, _ in relevant_lines])
    
    # Prompt estruturado conforme solicitado
    prompt = f"""
Pergunta: {query}

Contexto recuperado da base de conhecimento da Orbit Motordrones:
{context}

Com base apenas nas informações fornecidas acima, responda à pergunta de forma clara e precisa.
"""
    
    return get_ia_response(prompt)


def main():
    # Carrega variáveis de ambiente
    load_dotenv()
    
    # Verifica argumentos - estrutura do ex03
    if len(sys.argv) < 2:
        print("Uso: python3 rag.py \"sua pergunta sobre a Orbit Motordrones\"")
        sys.exit(1)
    
    query = " ".join(sys.argv[1:]).strip()
    
    # Carrega base de conhecimento
    knowledge_file = "orbit_motordrones.txt"
    texts = load_knowledge_base(knowledge_file)
    
    # Gera/carrega embeddings
    texts, embeddings = get_embeddings(texts)
    
    # Recupera linhas relevantes
    relevant_lines = retrieve_relevant_lines(query, texts, embeddings, top_k=3)
    
    # Mostra linhas recuperadas
    print("---- Linhas relevantes recuperadas: ----")
    for line, score in relevant_lines:
        print(f"- {line}")
    print("----------------------------------------")
    
    # Gera resposta RAG
    response = generate_rag_response(query, relevant_lines)
    print(response)


if __name__ == "__main__":
    main()