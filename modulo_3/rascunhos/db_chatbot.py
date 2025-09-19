import os
import sys
import sqlite3
from dotenv import load_dotenv
from google import genai
from google.genai import types

DB_FILE = "chatbot.db"

API_CONFIG = {
    "model_name": "gemini-1.5-flash",
    "temperature": 1.0,
    "instruction": "Seja como um amigo simpático e extrovertido. Mas não revele que é uma IA. Use emojis nas respostas. Evite respostas muito longas.",
    "instruction_summary": "Resuma de forma breve e objetiva as interações a seguir para memória de longo prazo. Foque nos temas principais, decisões tomadas e sentimentos expressos."
}

def get_ia_response(ask,
                    instruction=API_CONFIG["instruction"],
                    model_name=API_CONFIG["model_name"],
                    temp=API_CONFIG["temperature"]):
    try:
        api_key = os.getenv("GEMINI_API_KEY")
        client = genai.Client(api_key=api_key)
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
        return f"[Erro ao gerar resposta: {e}]"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user TEXT,
                    bot TEXT
                )''')
    c.execute('''CREATE TABLE IF NOT EXISTS summaries (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    summary TEXT
                )''')
    conn.commit()
    conn.close()

def save_message(user, bot):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("INSERT INTO messages (user, bot) VALUES (?, ?)", (user, bot))
    conn.commit()
    conn.close()

def get_last_messages(n=5):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT user, bot FROM messages ORDER BY id DESC LIMIT ?", (n,))
    rows = c.fetchall()
    conn.close()
    return rows[::-1]  # reverse to chronological order

def get_user_turns():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT user, bot FROM messages WHERE TRIM(user) != ''")
    rows = c.fetchall()
    conn.close()
    return rows

def save_summary(summary):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("INSERT INTO summaries (summary) VALUES (?)", (summary,))
    conn.commit()
    conn.close()

def get_last_summaries(n=10):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT summary FROM summaries ORDER BY id DESC LIMIT ?", (n,))
    rows = c.fetchall()
    conn.close()
    return [r[0] for r in rows[::-1]]

def summarize(history, instruction):
    context = "\n".join([f"User: {u}\nBot: {b}" for u, b in history[-10:]])
    resumo = get_ia_response(context, instruction)
    return resumo

def main():
    load_dotenv()
    init_db()
    print("Chatbot Gemini (digite 'bye' para encerrar)")
    if not get_user_turns():
        response = get_ia_response("Apresente-se como meu amigo, Bob", API_CONFIG["instruction"])
        print(f"Bob: {response}")
        save_message("", response)

    while True:
        user_input = input("Q: ")
        if user_input.strip().lower() == "bye":
            break
        short_memory = get_last_messages(5)
        context = ""
        for u, b in short_memory:
            context += f"User: {u}\nBot: {b}\n"
        context += f"User: {user_input}\nBot: "
        long_memory = get_last_summaries(10)
        if long_memory:
            context = "\n".join([f"Resumo: {s}" for s in long_memory]) + "\n" + context
        print("Bob is typing...")
        bot_reply = get_ia_response(context, API_CONFIG["instruction"])
        print(f"Bob: {bot_reply}")
        save_message(user_input, bot_reply)
        user_turns = get_user_turns()
        if len(user_turns) % 10 == 0 and user_turns:
            summary = summarize(user_turns, API_CONFIG["instruction_summary"])
            save_summary(summary)

            if len(get_last_summaries(11)) > 10:
                conn = sqlite3.connect(DB_FILE)
                c = conn.cursor()
                c.execute("DELETE FROM summaries WHERE id NOT IN (SELECT id FROM summaries ORDER BY id DESC LIMIT 10)")
                conn.commit()
                conn.close()

if __name__ == "__main__":
    main()
