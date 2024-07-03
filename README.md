# python-telegram-bot

## Useful methods:

```
update.message.reply_text(text)
update.message.reply_photo(photo)
update.message.reply_document(document)

context.bot.send_message(chat_id, text)
context.bot.send_photo(chat_id, photo)
context.bot.send_document(chat_id, document)

Handling Updates:
CommandHandler(command, callback)
Messagehandler(Filters.text, callback)

Updating Bot Commands:
set_my_commands(commands)

send_sticker(chat_id, sticker)
send_animation(chat_id, animation)

update.message.text

context.user_data[] = {}

ConversationHandler() - manage multi-step conversations. 
```