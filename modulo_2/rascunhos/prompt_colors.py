from dotenv import load_dotenv  
import sys
import os
import google.generativeai as genai
from rich import print, box
from rich.panel import Panel
from rich.prompt import Prompt
from rich.console import Console
from rich.table import Table

console = Console()


def get_ia_response(ask, model_name, temp=1.0):
    try:
        chave_api = os.getenv("GEMINI_API_KEY")
        if not chave_api:
            return "Erro: A chave de API não foi definida."
        genai.configure(api_key=chave_api)
        modelo = genai.GenerativeModel(model_name)
        modelo.generation_config = genai.GenerationConfig(temperature=temp)
        resposta = modelo.generate_content(ask)
        return resposta.text

    except Exception as e:
        return f"Ocorreu um erro: {e}"

def get_temperature(temp_str):
    temp = float(temp_str)
    if 0.0 <= temp <= 2.0:
        return temp
    return 1.0

# Painel de boas-vindas
print(Panel("[bold cyan]Bem-vindo ao Prompt Interativo com [magenta]Rich[/magenta]![/bold cyan]", title="🤖 IA 42sp", subtitle="Digite 'sair' para encerrar"))

historico = []

while True:
    if len(sys.argv) < 2:
        print("Uso: python prompt.py '<pergunta>'")
        sys.exit(1)
    if len(sys.argv) > 2:
        temp = get_temperature(sys.argv[2])
    pergunta = sys.argv[1]
    modelo_nome = "gemini-2.5-flash"

    resposta = get_ia_response(pergunta, modelo_nome, temp)
    print(f"Pergunta: {pergunta}")
    print(f"\n{modelo_nome}:")
    print("-" * 50)
    print(resposta)
    print("-" * 50)
    print(f"Modelo: {modelo_nome}, Temperatura: {temp}")

    if pergunta.lower() in ("sair", "exit", "quit"):
        print(Panel("[green]Até logo![/green]", title="👋"))
        break
    # Simulação de resposta da IA
    resposta = f"[italic]Resposta simulada para:[/] [bold]{pergunta}[/bold]"
    historico.append((pergunta, resposta))
    print(Panel(resposta, title="[blue]Resposta da IA[/blue]", subtitle="✨"))

    # Exibir histórico em tabela
    if len(historico) > 1:
        table = Table(title="Histórico de Perguntas", box=box.SIMPLE)
        table.add_column("Pergunta", style="yellow")
        table.add_column("Resposta", style="green")
        for p, r in historico:
            table.add_row(p, r)
        console.print(table)

