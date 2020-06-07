from sedenbot.events import sedenify, extract_args
from sedenbot import bot, LOGS
import asyncio
from telethon import functions, types, events
from telethon.tl.functions.contacts import AddContactRequest, GetContactsRequest, GetStatusesRequest
from telethon.tl.types import UserStatusOnline, UserStatusRecently, ChannelParticipantsRecent
from time import sleep
from telethon.tl.functions.channels import InviteToChannelRequest
from telethon.tl.functions.messages import AddChatUserRequest, DeleteChatUserRequest

@sedenify(outgoing=True, pattern=".sa")
async def _(event):
    await event.edit('Merhabalar herkese')
    limit = extract_args(event)
    print(f'limit {limit}') 
    sleepAfterAwhile = []
    async for user in event.client.iter_participants(event.chat_id, limit=int(limit)):
        # if isinstance(user.status, UserStatusOnline):
        if not user.bot and not user.contact and not user.is_self:
            print(user.first_name)
            try:
                result = await event.client(AddContactRequest(
                    id=int(user.id),
                    first_name=str(user.first_name),
                    last_name=str(user.last_name) if user.last_name else '',
                    phone='' if not user.phone else str(user.phone),
                    add_phone_privacy_exception=False
                ))
                sleepAfterAwhile.append(user)
                # sendToUser = await bot.get_entity(339388824)
                # await bot.send_message(sendToUser, f'@{user.username or user.first_name} `kullanicisini dizladim oglim`')
                if len(sleepAfterAwhile) > 4:
                    print('Uyuyuorum suan ', len(sleepAfterAwhile))
                    sleep(61)
                    sleepAfterAwhile.clear()
            except Exception as err:
                # e = sys.exc_info()[0]
                print(err)


@sedenify(outgoing=True, pattern='.as')
async def uyebas(event):
    await event.edit('`USER DUMP BASLADI (Database yükleniyor..) - HASSANSABBAH.`')
    # await event.edit('Görmediniz say eheheh')
    result = await event.client(GetStatusesRequest())
    users = []
    for userStatus in result:
        user = await bot.get_entity(userStatus.user_id)
        users.append(user)

        if len(users) == 20:
            break
    try:
        await event.edit('Eklemeler basladi..')
        await event.client(InviteToChannelRequest(
            channel=1371749757,
            users=users
        ))
    except Exception as e:
        print(e)


@sedenify(outgoing=True, pattern="^.contacts")
async def contactsCount(event):
    try:
        await event.edit('`Rehber yükleniyor...`')
        result = await event.client(GetContactsRequest(hash=0))
        totalUsers = len(result.users)
        await event.edit(f'`Toplam rehber üye sayisi: {totalUsers}`')

    except Exception as e:
        await event.edit('`Bilinmeyen hata ile karsilastik..`')
        LOGS.exception(e)
        