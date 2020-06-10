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

import importlib
import os
import re
import time

from telethon.tl.types import DocumentAttributeFilename, InputMessagesFilterDocument

from userbot import CMD_HELP, PLUGIN_CHANNEL_ID, bot
from userbot.events import extract_args, register


@register(outgoing=True, pattern="^.pkur")
async def pins(event):
    if event.is_reply:
        reply_message = await event.get_reply_message()
        data = await check_media(reply_message)
    else:
        await event.edit("`Yüklenecek modül dosyasına yanıt verin.`")
        return

    await event.edit("`Dosya indiriliyor...`")
    dosya = await event.client.download_media(data, os.getcwd() + "/userbot/moduller/")

    if PLUGIN_CHANNEL_ID != None:
        await reply_message.forward_to(PLUGIN_CHANNEL_ID)
    else:
        event.reply(
            "`Pluginlerin kalıcı olması için Id ayarlamamışsınız. Pluginleriniz yeniden başlatınca silinebilir!`")

    try:
        spec = importlib.util.spec_from_file_location(dosya, dosya)
        mod = importlib.util.module_from_spec(spec)

        spec.loader.exec_module(mod)
    except Exception as e:
        await event.edit(f"`Yükleme başarısız! Plugin hatalı.\n\nHata: {e}`")
        os.remove(os.getcwd() + "/userbot/moduller/" + dosya)
        return

    dosy = open(dosya, "r").read()
    if "@tgbot.on" in dosy:
        komu = re.findall(r"(pattern=\")(.*)(\")(\))", dosy)
        komutlar = ""
        i = 0
        while i < len(komu):
            komut = komu[i][1]
            CMD_HELP[komut] = f"Bu plugin dışarıdan botunuz için yüklenmiştir. Kullanım: {komut}"
            komutlar += komut + " "
            i += 1
        await event.edit(f"`Modül başarıyla yüklendi! {komutlar} ile kullanmaya başlayabilirsiniz.`")
    else:
        try:
            komu = str(re.findall(r"(pattern=\")(.*)(\")(\))", dosy)[0][1]).replace("^", "").replace(".", "")
        except IndexError:
            zaman = time.time()
            CMD_HELP[zaman] = f"Bu plugin dışarıdan yüklenmiştir. Kullanım: #KOMUT BULUNAMADI#"
            await event.edit(f"`Modül başarıyla yüklendi! Fakat komutu bulamadım, üzgünüm.`")
            return

        CMD_HELP[komu] = f"Bu plugin dışarıdan yüklenmiştir. Kullanım: .{komu}"
        await event.edit(f"`Modül başarıyla yüklendi! .{komu} ile kullanmaya başlayabilirsiniz.`")


async def check_media(reply_message):
    if reply_message and reply_message.media:
        if reply_message.photo:
            data = reply_message.photo
        elif reply_message.document:
            if DocumentAttributeFilename(file_name='AnimatedSticker.tgs') in reply_message.media.document.attributes:
                return False
            if reply_message.gif or reply_message.video or reply_message.audio or reply_message.voice:
                return False
            data = reply_message.media.document
        else:
            return False
    else:
        return False

    if not data or data is None:
        return False
    else:
        return data


@register(outgoing=True, pattern="^.plistesi")
async def plist(event):
    if PLUGIN_CHANNEL_ID != None:
        await event.edit("`Pluginler getiriliyor...`")
        yuklenen = "**İşte Yüklenen Pluginler:**\n\n"
        async for plugin in event.client.iter_messages(PLUGIN_CHANNEL_ID, filter=InputMessagesFilterDocument):
            if str(plugin.file.name).endswith('.py'):
                yuklenen += f"▶️ {plugin.file.name}\n"
        await event.edit(yuklenen)
    else:
        await event.edit("`Pluginleriniz kalıcı yüklenmiyor bu yüzden liste getiremem.`")


@register(outgoing=True, pattern="^.phepsinikur")
async def pinstallall(event):
    PLUGINS_TO_BE_INSTALLED = []
    if PLUGIN_CHANNEL_ID != None:
        await event.edit("`Pluginler getiriliyor...`")
        async for plugin in event.client.iter_messages(PLUGIN_CHANNEL_ID, filter=InputMessagesFilterDocument):

            raw_name = plugin.file.name
            file_name = str(plugin.file.name).strip('.')[0]
            modules_folder = os.getcwd() + "/userbot/moduller/"

            if str(plugin.file.name).endswith('.py'):

                if os.path.exists(os.path.join(modules_folder, raw_name)):
                    await event.reply(f'`{raw_name}` **Modül zaten yüklenmis.**')
                else:
                    data = await check_media(plugin)
                    dosya = await event.client.download_media(data, modules_folder)

                    spec = importlib.util.spec_from_file_location(dosya, dosya)
                    mod = importlib.util.module_from_spec(spec)

                    spec.loader.exec_module(mod)

        await event.edit('`Modüller başarılı bir şekilde yüklendi..`')

    else:
        await event.edit("`Pluginleriniz kalıcı yüklenmiyor bu yüzden işlem iptal edildi.`")


async def installPlugins():
    async for plugin in bot.iter_messages(PLUGIN_CHANNEL_ID, search="{KURBUNU}"):
        pins


@register(outgoing=True, pattern="^.psil ?(.*)")
async def premove(event):
    plugin_to_be_removed = extract_args(event)
    async for plugin in event.client.iter_messages(PLUGIN_CHANNEL_ID, search=plugin_to_be_removed):
        print(plugin)
        modules_folder = os.getcwd() + "/userbot/moduller/"

        if plugin_to_be_removed.endswith('.py'):

            if os.path.exists(os.path.join(modules_folder, plugin_to_be_removed)):
                os.remove(os.path.join(modules_folder, plugin_to_be_removed))
                await event.edit(f'`{plugin_to_be_removed}` **Modül silindi.**')
            else:
                await event.edit('** Aradığınız modül bulunamadı.. **')

        else:
            await event.edit('** Aradığınız modül bulunamadı.. **')
