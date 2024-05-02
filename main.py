import config
import asyncio

from pyrogram import Client, filters
from pyrogram.types import Message
import database
from datetime import datetime

api_hash = config.api_hash
api_id = config.api_id

# with Client(name="my_account", api_hash=api_hash, api_id=api_id) as app:
#     app.send_message("me", "Это я бот")

client = Client(name="my_account", api_hash=api_hash, api_id=api_id)

@client.on_message(filters.private)
async def echo(client_object, message: Message):
    #client_object.send_message(message.chat.id, f"вы сказали: {message.text}")
    user_id = message.from_user.id
    text = message.text.lower()
    text_array = text.split(' ')
    with database.Session(autoflush=False, bind=database.engine) as session:
        print(database.Msg(user_id=user_id))
        test = session.query(database.Msg).filter(database.Msg.user_id == user_id).first()

        if 'понятно' in text_array or 'ожидать' in text_array:
            test.status = 'finished'
            test.status_updated_at = datetime.now()
            session.commit()
        else:
            if test is None:
                msg = database.Msg(user_id=user_id, created_at=datetime.strftime(datetime.now(), '%d/%m/%Y, %H:%M:%S'), status='alive', status_updated_at=datetime.strftime(datetime.now(), '%d/%m/%Y, %H:%M:%S'), current_step=1)
                session.add(msg)
                session.commit()
            else:
                pass
    while True:
        with database.Session(autoflush=False, bind=database.engine) as session:
            #test = session.query(database.Msg).all()

            step1 = session.query(database.Msg).filter(database.Msg.current_step == 1, database.Msg.status == 'alive').all()
            for tmp in step1:
                time_difference = datetime.now() - datetime.strptime(tmp.status_updated_at, '%d/%m/%Y, %H:%M:%S')
                minutes_difference = time_difference.total_seconds() / 60
                if minutes_difference > 6:
                    await client.send_message(tmp.user_id, config.text1)
                    tmp.status_updated_at = datetime.strftime(datetime.now(), '%d/%m/%Y, %H:%M:%S')
                    tmp.current_step = 2
                    session.commit()

            step2 = session.query(database.Msg).filter(database.Msg.current_step == 1, database.Msg.status == 'alive').all()
            for tmp in step2:
                time_difference = datetime.now() - datetime.strptime(tmp.status_updated_at, '%d/%m/%Y, %H:%M:%S')
                minutes_difference = time_difference.total_seconds() / 60
                if minutes_difference > 39:
                    await client.send_message(tmp.user_id, config.text2)
                    tmp.status_updated_at = datetime.strftime(datetime.now(), '%d/%m/%Y, %H:%M:%S')
                    tmp.current_step = 3
                    session.commit()

            step3 = session.query(database.Msg).filter(database.Msg.current_step == 1, database.Msg.status == 'alive').all()
            for tmp in step3:
                time_difference = datetime.now() - datetime.strptime(tmp.status_updated_at, '%d/%m/%Y, %H:%M:%S')
                minutes_difference = time_difference.total_seconds() / 60
                if minutes_difference > 1560:
                    await client.send_message(tmp.user_id, config.text3)
                    tmp.status_updated_at = datetime.strftime(datetime.now(), '%d/%m/%Y, %H:%M:%S')
                    tmp.statue = 'finished'
                    session.commit()

        await asyncio.sleep(5)


client.run()


if __name__ == '__main__':
    client.run()



