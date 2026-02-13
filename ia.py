import os
import json
from groq import Groq

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

async def gerar_palavra_ia():
    prompt = """
    Gere uma palavra única em Português do Brasil para jogo da forca.
    Regras:
    - Apenas UMA palavra
    - Sem espaços
    - Sem acentos
    - Apenas letras minúsculas
    - Palavra comum no Brasil
    - Inclua uma dica curta

    Responda em JSON assim:
    {
        "palavra": "exemplo",
        "dica": "descricao curta"
    }
    """

    response = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.9,
    )

    content = response.choices[0].message.content.strip()

    try:
        data = json.loads(content)
        return data["palavra"], data["dica"]
    except:
        return "brasil", "Pais da America do Sul"
