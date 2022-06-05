import telebot
from config import keys, TOKEN
from utils import ConvertionException, CryptoConverter


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start','help'])
def help(message: telebot.types.Message):
    text = 'Приветствую! Я конвертер валют. Для начала работы введи:  \n<имя валюты> \
<в какую валюту перевести> \
<количество переводимой валюты>\nПросмотреть,список всех доступных валют с помощью команды:/values \
\nНужна помощь введи: /help'

    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
      text = 'Доступные валюты:'
      for key in keys.keys():
          text = '\n'.join((text, key, ))
      bot.reply_to(message, text)


@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
   try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise ConvertionException('Слишком много параметров')

        guote, base, amount = values
        total_base = CryptoConverter.convert(guote, base, amount)
   except ConvertionException as e:
        bot.reply_to(message,f'Ошибка пользователя.\n{e}')
   except Exception as e:
        bot.reply_to(message,f'Не удалось обработать команду\n{e}')
   else:
        text = f'Цена {amount} {guote} в {base} - {total_base}'
        bot.send_message(message.chat.id, text)

bot.polling(none_stop=True)
