# Explicação Detalhada do Código - Chatbot com Persistência

Este documento explica em detalhes o código do chatbot com memória curta e longa, focando nos conceitos Python que podem ser novos.

## 1. Imports e Configurações

```python
import os
import sys
import sqlite3
from dotenv import load_dotenv
from google import genai
from google.genai import types
```

**Explicação dos imports:**
- `sqlite3`: Biblioteca nativa do Python para trabalhar com banco de dados SQLite
- `dotenv`: Carrega variáveis de ambiente do arquivo `.env` (para proteger chaves de API)
- `google.genai`: Biblioteca para usar a IA Gemini do Google
- `types`: Tipos específicos da biblioteca Google GenAI

## 2. Função `get_ia_response()` - Comunicação com IA

```python
def get_ia_response(ask,
                    instruction=API_CONFIG["instruction"],
                    model_name=API_CONFIG["model_name"],
                    temp=API_CONFIG["temperature"]):
```

### **Conceitos novos:**

#### **Parâmetros com valores padrão**
- Permite chamar a função com menos argumentos
- Exemplo: `get_ia_response("Olá")` usa os valores padrão
- Ou: `get_ia_response("Olá", temp=0.5)` sobrescreve apenas a temperatura

#### **Configuração da IA**
```python
config=types.GenerateContentConfig(
    system_instruction=instruction,
    temperature=temp, 
    max_output_tokens=1024
)
```
- `system_instruction`: Define a personalidade da IA
- `temperature`: Controla criatividade (0 = mais focado, 2 = mais criativo)
- `max_output_tokens`: Limita o tamanho da resposta

## 3. Funções de Banco de Dados

### **Padrão de conexão SQLite**
Todas as funções de banco seguem este padrão:
```python
conn = sqlite3.connect(DB_FILE)    # 1. Conecta
c = conn.cursor()                  # 2. Cria cursor
c.execute("SQL COMMAND")           # 3. Executa comando
conn.commit()                      # 4. Salva mudanças
conn.close()                       # 5. Fecha conexão
```

### `init_db()` - Criação das tabelas

```python
c.execute('''CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user TEXT,
                bot TEXT
            )''')
```

**Conceitos SQL importantes:**
- `IF NOT EXISTS`: Só cria se a tabela não existir
- `PRIMARY KEY AUTOINCREMENT`: ID único que aumenta automaticamente
- `TEXT`: Tipo de dados para strings

### `save_message()` - Salvando dados com segurança

```python
c.execute("INSERT INTO messages (user, bot) VALUES (?, ?)", (user, bot))
```

**Conceitos de segurança:**
- `(?, ?)`: Placeholders que previnem SQL injection
- `(user, bot)`: Tupla com os valores a serem inseridos
- **Nunca** concatene strings diretamente no SQL!

### `get_last_messages()` - Buscando e manipulando dados

```python
def get_last_messages(n=5):
    c.execute("SELECT user, bot FROM messages ORDER BY id DESC LIMIT ?", (n,))
    rows = c.fetchall()
    return rows[::-1]  # Inverte a ordem
```

**Conceitos novos:**

#### **`fetchall()`**
- Retorna uma lista de tuplas
- Cada tupla representa uma linha do banco
- Exemplo: `[('oi', 'olá'), ('tchau', 'até mais')]`

#### **Slice reverso `[::-1]`**
- Inverte a ordem de uma lista
- `[1, 2, 3][::-1]` → `[3, 2, 1]`
- Necessário porque buscamos do mais recente para o mais antigo, mas queremos exibir na ordem cronológica

#### **SQL `ORDER BY ... DESC LIMIT`**
- `ORDER BY id DESC`: Ordena do ID maior para o menor (mais recente primeiro)
- `LIMIT ?`: Limita quantos registros retornar

## 4. List Comprehension - Programação Funcional

```python
return [r[0] for r in rows[::-1]]
```

**Tradução linha por linha:**
- `rows[::-1]`: Pega a lista `rows` e inverte
- `for r in`: Para cada elemento `r` na lista
- `r[0]`: Pega o primeiro item de cada tupla
- `[...]`: Cria uma nova lista com os resultados

**Equivalente com loop tradicional:**
```python
result = []
for r in rows[::-1]:
    result.append(r[0])
return result
```

## 5. Manipulação de Strings Avançada

### `summarize()` - Construindo contexto

```python
context = "\n".join([f"User: {u}\nBot: {b}" for u, b in history[-10:]])
```

**Quebra da expressão:**

#### **Slice negativo `[-10:]`**
- Pega os últimos 10 elementos de uma lista
- `[1,2,3,4,5][-3:]` → `[3,4,5]`

#### **Desempacotamento de tupla `for u, b in`**
- Cada item de `history` é uma tupla `(user_msg, bot_msg)`
- `u` recebe a mensagem do usuário
- `b` recebe a mensagem do bot

#### **f-string com formatação**
- `f"User: {u}\nBot: {b}"` insere as variáveis na string
- `\n` adiciona quebra de linha

#### **`join()` method**
- `"\n".join(lista)` junta todos os elementos da lista com quebras de linha
- Exemplo: `"\n".join(["a", "b", "c"])` → `"a\nb\nc"`

## 6. Lógica Principal - `main()`

### **Verificação de primeira execução**
```python
if not get_user_turns():
    # Primeira vez que o usuário abre o chat
    response = get_ia_response("Apresente-se como meu amigo, Bob")
    save_message("", response)
```

**Conceito:**
- `not lista_vazia` retorna `True`
- Se não há mensagens anteriores, o bot se apresenta

