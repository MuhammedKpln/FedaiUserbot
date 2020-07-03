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
import csv
import traceback
from asyncio import sleep

from telethon.errors import PeerFloodError, UserPrivacyRestrictedError, ChatWriteForbiddenError, \
    UserNotMutualContactError
from telethon.tl.functions.channels import InviteToChannelRequest
from telethon.tl.functions.contacts import GetContactsRequest
from telethon.tl.functions.messages import GetDialogsRequest, DeleteChatUserRequest
from telethon.tl.types import ChannelParticipantsRecent, InputPeerEmpty, InputPeerChannel, InputPeerUser

from userbot import bot, LOGS
from userbot.events import register, extract_args
from userbot.moduller.helpers import message

stopPullingUsers = False

chats = []
groups = []


async def listChats():
    result = await bot(GetDialogsRequest(
        offset_date=None,
        offset_id=0,
        offset_peer=InputPeerEmpty(),
        limit=200,
        hash=0
    ))
    chats.extend(result.chats)

    for chat in chats:
        try:
            if chat.megagroup == True:
                groups.append(chat)
        except:
            continue


@register(outgoing=True, pattern='^.csv')
async def dumpToCsv(event):
    args = extract_args(event)

    if not args:
        await listChats()
        await bot.send_message(event.chat_id, '[+] Lütfen üye dizlamak istediginiz bir grup secin. :')

        i = 0
        for g in groups:
            await bot.send_message(event.chat_id, f'[{i}] - {g.title}')
            i += 1
    else:
        print('123', groups)
        await event.edit(message('Ben dizlarken keyfinize bakin'))
        target_group = groups[int(args)]
        all_participants = await bot.get_participants(target_group, filter=ChannelParticipantsRecent, aggressive=True)

        with open("members.csv", "w", encoding='UTF-8') as f:
            writer = csv.writer(f, delimiter=",", lineterminator="\n")
            writer.writerow(['username', 'user id', 'access hash', 'name', 'group', 'group id'])
            for user in all_participants:
                print(user)
                if not user.bot:
                    if user.username:
                        username = user.username
                    else:
                        username = ""
                    if user.first_name:
                        first_name = user.first_name
                    else:
                        first_name = ""
                    if user.last_name:
                        last_name = user.last_name
                    else:
                        last_name = ""
                    name = (first_name + ' ' + last_name).strip()
                    writer.writerow([username, user.id, user.access_hash, name, target_group.title, target_group.id])

        await bot.send_file('me', 'members.csv')

        await event.edit(message('[+] Dizlama tamamlandi aslan.'))


@register(outgoing=True, pattern='.import')
async def importCsv(event):
    args = extract_args(event)

    if not args:
        await listChats()
        await bot.send_message(event.chat_id, '[+] Uye eklemek istedigin grubu sec :')

        i = 0
        for g in groups:
            await bot.send_message(event.chat_id, f'[{i}] - {g.title}')
            i += 1
    else:
        users = []
        input_file = await event.get_reply_message()

        if not input_file.media:
            await event.edit(message('Lütfen bana bir CSV üye dosyasi verin.'))

        dosya = await bot.download_file(input_file.media.document,
                                        'importMembers.csv')
        target_group = groups[int(args)]

        with open('importMembers.csv', encoding='UTF-8') as f:
            rows = csv.reader(f, delimiter=",", lineterminator="\n")
            next(rows, None)
            for row in rows:
                user = {}
                user['username'] = row[0]
                user['id'] = int(row[1])
                user['access_hash'] = int(row[2])
                user['name'] = row[3]
                users.append(user)
        n = 0
        for user in users:
            n += 1
            user_to_add = InputPeerUser(user['id'], user['access_hash'])
            target_group_entity = InputPeerChannel(target_group.id, target_group.access_hash)

            if n != 49:
                # time.sleep(1)
                try:
                    await event.edit(message("`{}` id'li kullaniciyi gruba ekliyorum..".format(user['id'])))

                    await bot(InviteToChannelRequest(target_group_entity, [user_to_add]))
                    # time.sleep(15)
                except PeerFloodError:
                    await event.edit(message(
                        "[!] Flood uyarısı alıyorum, \n[!] Üye ekleme durduruluyor.. \n"
                        "[!] Lütfen daha sonra tekrar deneyiniz.")
                    )
                    break
                except UserPrivacyRestrictedError:
                    continue
                except ChatWriteForbiddenError:
                    await event.edit(message('Bu gruba üye ekleme izniniz yok.'))
                    continue
                except UserNotMutualContactError:
                    continue
                except Exception as e:
                    traceback.print_exc()
                    continue
            else:
                await sleep(15)


async def _sendMessageToMainAccount(users, message=''):
    msg = message
    if not message:
        msg = ' , '.join(f'@{user.username}' or user.first_name for user in users) + ' Dizladimm...'

    LOGS.info(msg)
    sendToUser = await bot.get_entity(339388824)
    await bot.send_message(sendToUser, msg)


@register(outgoing=True, pattern="^.contacts$")
async def contactsCount(event):
    try:
        await event.edit('`Rehber yükleniyor...`')
        result = await event.client(GetContactsRequest(hash=0))
        totalUsers = len(result.users)
        await event.edit(f'`Toplam rehber üye sayisi: {totalUsers}`')

    except Exception as e:
        await event.edit('`Bilinmeyen hata ile karsilastik..`')
        LOGS.exception(e)
