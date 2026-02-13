import random
from database import c
from ai_groq import gerar_dica

def iniciar_jogo():
    c.execute("SELECT * FROM words ORDER BY RANDOM() LIMIT 1")
    palavra, hint = c.fetchone()
    jogo = {
        "palavra": palavra,
        "dica": gerar_dica(palavra, hint),
        "tentativas": 6,
        "acertos": ["_" for _ in palavra]
    }
    return jogo

def tentar_letra(jogo, letra):
    letra = letra.lower()
    if letra in jogo["palavra"]:
        for i, l in enumerate(jogo["palavra"]):
            if l == letra:
                jogo["acertos"][i] = letra
        venceu = "_" not in jogo["acertos"]
        return True, venceu
    else:
        jogo["tentativas"] -= 1
        perdeu = jogo["tentativas"] == 0
        return False, perdeu
