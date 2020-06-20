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

from telethon.events import NewMessage

from userbot import LOGS, CMD_HELP, BOTLOG, BOTLOG_CHATID
from userbot.events import extract_args, register
from userbot.moduller.helpers import message

try:
    from userbot.moduller.sql_helper.spam import add_spam, remove_spam, get_spam, get_spams
except Exception as e:
    LOGS.error(e)


@register(outgoing=True, pattern='^.spam ?(.*)')
async def getspam(e: NewMessage.Event) -> None:
    spam_name = extract_args(e)
    print(spam_name)
    if not spam_name:
        await e.edit(message('Lütfen bana bir spam ismi verin.'))
        return

    spam = get_spam(spam_name)

    if spam:
        await e.edit(spam)
    else:
        await e.edit(message(f'{spam_name} ismiyle herhangi bir spam bulunamadi.'))


@register(outgoing=True, pattern="^.spamkaydet ?(.*)")
async def add_new_spam(e):
    await e.edit('**FEDAI**: `Peki, bana bir dakika verin, yeni spamınız kaydoluyor..`')

    args = extract_args(e).split(' ')

    if len(args) < 2:
        await e.edit('**FEDAI**: `Doğru kullanım: .spamkaydet spamİsmi atılacakSpam`')
        return

    spam_name = args[0]
    spam = args[1]

    try:
        save_spam = add_spam(spam_name, spam)

        if save_spam:
            await e.edit('**FEDAI**: `Yeni spam başarılı bir şekilde eklendi!`')
        else:
            await e.edit(
                '**FEDAI**: `Yeni spam eklenirken bir hata meydana geldi!'
                '\n\n Daha önce kullanmadığınız bir spam ismi ile kaydetmeyi deneyin.`')

    except Exception as e:
        LOGS.error(e)
        print(e)


@register(outgoing=True, pattern='^.kspam$')
async def spams(e: NewMessage.Event) -> None:
    spams = get_spams()

    transact = message('Kaydedilmiş herhangi bir spamınız bulunmamakta.')

    for spam in spams:
        transact = "Kaydedilmiş spamlarınız:\n"
        transact += "`{}`\n".format(spam.spam_name)

    print(spams)
    await e.edit(transact)


@register(outgoing=True, pattern='^.spamsil ?(.*)')
async def rmspam(e: NewMessage.Event) -> None:
    spam_name = extract_args(e)

    if not spam_name:
        await e.edit(message('Lütfen bana bir spamm ismi verin.'))
        return

    await e.edit(message('Lütfen bekleyiniz..'))

    spam = remove_spam(spam_name)

    if spam:
        await e.edit(message('Kaydedilen spam başarılı bir şekilde silindi!'))
    else:
        await e.edit(message(f'{spam_name} ismiyle herhangi bir spam bulunamadi.'))


@register(outgoing=True, pattern="^.bigspam")
async def bigspam(e):
    if not e.text[0].isalpha() and e.text[0] not in ("/", "#", "@", "!"):
        message = e.text
        messageSplit = message.split(" ", 2)
        counter = int(messageSplit[1])
        spam_message = str(messageSplit[2])
        for i in range(1, counter):
            await e.respond(spam_message)
        await e.delete()
        if BOTLOG:
            await e.client.send_message(
                BOTLOG_CHATID,
                "#BIGSPAM \n\n"
                "Bigspam başarıyla gerçekleştirildi"
                )


CMD_HELP.update({
    'spam': message('Kaydettiğiniz spamı gösterir'),
    'spamekle': message('Yeni bir spam ekler \n\n Kullanım: .spamekle spamİsmi spam'),
    'spamsil': message('Kaydettiğiniz spami siler \n\n Kullanım: .spamsil spamİsmi'),
    'kspam': message('Tüm spamlerinizi listeler.'),
    'bigspam': message('Kullanim: .bigspam <miktar> <metin>')
})