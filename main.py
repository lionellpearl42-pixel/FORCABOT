from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from jogo import iniciar_jogo, tentar_letra
from torneio import atualizar_pontuacao, ranking
from convocacao import iniciar_scheduler

TOKEN = "SEU_TOKEN_DO_BOT"
CHAT_ID = "@seu_grupo"  # Grupo do Telegram

updater = Updater(TOKEN)
dp = updater.dispatcher

# Usuário -> jogo atual
user_jogos = {}

def start(update: Update, context: CallbackContext):
    update.message.reply_text("Bem-vindo ao Bot de Forca! Use /jogar para começar.")

def jogar(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    user_jogos[user_id] = iniciar_jogo()
    jogo = user_jogos[user_id]
    update.message.reply_text(f"Dica: {jogo['dica']}\n{' '.join(jogo['acertos'])}\nTentativas: {jogo['tentativas']}")

def letra(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    if user_id not in user_jogos:
        update.message.reply_text("Use /jogar para iniciar uma partida.")
        return
    l = update.message.text.lower()
    jogo = user_jogos[user_id]
    acertou, fim = tentar_letra(jogo, l)
    if acertou and fim:
        update.message.reply_text(f"🎉 Parabéns! Você acertou: {jogo['palavra']}")
        atualizar_pontuacao(user_id, 10)
        del user_jogos[user_id]
    elif not acertou and fim:
        update.message.reply_text(f"💀 Fim de jogo! A palavra era: {jogo['palavra']}")
        del user_jogos[user_id]
    else:
        update.message.reply_text(f"{' '.join(jogo['acertos'])}\nTentativas restantes: {jogo['tentativas']}")

def ver_ranking(update: Update, context: CallbackContext):
    r = ranking()
    msg = "🏆 Ranking Top 10:\n"
    for i, (nome, pontos) in enumerate(r, start=1):
        msg += f"{i}. {nome} - {pontos} pts\n"
    update.message.reply_text(msg)

dp.add_handler(CommandHandler("start", start))
dp.add_handler(CommandHandler("jogar", jogar))
dp.add_handler(CommandHandler("ranking", ver_ranking))
dp.add_handler(MessageHandler(Filters.text & ~Filters.command, letra))

# Inicia scheduler de convocação
iniciar_scheduler(TOKEN, CHAT_ID)

updater.start_polling()
updater.idle()
