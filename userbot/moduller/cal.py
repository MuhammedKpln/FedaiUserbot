# Copyright (C) 2020 MuhammedKpln.
#
# FedaiUserBot is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# FedaiUserBot is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#

from userbot.events import register, extract_args
from userbot import bot, LOGS
import asyncio
from telethon import functions, types, events
from telethon.tl.functions.contacts import AddContactRequest, GetContactsRequest, GetStatusesRequest
from telethon.tl.types import UserStatusOnline, UserStatusRecently, ChannelParticipantsRecent
from asyncio import sleep
from telethon.tl.functions.channels import InviteToChannelRequest
from telethon.tl.functions.messages import AddChatUserRequest, DeleteChatUserRequest

stopPullingUsers = False

@register(outgoing=True, pattern=".sa")
async def _(event):

    global stopPullingUsers
    await event.edit('Merhabalar herkese')
    args = extract_args(event).split(' ')
    notifyUser = bool(args[1]) if len(args) > 1 else True
    limit = int(args[0]) if isinstance(args[0], int) else 1000

    sleepAfterAwhile = []
    async for user in event.client.iter_participants(event.chat_id, limit=int(limit), filter=ChannelParticipantsRecent):
        
        if stopPullingUsers:
            break
        
        
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
                
                
                if len(sleepAfterAwhile) > 4:
                    if notifyUser:
                        await _sendMessageToMainAccount(sleepAfterAwhile)
                    await sleep(61)
                    sleepAfterAwhile.clear()


            except Exception as err:
                LOGS.error(err)
                _sendMessageToMainAccount(user, str(err))

async def _sendMessageToMainAccount(users, message = ''):
    msg = message
    if not message:
        msg = ' , '.join(f'@{user.username}' or user.first_name for user in users) + ' Dizladimm...'

    LOGS.info(msg)
    sendToUser = await bot.get_entity(339388824)
    await bot.send_message(sendToUser, msg)


@register(outgoing=True, pattern='.kes')
async def _stopPullingUsers(event):
    global stopPullingUsers
    stopPullingUsers = True
    await event.edit('Ben kactim arkadaslar, kendinize iyi baghin')


@register(outgoing=True, pattern='.as')
async def uyebas(event):
    await event.edit('`USER DUMP BASLADI (Database yükleniyor..) - by` @hasanisabbah.')
    await sleep(3)
    # await event.edit('Görmediniz say eheheh')
    result = await event.client(GetContactsRequest(
        hash=0
    ))
    limit = 10
    # users = []
    # for userStatus in result:
    #     user = await bot.get_entity(userStatus.user_id)
    #     await event.edit(f'`{user.id}` kullanici hafizaya alindi..')
    #     users.append(user)

    #     if len(users) == limit:
    #         break
    try:
        # await event.edit('Eklemeler basladi..')
        await event.client(InviteToChannelRequest(
            channel=1425906189,
            users=result.users[:10]
        ))
    except Exception as e:
        print(e)


@register(outgoing=True, pattern="^.contacts")
async def contactsCount(event):
    try:
        await event.edit('`Rehber yükleniyor...`')
        result = await event.client(GetContactsRequest(hash=0))
        totalUsers = len(result.users)
        await event.edit(f'`Toplam rehber üye sayisi: {totalUsers}`')

    except Exception as e:
        await event.edit('`Bilinmeyen hata ile karsilastik..`')
        LOGS.exception(e)
        