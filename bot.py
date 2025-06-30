import telebot
import json
from telebot import types
from config import token, password


bot=telebot.TeleBot(token)
file_path='chats-nums.json

def check_auth(chat_id):
	with open(file_path,'r') as file:
		database=json.load(file)
		if chat_id in database:
			return True
		else:
			return False

  
@bot.message_handler(commands=['start'])
def startBot(message):
    bot.reply_to(message, '''Привет! Я бот для отгадывания чисел. К сожалению, пока что я нахожусь в разработке, и поэтому такого функционала у меня нет.
        
    Для списка комманд пропишите /help.
        
    Пожалуйста, будьте аккуратнее со мной. Мой разработчик - нищенка, он разместил меня на бесплатном хостинге, так что я могу лечь в любой неподходящий момент. А ещё он неопытный, что означает, что я могу глючить...''')
  
  
@bot.message_handler(commands=['help'])
def help(message):
    bot.reply_to(message, '''Здесь расписаны мои БУДУЩИЕ команды, а не текущие, так как у меня ещё нет функционала.
        
    /gen - сгенерировать новое число.
    /num - ввести число как попытку. После этой команды я скажу, меньше или больше у меня загаданное число.''') 

  
@bot.message_handler(commands=['pass'])
def com_pass(message):
    passwd=message.text.replace('/pass','')
    if passwd==password:
		bot.send.message(message.chat.id,'Теперь этот чат авторизован! Можете пользоваться всеми моими командами'
	else:
		bot.send.message(message.chat.id,'Неправильный пароль!')
		
@bot.message_hadler(commands=['gen'])
def gen(message):
    chat_id=message.chat.id
    if check_auth(chat_id) == True:
	    with open(file_path,'r+') as file:
			database=json.load(file)
			database[chat_id]=random.randint(-1000000000,1000000000)
			json.dump(database,file,indent=4)
        bot.reply_to(message, '''Число успешно сгенерировано! 
    
        Удачи отгадывать :)''')
    else:
        bot.reply_to(message, 'Похоже, этот чат не авторизован. Введите пароль доступа через команду /pass') 
    
    
@bot.message_handler(command=['num'])
def num(message):
    chat_id=message.chat.id
    if check_auth(chat_id) == True:
	    attempt=message.text.replace('/num','')
	    try:
			attempt=int(attempt)
			with open(file_path,'r') as file:
			wtf=json.load(file)
			if wtf[chat_id] is None:
				bot.reply_to(message,'Сначала сгенерируйте число.')
			elif attempt==wtf[chat_id]:
				bot.reply_to(message,'Это действительно то число, которое я загадал, поздравляю!')
				wtf[chat_id]=None
			elif attempt>wtf[chat_id]:
				bot.reply_to(message,'Моё число меньше вашего.')
			else:
				bot.reply_to(message,'Моё число больше вашего.')
		except ValueError:
			bot.reply_to(message,'Введите число.')
	    
				
    else:
        bot.reply_to(message, 'Похоже, этот чат не авторизован. Введите пароль доступа через команду /pass') 
  
  
print('бот запущен') 
bot.infinity_polling()
