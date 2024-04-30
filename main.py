import time
import config

from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.errors import FloodWait

api_hash = config.api_hash
api_id = config.api_id

# with Client(name="my_account", api_hash=api_hash, api_id=api_id) as app:
#     app.send_message("me", "Это я бот")

client = Client(name="my_account", api_hash=api_hash, api_id=api_id)


@client.on_message(filters.private)
def echo(client_object, message: Message):
    #client_object.send_message(message.chat.id, f"вы сказали: {message.text}")
    text = message.text.lower()
    text_array = text.split(' ')
    if 'понятно' in text or 'ожидать' in text_array:
        pass
    else:
        pass


@client.on_message(filters.command("type", prefixes='!') & filters.me)
def type(client_object, message: Message):
    input_text = message.text.split("!type ", maxsplit=1)[1]
    temp_text = input_text
    edited_text = ""
    typing_symbol = "⁂"

    while edited_text != input_text:
        try:
            message.edit(edited_text + typing_symbol)
            time.sleep(0.05)
            edited_text = edited_text + temp_text[0]
            temp_text = temp_text[1:]
            message.edit(edited_text)
            time.sleep(0.05)
        except FloodWait:
            print("Превышен лимит сообщений")


client.run()


if __name__ == '__main__':
    client.run()



