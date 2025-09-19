
import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types


def main():
	load_dotenv()
	api_key = os.getenv("GOOGLE_API_KEY")
	if not api_key:
		print("Erro: GOOGLE_API_KEY não definida no .env.")
		sys.exit(1)

	genai.configure(api_key=api_key)
	model = genai.GenerativeModel("gemini-pro")

	history = []  # Lista de tuplas (user, bot)

	print("Chatbot Gemini (digite 'sair' para encerrar)")
	while True:
		user_input = input("Você: ")
		if user_input.strip().lower() == "sair":
			print("Encerrando o chatbot.")
			break

		# Monta contexto das últimas 5 interações
		context = ""
		for u, b in history[-5:]:
			context += f"Usuário: {u}\nBot: {b}\n"
		context += f"Usuário: {user_input}\nBot: "

		try:
			response = model.generate_content(context)
			bot_reply = response.text.strip()
		except Exception as e:
			bot_reply = f"[Erro ao gerar resposta: {e}]"

		print(f"Bot: {bot_reply}")
		history.append((user_input, bot_reply))
		# Mantém só as últimas 5 interações
		if len(history) > 5:
			history = history[-5:]


if __name__ == "__main__":
	main()