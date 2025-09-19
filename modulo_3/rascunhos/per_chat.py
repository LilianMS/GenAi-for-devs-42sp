import os
import sys
import json
from dotenv import load_dotenv
from google import genai
from google.genai import types

HISTORY_FILE = "chat_history.json"
SUMMARY_FILE = "chat_summaries.json"

API_CONFIG = {
    "model_name": "gemini-1.5-flash",
    "temperature": 1.0,
    "instruction": "Seja como um amigo simpático e extrovertido. Mas não revele que é uma IA. Use emojis nas respostas. Evite respostas muito longas.",
}

def get_ia_response(ask,
					instruction=API_CONFIG["instruction"],
                    model_name=API_CONFIG["model_name"],
                    temp=API_CONFIG["temperature"]):
    try:
        api_key = os.getenv("GOOGLE_API_KEY")
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


def load_json(filename, default):
	if os.path.exists(filename):
		try:
			with open(filename, 'r', encoding='utf-8') as f:
				return json.load(f)
		except Exception:
			return default
	return default

def save_json(filename, data):
	with open(filename, 'w', encoding='utf-8') as f:
		json.dump(data, f, ensure_ascii=False, indent=2)

def summarize(history, instruction):
	# Gera um resumo das últimas 10 interações
	context = "\n".join([f"User: {u}\nBot: {b}" for u, b in history[-10:]])
	prompt = f"Resuma de forma breve e objetiva as interações a seguir para memória de longo prazo:\n{context}"
	resumo = get_ia_response(prompt, instruction)
	return resumo


def main():

	# Carrega histórico e resumos
	history = load_json(HISTORY_FILE, [])
	summaries = load_json(SUMMARY_FILE, [])

	print("Chatbot Gemini (digite 'bye' para encerrar)")
	if not history:
		response = get_ia_response("Apresente-se como meu amigo, Bob", API_CONFIG["instruction"])
		print(f"Bob: {response}")
		history.append(("", response))
		save_json(HISTORY_FILE, history)

	while True:
		user_input = input("Q: ")
		if user_input.strip().lower() == "bye":
			break

		# Memória de curto prazo: últimas 5 mensagens
		short_term = history[-5:] if len(history) >= 5 else history
		context = ""
		for u, b in short_term:
			context += f"User: {u}\nBot: {b}\n"
		context += f"User: {user_input}\nBot: "

		# Memória de longo prazo: últimos 10 resumos
		long_term = summaries[-10:] if len(summaries) > 0 else []
		if long_term:
			context = "\n".join([f"Resumo: {s}" for s in long_term]) + "\n" + context

		print("Bob is typing...")
		bot_reply = get_ia_response(context, API_CONFIG["instruction"])
		print(f"Bob: {bot_reply}")
		history.append((user_input, bot_reply))
		save_json(HISTORY_FILE, history)

		# A cada 10 interações do User, gera resumo
		user_turns = [h for h in history if h[0].strip()]
		if len(user_turns) % 10 == 0:
			resumo = summarize(history, API_CONFIG["instruction"])
			summaries.append(resumo)
			# Mantém só os últimos 10 resumos
			if len(summaries) > 10:
				summaries = summaries[-10:]
			save_json(SUMMARY_FILE, summaries)


if __name__ == "__main__":
	load_dotenv()
	main()