
import sys
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


frases = [
    "O cachorro correu pelo parque atrás da bola azul.",
    "Ontem a bolsa de valores fechou em queda após anúncio do governo.",
    "O vulcão entrou em erupção, iluminando o céu noturno com lava.",
    "Aprender programação em Python pode abrir muitas portas no mercado de trabalho.",
    "O café recém-moído tem um aroma que desperta memórias da infância.",
    "Cientistas descobriram uma nova espécie de peixe em águas profundas.",
    "A final da Copa foi decidida nos pênaltis, com muita emoção na torcida.",
    "O conceito de buracos negros desafia nossa compreensão do espaço-tempo.",
    "O artista usou realidade aumentada para criar uma exposição interativa.",
    "A meditação diária ajuda a reduzir o estresse e aumentar a concentração."
]


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python3 embeddings.py \"sua frase de busca\"")
        sys.exit(1)

    consulta = " ".join(sys.argv[1:]).strip()

    model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")
    consulta_embedding = model.encode(consulta)
    frases_embeddings = model.encode(frases)

    scores = cosine_similarity([consulta_embedding], frases_embeddings)[0]

    top3 = sorted(zip(frases, scores), key=lambda x: x[1], reverse=True)[:3]

    for frase, score in top3:
        print(f"{frase} (score: {score:.4f})")