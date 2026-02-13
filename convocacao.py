from apscheduler.schedulers.background import BackgroundScheduler
from telegram import Bot

def convocar(bot_token, chat_id):
    bot = Bot(bot_token)
    bot.send_message(chat_id=chat_id, text="🚨 Novo torneio de Forca! Use /jogar para participar!")

def iniciar_scheduler(bot_token, chat_id):
    scheduler = BackgroundScheduler()
    scheduler.add_job(convocar, 'interval', hours=2, args=[bot_token, chat_id])
    scheduler.start()
