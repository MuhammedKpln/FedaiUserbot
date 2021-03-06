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

from userbot import BOT_USERNAME
from userbot.events import register

@register(outgoing=True, pattern="^.yardım")
async def yardim(event):
    tgbotusername = BOT_USERNAME
    if tgbotusername and len(tgbotusername) > 4:
        try:
            results = await event.client.inline_query(
                tgbotusername,
                "@FedaiUserBot"
            )
            await results[0].click(
                event.chat_id,
                reply_to=event.reply_to_msg_id,
                hide_via=True
            )
            await event.delete()
        except:
            await event.edit("`Botunda inline modunu açman gerekiyor.`")
    else:
        await event.edit("`Bot çalışmıyor! Lütfen Bot Tokeni ve Kullanıcı adını doğru ayarlayın. Modül durduruldu.`")
