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

import asyncio
from asyncio import sleep
from collections import deque

from userbot import CMD_HELP, BOTLOG_CHATID, BOTLOG
from userbot.events import extract_args, register


@register(outgoing=True, pattern="^.hack")
async def port_hack(event):
    if event.fwd_from:
        return
    message = extract_args(event)

    animation_interval = 3
    animation_ttl = range(0, 11)
    # input_str = event.pattern_match.group(1)
    # if input_str == "hack":
    await event.edit("Hacking..")
    animation_chars = [
        "`Connecting To Hacked Private Server...`",
        "`Target Selected.`",
        "`Hacking... 0%\n▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ `",
        "`Hacking... 4%\n█▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ `",
        "`Hacking... 8%\n██▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ `",
        "`Hacking... 20%\n█████▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ `",
        "`Hacking... 36%\n█████████▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ `",
        "`Hacking... 52%\n█████████████▒▒▒▒▒▒▒▒▒▒▒▒ `",
        "`Hacking... 84%\n█████████████████████▒▒▒▒ `",
        "`Hacking... 100%\n█████████HACKED███████████ `",
        f"`Targeted Account Hacked by @hasanisabbah...\n\n {message} `"
    ]

    for i in animation_ttl:
        await asyncio.sleep(animation_interval)
        await event.edit(animation_chars[i % 11])


@register(outgoing=True, pattern="^.mizah$")
async def mizahshow(e):
    await e.edit(
        "⚠️⚠️⚠️MmMmMmMizahh Şoww😨😨😨😨😱😱😱😱😱 \n"
        "😱😱⚠️⚠️ 😂😂😂😂😂😂😂😂😂😂😂😂😂😂😱😵 \n"
        "😂😂👍👍👍👍👍👍👍👍👍👍👍👍👍 MiZah \n"
        "ŞeLaLesNdEn b1r yUdm aLdım✔️✔️✔️✔️ \n"
        "AHAHAHAHAHAHHAHAHAHAHAHAHAHAHAHAHAHHAHAHAHAHA \n"
        "HAHAHAHAHAHAHHAHAHAHAHAHAHA😂😂😂😂😂😂😂😂 \n"
        "😂 KOMİK LAN KOMİİİK \n"
        "heLaL LaN ✔️✔️✔️✔️✔️✔️✔️✔️👏👏👏👏👏👏👏👏 \n"
        "👏 EfSaNe mMmMiZah şooooovv 👏👏👏👏👏😂😂😂😂 \n"
        "😂😂😂😂😂😂⚠️ \n"
        "💯💯💯💯💯💯💯💯💯 \n"
        "KNK AYNI BİİİZ 😂😂😂👏👏 \n"
        "💯💯⚠️⚠️♿️AÇ YOLU POST SAHİBİ VE ONU ♿️SAVUNANLAR \n"
        "GELIYOR ♿️♿️ DÜÜTT♿️ \n"
        "DÜÜÜÜT♿️DÜÜT♿️💯💯⚠️ \n"
        "♿️KOMİİİK ♿️ \n"
        "CJWJCJWJXJJWDJJQUXJAJXJAJXJWJFJWJXJAJXJWJXJWJFIWIXJQJJQJASJAXJ \n"
        "AJXJAJXJJAJXJWJFWJJFWIIFIWICIWIFIWICJAXJWJFJEICIIEICIEIFIWICJSXJJS \n"
        "CJEIVIAJXBWJCJIQICIWJSX💯💯💯💯💯💯😂😂😂😂😂😂😂 \n"
        "😂⚠️😂😂😂😂😂😂⚠️⚠️⚠️😂😂😂😂♿️♿️♿️😅😅 \n"
        "😅😂👏💯⚠️👏♿️🚨"
    )


@register(pattern=r".type(?: |$)(.*)", outgoing=True)
async def typewriter(typew):
    message = extract_args(typew)
    sleep_time = 0.03
    typing_symbol = "|"
    old_text = ""

    if not message:
        typew.edit('** Lütfen bana bir metin ver. **')
        return

    await typew.edit(typing_symbol)
    await sleep(sleep_time)
    for character in message:
        old_text = old_text + "" + character
        typing_text = old_text + "" + typing_symbol
        await typew.edit(typing_text)
        await sleep(sleep_time)
        await typew.edit(old_text)
        await sleep(sleep_time)


@register(outgoing=True, pattern="^.kalp (.*)")
async def _(event):
    if event.fwd_from:
        return
    input_str = extract_args(event)
    deq = deque(list("️❤️🧡💛💚💙💜🖤"))
    for _ in range(32):
        await asyncio.sleep(0.1)
        await event.edit("".join(deq))
        deq.rotate(1)
    await event.edit("❤️🧡💛" + input_str + "💚💙💜")


@register(outgoing=True, pattern=".ddg")
async def ddg(event):
    if event.fwd_from:
        return
    input_str = extract_args(event)
    sample_url = "https://duckduckgo.com/?q={}".format(
        input_str.replace(" ", "+"))
    if sample_url:
        link = sample_url.rstrip()
        await event.edit(
            "**Bir dakika senin için 🦆 DuckDuckGo üzerinden arama yapıyorum**:\n🔎 [{}]({})".format(input_str, link))
    else:

        await event.edit("Bir şeyler ters gitti...")


@register(outgoing=True, pattern=r"^.tts(?: |$)([\s\S]*)")
async def text_to_speech(query):
    from gtts import gTTS
    from os import remove

    textx = await query.get_reply_message()
    message = query.pattern_match.group(1)
    TTS_LANG = "tr"

    if message:
        pass
    elif textx:
        message = textx.text
    else:
        await query.edit(
            "`Yazıdan sese çevirmek için bir metin gir.`")
        return

    try:
        gTTS(message, lang=TTS_LANG)
    except AssertionError:
        await query.edit(
            'Metin boş.\n'
            'Ön işleme, tokenizasyon ve temizlikten sonra konuşacak hiçbir şey kalmadı.'
        )
        return
    except ValueError:
        await query.edit('Bu dil henüz desteklenmiyor.')
        return
    except RuntimeError:
        await query.edit('Dilin sözlüğünü görüntülemede bir hata gerçekleşti.')
        return
    tts = gTTS(message, lang=TTS_LANG)
    tts.save("h.mp3")
    with open("h.mp3", "rb") as audio:
        linelist = list(audio)
        linecount = len(linelist)
    if linecount == 1:
        tts = gTTS(message, lang=TTS_LANG)
        tts.save("h.mp3")
    with open("h.mp3", "r"):
        await query.client.send_file(query.chat_id, "h.mp3", voice_note=True)
        remove("h.mp3")
        if BOTLOG:
            await query.client.send_message(
                BOTLOG_CHATID, "Metin başarıyla sese dönüştürüldü!")
        await query.delete()


CMD_HELP.update({
    "hack":
        ".hack \
        \nKullanım: Hacking animasyonudur.\n",
    "mizah":
        ".mizah \
        \nKullanım: Mizah selalesinden bir yudum alin.\n",
    "type":
        ".type \
        \nKullanım: Yazilarinizi animasyonu bir sekilde yazin.\n",
    "ddg":
        ".ddg \
        \nKullanım: Usengecler icin ddg aramasi gerceklestirin.\n",
    "tts":
        ".tts \
        \nKullanım: komutu ile Google'ın metinden yazıya dönüştürme servisi kullanılabilir..\n",
})
