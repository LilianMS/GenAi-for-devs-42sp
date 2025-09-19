# Explicação do Projeto RAG (Retrieval-Augmented Generation)

## Índice
1. [O que é RAG?](#o-que-é-rag)
2. [Como os exercícios se conectam](#como-os-exercícios-se-conectam)
3. [Análise detalhada do código](#análise-detalhada-do-código)
4. [Biblioteca Pickle](#biblioteca-pickle)
5. [Fluxo completo do programa](#fluxo-completo-do-programa)

---

## O que é RAG?

**RAG (Retrieval-Augmented Generation)** é uma técnica que combina:
- **Busca inteligente** (Retrieval): Encontra informações relevantes em uma base de conhecimento
- **Geração de texto** (Generation): Usa IA para criar respostas naturais baseadas nas informações encontradas

**Vantagem principal**: A IA responde apenas com base em informações específicas fornecidas, evitando "alucinações" (respostas inventadas).

---

## Como os exercícios se conectam

### Ex01 - Chatbot Básico
```python
def get_ia_response(ask, instruction, model_name, temp):
```
- Função base para comunicação com IA
- Usada no RAG para gerar respostas contextualizadas

### Ex02 - Persistência 
```python
def get_embeddings(texts, cache_file='embeddings.pkl'):
```
- Conceito de salvar dados para reutilização
- No RAG: salva embeddings em cache para acelerar execuções

### Ex03 - Embeddings
```python
query_embedding = model.encode([query])
scores = cosine_similarity(query_embedding, embeddings)[0]
```
- Busca semântica por similaridade
- No RAG: encontra as linhas mais relevantes do arquivo

### Ex04 - RAG (Combinação de tudo)
- Une busca inteligente + IA generativa + persistência
- Cria um especialista em um assunto específico

---

## Análise detalhada do código

### 1. Carregamento da base de conhecimento
```python
def load_knowledge_base(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]
    return lines
```
**O que faz:**
- Lê arquivo de texto linha por linha
- Remove espaços em branco (`strip()`)
- Ignora linhas vazias (`if line.strip()`)
- Cada linha vira um "documento" pesquisável

### 2. Cache de embeddings
```python
def get_embeddings(texts, cache_file='embeddings.pkl'):
    if os.path.exists(cache_file):
        # Carrega embeddings já calculados
        with open(cache_file, 'rb') as f:
            data = pickle.load(f)
            return data['texts'], data['embeddings']
    else:
        # Calcula embeddings pela primeira vez
        model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")
        embeddings = model.encode(texts)
        # Salva para próximas execuções
        with open(cache_file, 'wb') as f:
            pickle.dump({'texts': texts, 'embeddings': embeddings}, f)
        return texts, embeddings
```
**O que faz:**
- **Primeira execução**: Calcula embeddings e salva
- **Execuções seguintes**: Carrega embeddings do cache
- **Resultado**: Programa muito mais rápido após primeira execução

### 3. Busca semântica
```python
def retrieve_relevant_lines(query, texts, embeddings, top_k=3):
    model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")
    query_embedding = model.encode([query])
    scores = cosine_similarity(query_embedding, embeddings)[0]
    top_indices = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:top_k]
    relevant_lines = []
    for i in top_indices:
        relevant_lines.append((texts[i], scores[i]))
    return relevant_lines
```
**O que faz:**
- Gera embedding da pergunta do usuário
- Compara com embeddings de todas as linhas do arquivo
- Retorna as 3 linhas mais similares (maior score)

### 4. Geração de resposta contextualizada
```python
def generate_rag_response(query, relevant_lines):
    context = "\n".join([f"- {line}" for line, _ in relevant_lines])
    prompt = f"""
Pergunta: {query}

Contexto recuperado da base de conhecimento:
{context}

Com base apenas nas informações fornecidas acima, responda à pergunta de forma clara e precisa.
"""
    return get_ia_response(prompt)
```
**O que faz:**
- Monta prompt com pergunta + informações relevantes
- Instrui a IA a responder APENAS com base no contexto
- Envia para modelo de IA e retorna resposta

---

## Biblioteca Pickle

### O que é?
`pickle` é uma biblioteca padrão do Python que "serializa" objetos, convertendo-os em formato binário para salvar em arquivo.

### Por que usar no RAG?
**Problema**: Calcular embeddings demora muito tempo
```python
embeddings = model.encode(texts)  # Pode demorar minutos!
```

**Solução**: Salvar embeddings calculados e reutilizar
```python
# Salvar
pickle.dump({'texts': texts, 'embeddings': embeddings}, file)

# Carregar
data = pickle.load(file)
```

### Formato dos dados salvos
```python
data = {
    'texts': ['linha 1', 'linha 2', 'linha 3', ...],      # Lista de strings
    'embeddings': [[0.1, 0.2, ...], [0.3, 0.4, ...]]     # Array NumPy de vetores
}
```

### Vantagens do pickle
- ✅ **Velocidade**: Evita recalcular embeddings
- ✅ **Automático**: Funciona com qualquer objeto Python
- ✅ **Binário**: Arquivos menores que JSON/texto
- ✅ **Nativo**: Biblioteca padrão do Python

### Desvantagens do pickle
- ❌ **Específico do Python**: Só funciona em Python
- ❌ **Versão**: Pode não funcionar entre versões diferentes
- ❌ **Segurança**: Não abrir arquivos pickle de fontes não confiáveis

### Exemplo prático de performance
```
Primeira execução (sem cache):
- Calcular embeddings: 30 segundos
- Buscar resposta: 2 segundos
- Total: 32 segundos

Execuções seguintes (com cache):
- Carregar embeddings: 0.1 segundos
- Buscar resposta: 2 segundos
- Total: 2.1 segundos

Aceleração: 15x mais rápido!
```

---

## Fluxo completo do programa

### 1. Entrada do usuário
```bash
python3 rag.py "Como funciona a manutenção dos drones?"
```

### 2. Carregamento da base de conhecimento
- Lê arquivo `orbit_motordrones.txt`
- Cada linha vira um documento pesquisável

### 3. Embeddings (com cache)
- **Se existe cache**: Carrega embeddings salvos (rápido)
- **Se não existe**: Calcula e salva embeddings (lento na primeira vez)

### 4. Busca semântica
- Gera embedding da pergunta
- Calcula similaridade com todas as linhas
- Seleciona as 3 mais relevantes

### 5. Geração de resposta
- Monta prompt com pergunta + contexto
- Envia para IA (Gemini)
- Recebe resposta baseada apenas no contexto

### 6. Saída
```
---- Linhas relevantes recuperadas: ----
- Os drones requerem manutenção preventiva a cada 50 horas de voo
- A equipe técnica realiza inspeções completas mensalmente
- Peças de reposição estão disponíveis com garantia de 2 anos
----------------------------------------

A manutenção dos drones da Orbit Motordrones segue um cronograma rigoroso...
```

---

## Conclusão

O projeto RAG demonstra como combinar diferentes tecnologias:
- **Busca semântica**: Para encontrar informações relevantes
- **IA generativa**: Para respostas naturais e contextualizadas  
- **Cache/Persistência**: Para otimização de performance
- **Base de conhecimento**: Para especialização em um domínio

Resultado: Um chatbot especialista, rápido e confiável, que responde apenas com base em informações verificadas!