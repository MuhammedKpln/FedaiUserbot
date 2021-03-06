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
from asyncio import sleep

from userbot import BOTLOG, BOTLOG_CHATID, CMD_HELP
from userbot.events import extract_args, register


@register(outgoing=True, pattern="^.purge$")
async def fastpurger(purg):
    """ .purge komutu hedeflenen yanıttan başlayarak tüm mesajları temizler. """
    chat = await purg.get_input_chat()
    msgs = []
    itermsg = purg.client.iter_messages(chat, min_id=purg.reply_to_msg_id)
    count = 0

    if purg.reply_to_msg_id:
        async for msg in itermsg:
            msgs.append(msg)
            count = count + 1
            msgs.append(purg.reply_to_msg_id)
            if len(msgs) == 100:
                await purg.client.delete_messages(chat, msgs)
                msgs = []
    else:
        await purg.edit("`Temizlemeye başlamak için bir mesaja ihtiyacım var.`")
        return

    if msgs:
        await purg.client.delete_messages(chat, msgs)
    done = await purg.client.send_message(
        purg.chat_id, f"`Hızlı temizlik tamamlandı!`\
        \n{str(count)} tane mesaj silindi.")

    if BOTLOG:
        await purg.client.send_message(
            BOTLOG_CHATID,
            "Hedeflenen " + str(count) + " mesaj başarıyla silindi.")
    await sleep(2)
    await done.delete()


@register(outgoing=True, pattern="^.purgeme")
async def purgeme(delme):
    """ .purgeme komutu belirtilen miktarda kullanıcın mesajlarını siler. """
    count = extract_args(delme)
    if not count.isdigit():
        await delme.edit("`Temizlik yapılamadı, sayı geçersiz.`")
        return
    i = 1

    async for message in delme.client.iter_messages(delme.chat_id,
                                                    from_user='me'):
        if i > int(count) + 1:
            break
        i = i + 1
        await message.delete()

    smsg = await delme.client.send_message(
        delme.chat_id,
        "`Temizlik tamamlandı` " + str(count) + " tane mesaj silindi.",
    )
    if BOTLOG:
        await delme.client.send_message(
            BOTLOG_CHATID,
            "Hedeflenen " + str(count) + " mesaj başarıyla silindi.")
    await sleep(2)
    i = 1
    await smsg.delete()


@register(outgoing=True, pattern="^.del$")
async def delete_it(delme):
    """ .del komutu yanıtlanan mesajı siler. """
    msg_src = await delme.get_reply_message()
    if delme.reply_to_msg_id:
        try:
            await msg_src.delete()
            await delme.delete()
            if BOTLOG:
                await delme.client.send_message(
                    BOTLOG_CHATID, "Hedeflenen mesajın silinmesi başarılıyla tamamlandı")
        except:
            if BOTLOG:
                await delme.client.send_message(
                    BOTLOG_CHATID, "Bu mesajı silemiyorum.")


@register(outgoing=True, pattern="^.edit")
async def editer(edit):
    """ .editme komutu son mesajınızı düzenler. """
    message = edit.text
    chat = await edit.get_input_chat()
    self_id = await edit.client.get_peer_id('me')
    string = extract_args(edit)
    i = 1
    async for message in edit.client.iter_messages(chat, self_id):
        if i == 2:
            await message.edit(string)
            await edit.delete()
            break
        i = i + 1
    if BOTLOG:
        await edit.client.send_message(BOTLOG_CHATID,
                                       "Mesaj düzenleme sorgusu başarıyla yürütüldü")


@register(outgoing=True, pattern="^.sd")
async def selfdestruct(destroy):
    """ .sd komutu kendi kendine yok edilebilir mesajlar yapar. """
    args = extract_args(destroy)
    argv = args.split(' ', 1)
    if len(args) < 1 or len(argv) < 2 or not argv[0].isdigit():
        await destroy.edit("`Komut kullanımı hatalı.`")
        return
    counter = int(argv[0])
    text = argv[1]
    await destroy.delete()
    smsg = await destroy.client.send_message(destroy.chat_id, text)
    await sleep(counter)
    await smsg.delete()
    if BOTLOG:
        await destroy.client.send_message(BOTLOG_CHATID,
                                          "sd sorgusu başarıyla tamamlandı")


CMD_HELP.update({
    'purge':
        '.purge\
            \nKullanım: Hedeflenen yanıttan başlayarak tüm mesajları temizler.'
})

CMD_HELP.update({
    'purgeme':
        '.purgeme <x>\
            \nKullanım: Hedeflenen yanıttan başlayarak tüm mesajları temizler.'
})

CMD_HELP.update({"del": ".del\
\nKullanım: Yanıtladığınız mesajı siler."})

CMD_HELP.update({
    'edit':
        ".edit <yenimesaj>\
    \nKullanım: Son mesajanızı <yenimesaj> ile değiştirin."
})

CMD_HELP.update({
    'sd':
        '.sd <x> <mesaj>\
    \nKullanım: x saniye içinde kendini yok eden bir mesaj oluşturur.\
    \nBotunuzu uyku moduna geçirdiğinden, saniyeleri 100 ün altında tutun.'
})
