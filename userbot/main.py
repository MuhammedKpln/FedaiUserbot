
""" UserBot başlangıç noktası """

from importlib import import_module
from sqlite3 import connect
from asyncio import run as runas
from requests import get
from os import path, remove

from telethon.errors.rpcerrorlist import PhoneNumberInvalidError
from . import BRAIN_CHECKER, BLACKLIST, LOGS, bot
from .moduller import ALL_MODULES

INVALID_PH = '\nHATA: Girilen telefon numarası geçersiz' \
             '\n  Ipucu: Ülke kodunu kullanarak numaranı gir' \
             '\n       Telefon numaranızı tekrar kontrol edin'

try:
    bot.start()
except PhoneNumberInvalidError:
    print(INVALID_PH)
    exit(1)

for module_name in ALL_MODULES:
    try:
        import_module("userbot.moduller." + module_name)
    except:
        LOGS.warn(f"{module_name} modülü yüklenirken bir hata oluştu.")

LOGS.info("Botunuz çalışıyor! Herhangi bir sohbete .alive yazarak Test edin."
          " Yardıma ihtiyacınız varsa, Destek grubumuza gelin t.me/FedaiUserBotSupport")
LOGS.info("Bot sürümünüz Fedai v1.4")

bot.run_until_disconnected()
