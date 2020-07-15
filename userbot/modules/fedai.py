""" UserBot yardım komutu """

from userbot import CMD_HELP
from userbot.events import extract_args, register


@register(outgoing=True, pattern="^.fedai")
async def fedai(event):
    """ .fedai komutu için """
    args = extract_args(event).lower()
    if args:
        if args in CMD_HELP:
            await event.edit(str(CMD_HELP[args]))
        else:
            await event.edit("Lütfen bir Fedai modülü adı belirtin.")
    else:
        await event.edit("Lütfen hangi Fedai modülü için yardım istediğinizi belirtin !!\
            \nKullanım: .fedai <modül adı>")
        string = "**[Fedai UserBot](https://telegram.dog/FedaiUserBot) Yüklü Modüller:**\n↓  ↓  ↓  ↓\n"
        for i in CMD_HELP:
            string += "🔸 - `" + str(i)
            string += "` \n"
        await event.reply(string)
