# symmetrical-potato
## Основные модули
Платформа для создания бота
Маркетплейс
Класс курса
Статистика

# Итерации
1. Класс курса
2. Платформа для создания бота/Статистика
3. Маркетплейс 


## Model API
- init_bot(token) - Adds bot to database and returns "Sucsess" or "Fail"
- get_description(token) - Return bot's name and decription
- new_user(token, chat_id) - Adds new user to bot connections list and returns first question
- get_info(token, chat_id) - Return next time to send message and next question if user read previous
- set_read(token, chat_id) - Sets user _read_last_message_ property to true, so bot can send new messages

## Bot Initial Info
- Token
- Name - @bot
- Screen Name - "Bot"
- Tags 
- Messages
- Description
- Author 