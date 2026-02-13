from ia import gerar_palavra_ia

async def iniciar_jogo():
    palavra, dica = await gerar_palavra_ia()

    return {
        "palavra": palavra,
        "dica": dica,
        "acertos": ["_" for _ in palavra],
        "tentativas": 6,
        "letras_usadas": []
    }

def tentar_letra(jogo, letra):
    if letra in jogo["letras_usadas"]:
        return False, False

    jogo["letras_usadas"].append(letra)

    if letra in jogo["palavra"]:
        for i, l in enumerate(jogo["palavra"]):
            if l == letra:
                jogo["acertos"][i] = letra

        if "_" not in jogo["acertos"]:
            return True, True

        return True, False
    else:
        jogo["tentativas"] -= 1

        if jogo["tentativas"] <= 0:
            return False, True

        return False, False
