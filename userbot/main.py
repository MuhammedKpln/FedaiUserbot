
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

async def load_brain():
    if path.exists("learning-data-root.check"):
        remove("learning-data-root.check")
    URL = 'https://raw.githubusercontent.com/MuhammedKpln/databasescape/master/learning-data-root.check'
    with open('learning-data-root.check', 'wb') as load:
        load.write(get(URL).content)
    DB = connect("learning-data-root.check")
    CURSOR = DB.cursor()
    CURSOR.execute("""SELECT * FROM BRAIN1""")
    ALL_ROWS = CURSOR.fetchall()
    for i in ALL_ROWS:
        BRAIN_CHECKER.append(i[0])
    DB.close()

async def load_bl():
    if path.exists("blacklist.check"):
        remove("blacklist.check")
    URL = 'https://raw.githubusercontent.com/MuhammedKpln/databaseblacklist/master/blacklist.check'
    with open('blacklist.check', 'wb') as load:
        load.write(get(URL).content)    
    DB = connect("blacklist.check")
    CURSOR = DB.cursor()
    CURSOR.execute("SELECT * FROM RETARDS")
    ALL_ROWS = CURSOR.fetchall()
    for i in ALL_ROWS:
        BLACKLIST.append(i[0])
    DB.close()

runas(load_brain())
runas(load_bl())

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
