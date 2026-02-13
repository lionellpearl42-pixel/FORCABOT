import os
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)

from jogo import iniciar_jogo, tentar_letra
from torneio import atualizar_pontuacao, ranking
from convocacao import iniciar_scheduler

TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

user_jogos = {}

# ---------------- START ----------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 Bem-vindo ao Bot de Forca!\nUse /jogar para começar."
    )

# ---------------- JOGAR ----------------
async def jogar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    user_jogos[user_id] = iniciar_jogo()
    jogo = user_jogos[user_id]

    await update.message.reply_text(
        f"🧠 Dica: {jogo['dica']}\n"
        f"{' '.join(jogo['acertos'])}\n"
        f"Tentativas: {jogo['tentativas']}"
    )

# ---------------- LETRA ----------------
async def letra(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id

    if user_id not in user_jogos:
        return

    l = update.message.text.lower()
    jogo = user_jogos[user_id]

    acertou, fim = tentar_letra(jogo, l)

    if acertou and fim:
        await update.message.reply_text(
            f"🎉 Parabéns! Você acertou: {jogo['palavra']}"
        )
        atualizar_pontuacao(user_id, 10)
        del user_jogos[user_id]

    elif not acertou and fim:
        await update.message.reply_text(
            f"💀 Fim de jogo! A palavra era: {jogo['palavra']}"
        )
        del user_jogos[user_id]

    else:
        await update.message.reply_text(
            f"{' '.join(jogo['acertos'])}\n"
            f"Tentativas restantes: {jogo['tentativas']}"
        )

# ---------------- RANKING ----------------
async def ver_ranking(update: Update, context: ContextTypes.DEFAULT_TYPE):
    r = ranking()
    msg = "🏆 Ranking Top 10:\n"

    for i, (nome, pontos) in enumerate(r, start=1):
        msg += f"{i}. {nome} - {pontos} pts\n"

    await update.message.reply_text(msg)

# ---------------- MAIN ----------------
def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("jogar", jogar))
    app.add_handler(CommandHandler("ranking", ver_ranking))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, letra))

    # Inicia convocação automática
    iniciar_scheduler(TOKEN, CHAT_ID)

    print("✅ Bot rodando...")
    app.run_polling()

if __name__ == "__main__":
    main()
