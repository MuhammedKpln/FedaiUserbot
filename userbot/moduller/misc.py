
""" Birkaç küçük komutu içeren UserBot modülü. """

from io import BytesIO
from sys import executable, argv

from os import execl
from random import randint
from asyncio import sleep

from userbot import BOTLOG, BOTLOG_CHATID, CMD_HELP, bot
from userbot.events import extract_args, register, me

@register(outgoing=True, pattern="^.random")
async def randomise(items):
    """ .random komutu, eşya listesinden rastgele bir eşya seçer. """
    itemo = (items.text[8:]).split()
    if len(itemo) < 2:
        await items.edit(
            "`2 veya daha fazla eşya gerekli. Daha fazla bilgi için .fedai random komutunu gir.`"
        )
        return
    index = randint(1, len(itemo) - 1)
    await items.edit("**Sorgu: **\n`" + items.text[8:] + "`\n**Çıktı: **\n`" +
                     itemo[index] + "`")

@register(outgoing=True, pattern="^.sleep")
async def sleepybot(time):
    """ .sleep komutu Fedai'in birkaç saniye uyumasına olanak sağlar. """
    args = extract_args(time)
    if len(args) < 1 or not args.isdigit():
        await time.edit("Kullanım Şekli: `.sleep [saniye]`")
    else:
        counter = int(args)
        await time.edit("`Horlayarak uyuyorum...`")
        await sleep(2)
        if BOTLOG:
            await time.client.send_message(
                BOTLOG_CHATID,
                f"#SLEEP\nBotu {counter} saniye uykuya bıraktın.",
            )
        await sleep(counter)
        await time.edit("`Günaydın!`")

@register(outgoing=True, pattern="^.shutdown$")
async def shutdown(event):
    """ .shutdown komutu botu kapatır. """
    await event.edit("`Görüşürüz... *Windows XP kapanma sesi*`")
    if BOTLOG:
        await event.client.send_message(BOTLOG_CHATID, "#SHUTDOWN \n"
                                        "Bot kapatıldı.")
    try:
        await bot.disconnect()
    except:
        pass

@register(outgoing=True, pattern=".alive")
async def alive(event):
        DEFAULTUSER =  me.first_name
        await event.edit("**İSTATİSTİKLERİM** \n` ŞUAN :` **✅ ÇALIŞIYORUM **\n\n"
                     "`TELETHON VERSİYONU:` **6.0.9**\n`Python:` **3.7.4**\n"
                     "`VERİTABANİ:` **HERŞEY YOLUNDA 🙂**\n`HİÇ BİR PROBLEM BULUNMADI🔥!\n`"
                     "`DEPLOY SERVİSİ: HEROKU INC.\n"
                     "`IP:` Hmm..\n"
                     "`İŞLETİM SİSTEMİ:` LINUX\n"
                     "`UYDU:` ⚡TÜRKSAT-3A⚡\n"
                     "`KODLAMA DİLİ:` PYTHON\n"
                     f"`PATRONUM`: {DEFAULTUSER}\n\n"
                     "`UYDU DURUMU: ✅ UYGUN\n\n"
                     "[⚡ PATRONUM OLMAYA NE DERSİN?⚡](https://github.com/muhammedkpln/fedaiuserbot)") 
    

@register(outgoing=True, pattern="^.restart$")
async def restart(event):
    await event.edit("`Bot yeniden başlatılıyor...`")
    if BOTLOG:
        await event.client.send_message(BOTLOG_CHATID, "#RESTART \n"
                                        "Bot yeniden başlatıldı.")

    try:
        await bot.disconnect()
    except:
        pass

    execl(executable, executable, *argv)

@register(outgoing=True, pattern="^.support$")
async def bot_support(wannahelp):
    """ .support komutu destek grubumuzu verir. """
    await wannahelp.edit("[Buradan](http://t.me/FedaiUserBotSupport) destek grubumuza ulaşabilirsiniz.")

