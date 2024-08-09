import telebot
import supabase
import uuid

bot = telebot.TeleBot("TELE_API")
supabase_client = supabase.create_client("LINK_TO_BASE", "SUPABASE_KEY")

edit_mode = False
registration_keys = ['TELEGRAM_USER_ID', 'TELEGRAM_USER_ID', 'TELEGRAM_USER_ID', 'TELEGRAM_USER_ID']

@bot.message_handler(commands=['start'])
def handle_start(message):
    chat_id = message.chat.id
    user_id = message.from_user.id

    if str(user_id) in registration_keys:
        user_exists = supabase_client.table("users").select("*").eq("user_id", user_id).execute()

        if user_exists.data and len(user_exists.data) > 0:
            user_data = user_exists.data[0]
            bot.send_message(chat_id, f"👨‍💻 Личный кабинет:\n\n┌ Id: {user_data['user_id']}\n└ Имя: {user_data['name']}\n\n/start - Личный Кабинект.\n/alert - Создать алерт.\n/alertfl - Флуд пятью алертами.\n/edit - Редактировать свои данные!\n/faq - Часто задаваемые вопросы.\n/contacts - Cписок контактов.")
        else:
            bot.send_message(chat_id, "Привет! Пожалуйста, введите ваше имя:")
            bot.register_next_step_handler(message, handle_name)
    else:
        bot.send_message(chat_id, "Извините, у вас нет разрешения на доступ к боту.")

@bot.message_handler(commands=['alert'])
def handle_alert(message):
    chat_id = message.chat.id
    user_id = message.from_user.id

    if str(user_id) in registration_keys:
        bot.send_message(chat_id, "Пожалуйста, введите цифру от 1 до 10:")
        bot.register_next_step_handler(message, handle_number, user_id)
    else:
        bot.send_message(chat_id, "Вы не зарегистрированы. Обратитесь к администратору для регистрации.\n@TELEGRAM_TAG")

def handle_number(message, user_id):
    chat_id = message.chat.id
    number = message.text

    if not number.isdigit() or int(number) < 1 or int(number) > 10:
        bot.send_message(chat_id, "Некорректный ввод. Пожалуйста, введите цифру от 1 до 10:")
        bot.register_next_step_handler(message, handle_number, user_id)
    else:
        bot.send_message(chat_id, "Пожалуйста, опишите проблему:")
        bot.register_next_step_handler(message, handle_description, user_id, number)

def handle_description(message, user_id, number):
    chat_id = message.chat.id
    description = message.text

    users = supabase_client.table("users").select("*").execute().data
    for user in users:
        alert_message = f"🚨ALERT!\n\n┌ Опасность: {number}\n├ Описание: {description}\n├ От ID: {user_id}, Имя: {message.from_user.first_name}\n└ Удачи, Гномы!"
        bot.send_message(user['user_id'], alert_message)

    bot.send_message(chat_id, "Сообщение успешно отправлено всем пользователям.")

@bot.message_handler(commands=['alertfl'])
def handle_alertfl(message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    if str(user_id) in registration_keys:
        bot.send_message(chat_id, "Пожалуйста, введите цифру от 1 до 10:")
        bot.register_next_step_handler(message, handle_numberfl, user_id)
    else:
        bot.send_message(chat_id, "Вы не зарегистрированы. Обратитесь к администратору для регистрации.\n@TELEGRAM_TAG")

def handle_numberfl(message, user_id):
    chat_id = message.chat.id
    number = message.text

    if not number.isdigit() or int(number) < 1 or int(number) > 10:
        bot.send_message(chat_id, "Некорректный ввод. Пожалуйста, введите цифру от 1 до 10:")
        bot.register_next_step_handler(message, handle_numberfl, user_id)
    else:
        bot.send_message(chat_id, "Пожалуйста, опишите проблему:")
        bot.register_next_step_handler(message, handle_descriptionfl, user_id, number)

def handle_descriptionfl(message, user_id, number):
    chat_id = message.chat.id
    description = message.text

    users = supabase_client.table("users").select("*").execute().data
    for user in users:
        alert_message = f"🚨ALERT!\n\n┌ Опасность: {number}\n├ Описание: {description}\n├ От ID: {user_id}, Имя: {message.from_user.first_name}\n└ Удачи, Гномы!"
        for _ in range(5):
            bot.send_message(user['user_id'], alert_message)

    bot.send_message(chat_id, "Сообщение успешно отправлено всем пользователям.")

def handle_name(message):
    chat_id = message.chat.id
    name = message.text

    user_id = message.from_user.id 
    user_uuid = uuid.uuid4()

    data = {
        "user_id": user_id,
        "name": name,
        "uuid": str(user_uuid)
    }
    supabase_client.table("users").insert(data).execute()

    bot.send_message(chat_id, f"👨‍💻 Личный кабинет:\n\n┌ Id: {user_id}\n└ Имя: {name}\n\n/start- Личный Кабинект.\n/alert - Создать алерт.\n/alertfl - Флуд пятью алертами.\n/edit - Редактировать свои данные!\n/faq - Часто задаваемые вопросы.\n/contacts - Cписок контактов.")

@bot.message_handler(commands=['contacts'])
def handle_edit(message):
    chat_id = message.chat.id
    user_id = message.from_user.id 
    if str(user_id) in registration_keys:
        bot.send_message(chat_id, "Contacts text")
    else:
        bot.send_message(chat_id, "Вы не зарегистрированы. Обратитесь к администратору для регистрации.\n@TELEGRAM_TAG")

@bot.message_handler(commands=['faq'])
def handle_edit(message):
    chat_id = message.chat.id
    user_id = message.from_user.id 
    if str(user_id) in registration_keys:
        bot.send_message(chat_id, "FAQ text")
    else:
        bot.send_message(chat_id, "Вы не зарегистрированы. Обратитесь к администратору для регистрации.\n@TELEGRAM_TAG")

@bot.message_handler(commands=['edit'])
def handle_edit(message):
    global edit_mode
    chat_id = message.chat.id
    user_id = message.from_user.id 

    if str(user_id) in registration_keys:

        if message.text.strip().lower() != '/edit':
            bot.send_message(chat_id, "Пожалуйста, введите команду /edit, чтобы редактировать свои данные.")
            return

        edit_mode = True

        bot.send_message(chat_id, "Выберите опцию для редактирования:")
        keyboard = telebot.types.ReplyKeyboardMarkup(row_width=2)
        button_name = telebot.types.KeyboardButton(text='Изменить имя')
        keyboard.add(button_name)
    else:
        bot.send_message(chat_id, "Вы не зарегистрированы. Обратитесь к администратору для регистрации.\n@TELEGRAM_TAG")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    global edit_mode
    chat_id = message.chat.id
    text = message.text.lower()

    if edit_mode:
        if text == 'изменить имя':
            bot.send_message(chat_id, "Введите новое имя:")
            bot.register_next_step_handler(message, handle_name_update)
        else:
            bot.send_message(chat_id, "Некорректный выбор.")

def handle_name_update(message):
    global edit_mode
    chat_id = message.chat.id
    name = message.text
    supabase_client.table("users").update({"name": name}).eq("user_id", message.from_user.id).execute()
    bot.send_message(chat_id, "Имя успешно обновлено.", reply_markup=telebot.types.ReplyKeyboardRemove())
    edit_mode = False

bot.polling()