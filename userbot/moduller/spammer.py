
import time
import threading
from pprint import pprint

from re import sub

from asyncio import wait, sleep

from userbot import BOTLOG, BOTLOG_CHATID, CMD_HELP, bot
from userbot.events import extract_args, extract_args_arr, register


@register(outgoing=True, pattern="^.savespamm")
async def add_new_spam(e):
    try:
        from userbot.moduller.sql_helper.spam import add_spam
    except:
        await e.edit("`Bot Non-SQL modunda çalışıyor!!`")
        return

    await e.edit('Bakiyorum suan')
    chat = await e.client.get_chat()
    await e.edit(','.join(await bot.iter_participants(chat, 40)))

    print(await bot.iter_participants(chat, 40))
    # print(await e.client.iter_participants)


    spamEvent = extract_args(e).split(' ')

    if len(spamEvent) < 2:
        await e.edit('`Doğru kullanım: .savespam spamİsmi atılacakSpam`')
        return
       
    spamName = spamEvent[0]
    spam = spamEvent[1]

    saveSpam = add_spam(spamName, spam)
    pprint( add_spam(spamName, spam))
    if saveSpam:
        await e.edit('Yeni spam başarılı bir şekilde eklendii.')
    else:
        await e.edit('`Yeni spam eklenirker bir hata meydana geldi!`')







@register(outgoing=True, pattern="^.tspam")
async def tmeme(e):
    message = extract_args(e)
    if len(message) < 1:
        await e.edit("`Bir şeyler eksik/yanlış gibi görünüyor.`")
        return
    await e.delete()
    for letter in message.replace(' ',''):
        await e.respond(letter)
    if BOTLOG:
            await e.client.send_message(
                BOTLOG_CHATID,
                "#TSPAM \n\n"
                "TSpam başarıyla gerçekleştirildi"
                )

@register(outgoing=True, pattern="^.spam")
async def bigspam(e):
    message = extract_args(e)
    if len(message) < 1:
        await e.edit("`Bir şeyler eksik/yanlış gibi görünüyor.`")
        return
    arr = message.split()
    if not arr[0].isdigit():
        await e.edit("`Bir şeyler eksik/yanlış gibi görünüyor.`")
        return
    await e.delete()
    counter = int(arr[0])
    spam_message = message.replace(arr[0],'').strip()
    for i in range(0, counter):
        await e.respond(spam_message)
    if BOTLOG:
         await e.client.send_message(
             BOTLOG_CHATID,
             "#BIGSPAM \n\n"
             "Bigspam başarıyla gerçekleştirildi"
            )

@register(outgoing=True, pattern="^.picspam")
async def tiny_pic_spam(e):
    arr = extract_args_arr(e)
    if len(arr) < 2 or not arr[0].isdigit():
        await e.edit("`Bir şeyler eksik/yanlış gibi görünüyor.`")
        return
    await e.delete()
    counter = int(arr[0])
    link = arr[1]
    for i in range(0, counter):
        await e.client.send_file(e.chat_id, link)
    if BOTLOG:
        await e.client.send_message(
            BOTLOG_CHATID,
            "#PICSPAM \n\n"
            "PicSpam başarıyla gerçekleştirildi"
            )

@register(outgoing=True, pattern="^.delayspam")
async def delayspammer(e):
    # Teşekkürler @ReversedPosix
    message = extract_args(e)
    arr = message.split()
    if len(arr) < 3 or not arr[0].isdigit() or not arr[1].isdigit():
        await e.edit("`Bir şeyler eksik/yanlış gibi görünüyor.`")
        return
    spam_delay = int(arr[0])
    counter = int(arr[1])
    spam_message = sub(f'{arr[0]}|{arr[1]}', '', message).strip()
    await e.delete()
    delaySpamEvent = threading.Event()
    for i in range(0, counter):
        await e.respond(spam_message)
        delaySpamEvent.wait(spam_delay)
    if BOTLOG:
        await e.client.send_message(
            BOTLOG_CHATID,
            "#DelaySPAM \n\n"
            "DelaySpam başarıyla gerçekleştirildi"
            )
                               
CMD_HELP.update({
    "spammer": ".tspam <metin>\
\nKullanım: Verilen mesajı tek tek göndererek spam yapar\
\n\n.spam <miktar> <metin>\
\nKullanım: Verilen miktarda spam gönderir\
\n\n.picspam <miktar> <link>\
\nKullanım: Verilen miktarda resimli spam gönderir\
\n\n.delayspam <gecikme> <miktar> <metin>\
\nKullanım: Verilen miktar ve verilen gecikme ile gecikmeli spam yapar\
\n\n\nNOT : Sorumluluk size aittir!!"
})
