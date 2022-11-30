import config
import telebot

bot = telebot.TeleBot(config.bot_token)


def send_message_to_terr_upr(text):
    bot.send_message(chat_id=config.chat_id_knm, text=text)


if __name__ == '__main__':
    send_message_to_terr_upr('если это пришло от бота - значит работает!')
