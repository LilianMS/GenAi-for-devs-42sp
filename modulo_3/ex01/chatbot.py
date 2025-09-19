import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

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


def main():

	history = []
	print("Chatbot Gemini (digite 'bye' para encerrar)")
	response = get_ia_response("Apresente-se como meu amigo, Bob", API_CONFIG["instruction"])
	print(f"Bob: {response}")
	history.append(("", response))
	while True:
		user_input = input("Q: ")
		if user_input.strip().lower() == "bye":
			break
		context = ""
		for u, b in history[-5:]:
			context += f"User: {u}\nBot: {b}\n"
		context += f"User: {user_input}\nBot: "
		user_input = context
		print("Bob is typing...")
		bot_reply = get_ia_response(user_input, API_CONFIG["instruction"])

		print(f"Bob: {bot_reply}")
		history.append((user_input, bot_reply))
		
		if len(history) > 5:
			history = history[-5:]


if __name__ == "__main__":
	load_dotenv()
	main()