from logic import *
from config import *
from telebot import TeleBot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

bot = TeleBot(token)
manager = DB_Manager(DATABASE)


STATES = [
    "Maharashtra", "Tamil Nadu", "Andhra Pradesh", "Tripura",
    "Pondicherry", "West Bengal", "Nagaland", "Rajasthan",
    "Karnataka", "Assam", "Madhya Pradesh", "Chandigarh"
]

@bot.message_handler(commands=['start'])
def start(message):
    keyboard = InlineKeyboardMarkup()
    

    for state in STATES:
        keyboard.add(InlineKeyboardButton(state, callback_data=f"state_{state}"))
    
    bot.send_message(message.chat.id, "Выберите штат:", reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: call.data.startswith('state_'))
def handle_click(call):
    state_name = call.data.replace('state_', '')
    
    try:
        data = manager.get_state_data(state_name)
        
        if data:
            result = f"Топ рынков в {state_name}:\n\n"
            for index, row in enumerate(data, 1):
                result += f"{index}. {row[0]}\n"
                result += f"Мин стоимость: {row[1]}\n"
                result += f"Макс стоимость: {row[2]}\n\n"
            
            bot.send_message(call.message.chat.id, result, parse_mode='Markdown')

        
    except Exception as e:
        print(e)

if __name__ == '__main__':
    bot.polling()