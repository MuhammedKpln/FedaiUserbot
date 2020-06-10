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

from telethon import events
from telethon.errors.rpcerrorlist import YouBlockedUserError

from userbot import bot, CMD_HELP
from userbot.events import register


@register(outgoing=True, pattern=".tara ?(.*)")
async def virusscanner(event):
    if event.fwd_from:
        return
    if not event.reply_to_msg_id:
        await event.edit("```Lütfen bir mesaj alıntılayın..```")
        return
    reply_message = await event.get_reply_message()
    if not reply_message.media:
        await event.edit("```Alıntıladığınız mesajda herhangi bir dosya bulunmadı..```")
        return
    chat = "@DrWebBot"
    sender = reply_message.sender
    if reply_message.sender.bot:
        await event.edit("```Reply to actual users message.```")
        return
    await event.edit(" `Sliding my tip, of fingers over it`")
    async with bot.conversation(chat) as conv:
        msg = await reply_message.forward_to(chat)
        message_edited = await conv.wait_event(events.NewMessage(chat))
        response = await conv.get_response(message=msg, timeout=5)
        if response.message.startswith("Select"):
            await event.edit("`Lütfen @DrWebBot bot ile açılmış sohbette` `bir dil seçtikten sonra yeniden deneyin..`")
        else:
            await event.edit(f"**Virus taraması bitti, işte sonuçlar..**\n {response.message}")


@register(outgoing=True, pattern="^.voicy")
async def voicy(event):
    if event.fwd_from:
        return
    if not event.reply_to_msg_id:
        await event.edit("`Herhangi bir kullanıcı mesajına cevap verin.`")
        return
    reply_message = await event.get_reply_message()
    if not reply_message.voice:
        await event.edit("`Mesaja cevap verin.`")
        return
    chat = "@voicybot"
    sender = reply_message.sender
    if reply_message.sender.bot:
        await event.edit("`Botlara cevap veremezsiniz.`")
        return
    await event.edit("`İşleniyor...`")
    async with bot.conversation(chat, exclusive=False) as conv:
        response = None
        try:
            msg = await reply_message.forward_to(chat)
            await event.edit('`Sizi 3 saniye bekletmek zorunda kalacam..`')
            message_edited = await conv.wait_event(events.MessageEdited(chat))
            response = await conv.get_response(message=msg, timeout=5)
        except YouBlockedUserError:
            await event.edit(f"`Lütfen {chat} engelini kaldırın ve tekrar deneyin`")
            return
        except Exception as e:
            print(e.__class__)

        if not response:
            await event.edit("`Botdan cevap alamadım!`")
        elif response.text.startswith("Forward"):
            await event.edit("`Gizlilik ayarları yüzenden alıntı yapamadım`")
        else:
            await event.edit(f'**Şşş, Sanırım bunları duydum**: `{response.text}`')
            await bot.send_read_acknowledge(chat, max_id=(response.id + 3))
            await conv.cancel_all()


@register(outgoing=True, pattern="^.sangmata")
async def _(event):
    if event.fwd_from:
        return
    if not event.reply_to_msg_id:
        await event.edit("`Herhangi bir kullanıcı mesajına cevap verin.`")
        return
    reply_message = await event.get_reply_message()
    if not reply_message.text:
        await event.edit("`Mesaja cevap verin.`")
        return
    chat = "@SangMataInfo_bot"
    sender = reply_message.sender
    if reply_message.sender.bot:
        await event.edit("`Botlara cevap veremezsiniz.`")
        return
    await event.edit("`İşleniyor...`")
    async with bot.conversation(chat, exclusive=False) as conv:
        response = None
        try:
            msg = await reply_message.forward_to(chat)
            response = await conv.get_response(message=msg, timeout=5)
        except YouBlockedUserError:
            await event.edit(f"`Lütfen {chat} engelini kaldırın ve tekrar deneyin`")
            return
        except Exception as e:
            print(e.__class__)

        if not response:
            await event.edit("`Botdan cevap alamadım!`")
        elif response.text.startswith("Forward"):
            await event.edit("`Gizlilik ayarları yüzenden alıntı yapamadım`")
        else:
            await event.edit(response.text)
        await bot.send_read_acknowledge(chat, max_id=(response.id + 3))
        await conv.cancel_all()


CMD_HELP.update({
    "voicy":
        ".voicy \
        \nKullanım: Ses atan kullanıcının sesini alıntılayın.\n",
    "sangmata":
        ".sangmata \
        \nKullanım: Kullanıcının mesajını alıntılayın, isim geçmişini gösterir.\n",
    "tara":
        ".tara \
        \nKullanım: Alıntılanan dosyada virus taraması gerçekleştirir.\n",

},
)
