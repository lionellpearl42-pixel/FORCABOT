import random

def gerar_dica(palavra, hint_base):
    # Dicas simples sem OpenAI
    dicas = [
        f"Começa com '{palavra[0]}'",
        f"Termina com '{palavra[-1]}'",
        f"Dica base: {hint_base}"
    ]
    return random.choice(dicas)