### **Loop principal com controle de fluxo**
```python
while True:
    user_input = input("Q: ")
    if user_input.strip().lower() == "bye":
        break
```

**Métodos de string:**
- `strip()`: Remove espaços em branco do início e fim
- `lower()`: Converte para minúsculas
- Permite "bye", "BYE", " bye ", etc.

### **Construção inteligente do contexto**

```python
# Memória curta (últimas 5 mensagens)
short_memory = get_last_messages(5)
context = ""
for u, b in short_memory:
    context += f"User: {u}\nBot: {b}\n"

# Memória longa (resumos)
long_memory = get_last_summaries(10)
if long_memory:
    context = "\n".join([f"Resumo: {s}" for s in long_memory]) + "\n" + context
```

**Estratégia de memória:**
1. Pega as 5 mensagens mais recentes (contexto imediato)
2. Pega os 10 resumos mais recentes (contexto histórico)
3. Combina: resumos + mensagens recentes + nova pergunta

### **Sistema de resumos automáticos**
```python
user_turns = get_user_turns()
if len(user_turns) % 10 == 0 and user_turns:
    summary = summarize(user_turns, API_CONFIG["instruction_summary"])
    save_summary(summary)
```

**Conceitos matemáticos:**
- **Operador módulo `%`**: Resto da divisão
- `10 % 10 = 0`, `20 % 10 = 0`, `25 % 10 = 5`
- `len(user_turns) % 10 == 0`: Verifica se é múltiplo de 10
- **Operador `and`**: Ambas condições devem ser verdadeiras

### **Limpeza automática de dados antigos**
```python
if len(get_last_summaries(11)) > 10:
    c.execute("DELETE FROM summaries WHERE id NOT IN (SELECT id FROM summaries ORDER BY id DESC LIMIT 10)")
```

**SQL complexo:**
- `SELECT id FROM summaries ORDER BY id DESC LIMIT 10`: Pega IDs dos 10 resumos mais recentes
- `WHERE id NOT IN (...)`: Deleta todos os IDs que NÃO estão na lista dos 10 mais recentes
- Mantém apenas os 10 resumos mais recentes

## 7. Conceitos Python Importantes Aprendidos

### **1. Slices (Fatias de Lista)**
```python
lista = [1, 2, 3, 4, 5]
lista[-3:]     # [3, 4, 5] - últimos 3
lista[::-1]    # [5, 4, 3, 2, 1] - invertido
lista[1:4]     # [2, 3, 4] - do índice 1 ao 3
```

### **2. List Comprehension**
```python
# Forma compacta
numeros_pares = [x for x in range(10) if x % 2 == 0]

# Equivalente com loop
numeros_pares = []
for x in range(10):
    if x % 2 == 0:
        numeros_pares.append(x)
```

### **3. f-strings (Formatação de Strings)**
```python
nome = "João"
idade = 25
mensagem = f"Olá {nome}, você tem {idade} anos"
# Resultado: "Olá João, você tem 25 anos"
```

### **4. Métodos de String Úteis**
```python
texto = "  Olá Mundo  "
texto.strip()     # "Olá Mundo" - remove espaços
texto.lower()     # "  olá mundo  " - minúsculas
texto.upper()     # "  OLÁ MUNDO  " - maiúsculas

lista = ["a", "b", "c"]
"-".join(lista)   # "a-b-c" - junta com separador
```

### **5. Operadores Lógicos e Matemáticos**
```python
# Operador módulo
10 % 3 = 1    # resto da divisão
15 % 5 = 0    # sem resto (múltiplo)

# Operadores lógicos
True and False = False
True or False = True
not True = False
```

### **6. Context Management com Banco de Dados**
```python
# Padrão sempre seguido:
conn = sqlite3.connect("banco.db")  # Abre conexão
c = conn.cursor()                   # Cria cursor
try:
    c.execute("SQL")                # Executa comando
    conn.commit()                   # Salva mudanças
finally:
    conn.close()                    # SEMPRE fecha
```

### **7. Parâmetros de Função Flexíveis**
```python
def minha_funcao(obrigatorio, opcional="padrão", *args, **kwargs):
    pass

# Chamadas possíveis:
minha_funcao("valor")                    # usa padrão
minha_funcao("valor", "outro")           # sobrescreve padrão
minha_funcao("valor", opcional="novo")   # parâmetro nomeado
```

## 8. Fluxo Completo do Programa

1. **Inicialização**: Carrega variáveis, cria banco se não existir
2. **Primeira vez**: Bot se apresenta se não há histórico
3. **Loop principal**:
   - Usuário digita mensagem
   - Sistema busca contexto (memória curta + longa)
   - IA gera resposta baseada no contexto
   - Salva interação no banco
   - A cada 10 interações: cria resumo automático
   - Mantém apenas 10 resumos mais recentes
4. **Encerramento**: Usuário digita "bye"

## 9. Arquitetura de Memória

```
MEMÓRIA LONGA (Resumos)    +    MEMÓRIA CURTA (Últimas 5 msgs)
      ↓                              ↓
   Banco: summaries              Banco: messages
   (últimos 10 resumos)          (últimas 5 conversas)
      ↓                              ↓
      └──────────── CONTEXTO ────────────┘
                        ↓
                   IA GEMINI
                        ↓
                    RESPOSTA
```

Este sistema permite que o chatbot:
- Lembre de conversas antigas (resumos)
- Mantenha contexto imediato (últimas mensagens)
- Seja eficiente (não carrega todo o histórico)
- Persista entre sessões (banco de dados)

---

**Dica final**: Experimente modificar os valores (5 mensagens, 10 resumos, 10 interações) para ver como afeta o comportamento do bot!