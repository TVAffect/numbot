import telebot 
import random
import json
from telebot import types
from tgconfig import token, password

#у меня тут всё тупо и плоско, даже комментариев нет почти. возмущаться запрещаю

bot=telebot.TeleBot(token)
file_path='chats-nums.json'

def check_auth(chat_id):
  try:
    with open(file_path,'r') as file:
      database=json.load(file)
  except FileNotFoundError:
    database={}
    with open(file_path,'w') as file:
      json.dump(database,file,indent=2)
  if database.get(str(chat_id),False) != False:
    return True
  else:
    return False

@bot.message_handler(commands=['start'])
def start(message):
  print(message.text,'-',message.chat.id,message.from_user.username)
  bot.reply_to(message, '''Привет! Я бот для отгадывания чисел.
  
  Для списка команд пропишите /help.
  
  Имейте ввиду, что я размещён не на хостинге, а на компе моего разраба. Наврядли я внезапно лягу, но моя работа зависит от расположения Сатурна относительно Козерога, желаний левой пятки мамки и состояния компа моего создателя.''')

@bot.message_handler(commands=['help'])
def help(message):
  print(message.text,'-',message.chat.id,message.from_user.username)
  bot.reply_to(message, '''Здесь расписаны мои команды.
  
  /gen - сгенерировать новое число. После этой команды в том же сообщении нужно написать сложность загаданного числа (меньше сложность - меньше диапазон). Лёгкая - "1" или "easy", средняя - "2" или "medium", сложная - "3" или "hard". Пример: /gen hard, /gen 2.
  /num - ввести число как попытку. После этой команды я скажу, меньше или больше у меня загаданное число.
  /pass - ввести пароль для доступа к функционалу. Вводить нужно в одном сообщении с командой.''') 

@bot.message_handler(commands=['pass'])
def com_pass(message):
  chat_id=message.chat.id
  print(message.text,'-',chat_id,message.from_user.username)
  if check_auth==True:
    bot.reply_to(message,'Этот чат уже авторизован.')
  else:
    passwd=message.text.replace('/pass ','')
    if passwd==password:
      chat_id=message.chat.id
      with open(file_path,'r') as file:
        database=json.load(file)
      database[str(chat_id)]='Severe Head Pain'
      with open(file_path,'w') as file:
        json.dump(database,file,indent=2)
      bot.reply_to(message,'Теперь этот чат авторизован! Можете пользоваться всеми моими командами.')
    else:
      bot.reply_to(message,'Неправильный пароль!')

@bot.message_handler(commands=['gen'])
def gen(message):
  chat_id=message.chat.id
  print(message.text,'-',chat_id,message.from_user.username)
  if check_auth(chat_id) == True:
    with open(file_path,'r') as file:
      database=json.load(file)
    difficulty=message.text.replace('/gen ','')
    if difficulty=='1' or difficulty=='easy':
      database[str(chat_id)]=random.randint(-100,100)
      bot.reply_to(message, '''Число успешно сгенерировано! Сложность - лёгкая. Удачи отгадывать :)''')
    elif difficulty=='2' or difficulty=='medium':
      database[str(chat_id)]=random.randint(-1000000,1000000)
      bot.reply_to(message, '''Число успешно сгенерировано! Сложность - средняя. Удачи отгадывать :)''')
    elif difficulty=='3' or difficulty=='hard':
      database[str(chat_id)]=random.randint(-10000000000,10000000000)
      bot.reply_to(message, '''Число успешно сгенерировано! Сложность - сложная. Удачи отгадывать :)''')
    else:
      bot.reply_to(message,'После команды нужно ввести сложность. Введите /help для подробностей.')
    with open(file_path,'w') as file:
        json.dump(database,file,indent=2)
  elif check_auth(chat_id) == False:
    bot.reply_to(message, 'Похоже, этот чат не авторизован. Введите пароль доступа через команду /pass') 
  else:
    print('что-то пошло не так на чеке')

@bot.message_handler(commands=['num'])
def num(message):
  chat_id=message.chat.id
  print(message.text,'-',chat_id,message.from_user.username)
  if check_auth(chat_id) == True:
    attempt=message.text.replace('/num ','')
    try:
      attempt=int(attempt)
      with open(file_path,'r') as file:
        wtf=json.load(file)
      if wtf[str(chat_id)]=='Severe Head Pain':
        bot.reply_to(message,'Сначала сгенерируйте число.')
      elif attempt==wtf[str(chat_id)]:
        wtf[str(chat_id)]='Severe Head Pain'
        with open(file_path,'w') as file:
          json.dump(wtf,file,indent=2)
        bot.reply_to(message,'Это действительно то число, которое я загадал, поздравляю!')
      elif attempt>wtf[str(chat_id)]:
        bot.reply_to(message,'Моё число меньше вашего.')
      else:
        bot.reply_to(message,'Моё число больше вашего.')
    except ValueError:
      bot.reply_to(message,'Введите нормальное число, а не что вы там ввели...')
  else:
    bot.reply_to(message,'Похоже, этот чат не авторизован. Введите пароль доступа через команду /pass') 

print('бот запущен') 
bot.infinity_polling()