@register(outgoing=True, pattern="^.creator$")
async def creator(e):
    await e.edit("========================= \n\n"
                 "Bu bot \n"
                 "[MuhammedKpln](https://t.me/hasanisabbah) tarafından geliştirilip \n"
                 "=========================")

@register(outgoing=True, pattern="^.readme$")
async def reedme(e):
    await e.edit("[Fedai README.md](https://github.com/muhammedkpln/fedaiuserbot/blob/fedai/README.md)")

# Copyright (c) Gegham Zakaryan | 2019
@register(outgoing=True, pattern="^.repeat")
async def repeat(rep):
    args = extract_args(rep).split(' ', 1)
    if len(args) < 2:
        await rep.edit("`Kullanım şekli hatalı.`")
        return
    cnt, txt = args
    if not cnt.isdigit():
        await rep.edit("`Kullanım şekli hatalı.`")
        return
    replyCount = int(cnt)
    toBeRepeated = txt

    replyText = toBeRepeated + "\n"

    for i in range(0, replyCount - 1):
        replyText += toBeRepeated + "\n"

    await rep.edit(replyText)

@register(outgoing=True, pattern="^.repo$")
async def repo_is_here(wannasee):
    """ .repo komutunun tek yaptığı şey GitHub repomuzun bağlantısını vermek. """
    await wannasee.edit("[Fedai Repo](https://github.com/muhammedkpln/fedaiuserbot)")

@register(outgoing=True, pattern="^.raw$")
async def raw(event):
    the_real_message = None
    reply_to_id = None
    if event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        the_real_message = previous_message.stringify()
        reply_to_id = event.reply_to_msg_id
    else:
        the_real_message = event.stringify()
        reply_to_id = event.message.id
    with BytesIO(str.encode(the_real_message)) as out_file:
        out_file.name = "raw_message_data.txt"
        await event.edit(
            "`Çözülmüş mesaj için UserBot loglarını kontrol et!`")
        await event.client.send_file(
            BOTLOG_CHATID,
            out_file,
            force_document=True,
            allow_cache=False,
            reply_to=reply_to_id,
            caption="`Çözülen mesaj`")

CMD_HELP.update({
    'random':
    '.random <eşya1> <eşya2> ... <eşyaN>\
\nKullanım: Eşya listesinden rastgele bir eşya seçer'
})

CMD_HELP.update({
    'sleep':
    '.sleep <saniye>\
\nKullanım: Fedai de bir insan, o da yoruluyor. Ara sıra biraz uyumasına izin ver.'
})

CMD_HELP.update({
    "shutdown":
    ".shutdown\
\nKullanım: Bazen canın botunu kapatmak ister. Gerçekten o nostaljik\
Windows XP kapanış sesini duyabileceğini zannedersin..."
})

CMD_HELP.update(
    {'support': ".support\
\nKullanım: Yardıma ihtiyacın olursa bu komutu kullan."
     })

CMD_HELP.update({
    'repo':
    '.repo\
\nKullanım: Fedai UserBot GitHub reposu'
})

CMD_HELP.update({
    "readme":
    ".readme\
\nKullanım: Fedai botunun GitHub'daki README.md dosyasına giden bir bağlantı."
})

CMD_HELP.update(
    {"creator": ".creator\
\nKullanım: Bu güzel botu kimlerin oluşturduğunu öğren :-)"})

CMD_HELP.update({
    "repeat":
    ".repeat <sayı> <metin>\
\nKullanım: Bir metni belli bir sayıda tekrar eder. Spam komutu ile karıştırma!"
})

CMD_HELP.update({"restart": ".restart\
\nKullanım: Botu yeniden başlatır."})

CMD_HELP.update({
    "raw":
    ".raw\
\nKullanım: Kullanılan mesaj hakkında JSON'a benzer bir şekilde detaylı bilgiler verir."
})
