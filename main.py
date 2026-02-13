import os
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

from jogo import iniciar_jogo, tentar_letra
from torneio import atualizar_pontuacao, ranking

# =============================
# CONFIGURAÇÕES
# =============================

TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")  # Ex: -1001234567890

user_jogos = {}

# =============================
# COMANDOS
# =============================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 Bem-vindo ao Bot de Forca!\n\n"
        "Use /jogar para começar.\n"
        "Use /ranking para ver os melhores."
    )


async def jogar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id

    jogo = await iniciar_jogo()
    user_jogos[user_id] = jogo

    await update.message.reply_text(
        f"🧠 Dica: {jogo['dica']}\n\n"
        f"{' '.join(jogo['acertos'])}\n"
        f"🎯 Tentativas: {jogo['tentativas']}"
    )



async def letra(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id

    if user_id not in user_jogos:
        return

    l = update.message.text.lower()
    jogo = user_jogos[user_id]

    acertou, fim = tentar_letra(jogo, l)

   if acertou and fim:
    usuario = update.message.from_user
    mention = f"<a href='tg://user?id={usuario.id}'>{usuario.first_name}</a>"

    await update.message.reply_html(
        f"🎉 {mention} VENCEU!\n\n"
        f"Palavra: <b>{jogo['palavra']}</b>\n"
        f"+10 pontos!"
    )

    atualizar_pontuacao(str(usuario.id), 10)
    del user_jogos[user_id]


    elif not acertou and fim:
        await update.message.reply_text(
            f"💀 Fim de jogo!\nA palavra era: {jogo['palavra']}"
        )

        del user_jogos[user_id]

    else:
        await update.message.reply_text(
            f"{' '.join(jogo['acertos'])}\n"
            f"❌ Tentativas restantes: {jogo['tentativas']}"
        )


async def ver_ranking(update: Update, context: ContextTypes.DEFAULT_TYPE):
    r = ranking()

    if not r:
        await update.message.reply_text("Ainda não há pontuações.")
        return

    msg = "🏆 RANKING TOP 10\n\n"

    for i, (nome, pontos) in enumerate(r, start=1):
        msg += f"{i}. {nome} - {pontos} pts\n"

    await update.message.reply_text(msg)


# =============================
# CONVOCAÇÃO AUTOMÁTICA
# =============================

async def convocar(context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=context.job.chat_id,
        text="🚨 NOVO TORNEIO DE FORCA!\nUse /jogar para participar!"
    )


def iniciar_scheduler(app, chat_id):
    # A cada 2 horas (7200 segundos)
    app.job_queue.run_repeating(
        convocar,
        interval=7200,
        first=15,
        chat_id=chat_id,
    )


# =============================
# MAIN
# =============================

def main():
    if not TOKEN:
        raise ValueError("BOT_TOKEN não definido nas variáveis de ambiente.")

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("jogar", jogar))
    app.add_handler(CommandHandler("ranking", ver_ranking))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, letra))

    # Inicia convocação automática
    if CHAT_ID:
        iniciar_scheduler(app, CHAT_ID)

    print("✅ Bot rodando...")
    app.run_polling()


if __name__ == "__main__":
    main()
