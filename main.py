import telebot
from telebot import types
import time
from random import randint
import phrases
import user
import board
import pymysql
import staff_functions
import threading

strings = phrases.strings()
board   = board.board()

secrets = staff_functions.load_json("/secrets.json")
mysql_user                 = "miron_root"
mysql_pass				   = secrets["mysql_pass"]

bot = telebot.TeleBot("1577575841:AAFO0cSv0EMZuMR_L-8CniDh98r8ZUKfoeo")
users = []
def send_info_key_board():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row("Написать в чат")
    markup.row("Вопрос к матери")
    markup.row("Пропустить и бросить кубик🎲")
    return markup

def thread_function(bot, chat_id, message_id):
        num_to_send = randint(0,6)
        num_buff    = 0
        i = 0
        while i < 7:
            num_to_send = randint(1,6)

            if(num_to_send != num_buff):           
                bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=strings.when_cude_is_rotating+str(num_to_send))
                num_buff = num_to_send
                time.sleep(0.1)
                i+=1
        process_cube_result(bot, chat_id, message_id, num_buff)

def process_cube_result(bot, chat_id, message_id, score_cube):
        #bot.send_message(chat_id=chat_id, text="Результат кубика: "+str(score_cube))
        user = get_user(chat_id)
        if_new = 0
        if(user.current_step == 0):
                if_new = 1
        user.current_step = user.current_step + score_cube
        info_pos = board.get_info(user.current_step)
        exit_str = ""
        if(if_new):
            exit_str =  strings.result_cube + str(score_cube) + "\n\n" + strings.now_position  + str(user.current_step) + "\n" + strings.theam_position + info_pos[2] + "\n\n" + strings.first_message + str(user.current_step) + ", «" + info_pos[2] + "»\n"
        else:
            exit_str =  strings.result_cube + str(score_cube) + "\n\n" + strings.now_position  + str(user.current_step)+ "\n" + strings.theam_position + info_pos[2] + "\n\n" + strings.first_message + str(user.current_step) + ", <a href = '"+str(info_pos[4])+"'>«" + info_pos[2] + "</a>»\n"
        user.stage = 4
        user.sync()
                    
        bot.send_message(chat_id=chat_id, text=exit_str, parse_mode='HTML',reply_markup=send_info_key_board())
@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):

    if call.message:
        #url_button = types.InlineKeyboardButton(text="URL", url="https://ya.ru")
        #switch_button = types.InlineKeyboardButton(text="Switch", switch_inline_query="Telegram")
   
        keyboard = types.InlineKeyboardMarkup(row_width=2)

        if call.data == "test":
            callback_button = types.InlineKeyboardButton(text="А ну быстро сосатьxx2", callback_data="sosi")
            keyboard.add(callback_button)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="сосать",reply_markup=keyboard)
            bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="Пыщь!")

        if call.data == "sosi":
            callback_button = types.InlineKeyboardButton(text="Генерация числа", callback_data="generate_numbers")
            keyboard.add(callback_button)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="generate_numbers", reply_markup=keyboard)
            bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="generate_numbers")
        if call.data == "generate_numbers":
            bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="Кубик брошен!")
            
            mythrd = threading.Thread(target= thread_function,args=(bot, call.message.chat.id, call.message.message_id), daemon=True)
            mythrd.start()
        

    elif call.inline_message_id:
        if call.data == "test":
            bot.edit_message_text(inline_message_id=call.inline_message_id, text="Бдыщь")

@bot.message_handler(commands=['gen'])
def send_gen(message):
            keyboard = types.InlineKeyboardMarkup(row_width=2)
            callback_button = types.InlineKeyboardButton(text="Генерация числа", callback_data="generate_numbers")
            keyboard.add(callback_button)
            bot.send_message(chat_id=message.chat.id, text="0", reply_markup=keyboard)


def get_user(chat_id): 
        con = pymysql.connect('localhost', mysql_user, mysql_pass, 'tg_bot', autocommit=True)
        cur = con.cursor()
        cur.execute("SELECT * FROM `users` WHERE chat_id = " + str(chat_id))
        rows = cur.fetchall()
        if(cur.rowcount < 1):
                cur2 = con.cursor()
                cur2.execute("INSERT INTO `users` (`id`, `chat_id`, `current_step`, `lives`, `last_time_write`, `payment`, `name`, `stage`) VALUES (NULL, '"+str(chat_id)+"', '0', '0', '"+str(int(time.time()))+"', '0', 'User', 0);")
                return user.user(chat_id, 0, 0, int(time.time()), 0, "User", 0)
        else:
            return user.user(chat_id, rows[0][2], rows[0][3], rows[0][4], rows[0][5], rows[0][6],rows[0][7])

@bot.message_handler(commands=['start'])
def send_start(message):
            user = get_user(message.chat.id)
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            keyboard.row(strings.message_to_form_query_button)
            bot.send_message(chat_id=message.chat.id, text=strings.message_to_form_query, reply_markup=keyboard)
            user.stage = 1
            user.sync()
            
@bot.message_handler(func=lambda message: True, content_types=['text'])
def any_msg(message):
            user = get_user(message.chat.id)
            user.echo_user()
            if(message.text == strings.message_to_form_query_button and user.stage == 1):
                bot.send_message(chat_id=message.chat.id, text=strings.message_get_user_query, reply_markup=types.ReplyKeyboardRemove())
                user.stage = 2
                user.sync()
                return
            if(user.stage == 2):
                user.set_user_query(message.text)
                user.stage = 3
                keyboard = types.InlineKeyboardMarkup(row_width=2)
                callback_button = types.InlineKeyboardButton(text=strings.spin_cude, callback_data="generate_numbers")
                keyboard.add(callback_button)
                bot.send_message(chat_id=message.chat.id, text = strings.message_reply_get_user_query, reply_markup=keyboard)
                user.sync()
                return
            if(user.stage == 4 and message.text == strings.skip_and_spin_cude ):
                    user.stage = 0
                    bot.send_message(chat_id=message.chat.id, text = "Извини у тебя нет подписки оформи или попробуй завтра")
                    
                    user.sync()

if __name__ == '__main__':
    #bot.infinity_polling()
    bot.polling(none_stop=True,timeout=1,long_polling_timeout=1)