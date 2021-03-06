
""" UserBot hazırlanışı. """

import os
import re

from sys import version_info
from logging import basicConfig, getLogger, INFO, DEBUG
from distutils.util import strtobool as sb
from math import ceil
from dotenv import load_dotenv
from requests import get
from telethon.sync import TelegramClient, custom, events
from telethon.tl.functions.channels import JoinChannelRequest
from telethon.sessions import StringSession
from telethon.utils import get_peer_id
load_dotenv("config.env")


# Bot günlükleri kurulumu:
CONSOLE_LOGGER_VERBOSE = sb(os.environ.get("CONSOLE_LOGGER_VERBOSE", "False"))

ASYNC_POOL = []

if CONSOLE_LOGGER_VERBOSE:
    basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        level=DEBUG,
    )
else:
    basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                level=INFO)
LOGS = getLogger(__name__)

if version_info[0] < 3 or version_info[1] < 8:
    LOGS.info("En az python 3.8 sürümüne sahip olmanız gerekir."
              "Birden fazla özellik buna bağlıdır. Bot kapatılıyor.")
    quit(1)

# Yapılandırmanın önceden kullanılan değişkeni kullanarak düzenlenip düzenlenmediğini kontrol edin.
# Temel olarak, yapılandırma dosyası için kontrol.
CONFIG_CHECK = os.environ.get(
    "___________LUTFEN_______BU_____SATIRI_____SILIN__________", None)

if CONFIG_CHECK:
    LOGS.info(
        "Lütfen ilk hashtag'de belirtilen satırı config.env dosyasından kaldırın"
    )
    quit(1)

# Telegram API KEY ve HASH
API_KEY = os.environ.get("API_KEY", None)
API_HASH = os.environ.get("API_HASH", None)

# UserBot Session String
STRING_SESSION = os.environ.get("STRING_SESSION", None)

# Kanal / Grup ID yapılandırmasını günlüğe kaydetme.
BOTLOG_CHATID = int(os.environ.get("BOTLOG_CHATID", None))

# UserBot günlükleme özelliği.
BOTLOG = sb(os.environ.get("BOTLOG", "False"))
LOGSPAMMER = sb(os.environ.get("LOGSPAMMER", "False"))

# Hey! Bu bir bot. Endişelenme ;)
PM_AUTO_BAN = sb(os.environ.get("PM_AUTO_BAN", "False"))

# Güncelleyici için Heroku hesap bilgileri.
HEROKU_APPNAME = os.environ.get("HEROKU_APPNAME", None)
HEROKU_APIKEY = os.environ.get("HEROKU_APIKEY", None)

# Güncelleyici için özel (fork) repo linki.
UPSTREAM_REPO_URL = os.environ.get(
    "UPSTREAM_REPO_URL",
    "https://github.com/MuhammedKpln/fedaiuserbot.git")

# Ayrıntılı konsol günlügü
CONSOLE_LOGGER_VERBOSE = sb(os.environ.get("CONSOLE_LOGGER_VERBOSE", "False"))

# SQL Veritabanı
DB_URI = os.environ.get("DATABASE_URL", None)

# remove.bg API key
REM_BG_API_KEY = os.environ.get("REM_BG_API_KEY", None)

# AUTO PP
AUTO_PP = os.environ.get("AUTO_PP", None)

# Lydia API
LYDIA_API_KEY = os.environ.get("LYDIA_API_KEY", None)

# Anti Spambot
ANTI_SPAMBOT = sb(os.environ.get("ANTI_SPAMBOT", "False"))
ANTI_SPAMBOT_SHOUT = sb(os.environ.get("ANTI_SPAMBOT_SHOUT", "False"))

# Youtube API key
YOUTUBE_API_KEY = os.environ.get("YOUTUBE_API_KEY", None)

# Saat & Tarih - Ülke ve Saat Dilimi
COUNTRY = str(os.environ.get("COUNTRY", ""))
TZ_NUMBER = int(os.environ.get("TZ_NUMBER", 1))

# Temiz Karşılama
CLEAN_WELCOME = sb(os.environ.get("CLEAN_WELCOME", "True"))

BIO_PREFIX = os.environ.get("BIO_PREFIX", None)
DEFAULT_BIO = os.environ.get("DEFAULT_BIO", None)

PROTECT_CHAT = os.environ.get('PROTECT_CHAT', '')

# Google Drive Modülü
TEMP_DOWNLOAD_DIRECTORY = os.environ.get("TMP_DOWNLOAD_DIRECTORY",
                                         "./downloads")

# Inline bot çalışması için
BOT_TOKEN = os.environ.get("BOT_TOKEN", None)
BOT_USERNAME = os.environ.get("BOT_USERNAME", None)

# Ayarlanabilir PM izin verilmedi mesajı
PM_UNAPPROVED = os.environ.get("PM_UNAPPROVED", None)

CMD_HELP = {}

# 'bot' değişkeni
if STRING_SESSION:
    # pylint: devre dışı=geçersiz ad
    bot = TelegramClient(StringSession(STRING_SESSION), API_KEY, API_HASH)
else:
    # pylint: devre dışı=geçersiz ad
    bot = TelegramClient("fedaibot", API_KEY, API_HASH)


async def check_botlog_chatid():
    if not BOTLOG_CHATID and LOGSPAMMER:
        LOGS.info(
            "HATA: LOGSPAMMER çalışması için BOTLOG_CHATID değişkenini ayarlamanız gerekir. "
            "Bot kapatılıyor..."
        )
        quit(1)

    elif not BOTLOG_CHATID and BOTLOG:
        LOGS.info(
            "Günlüğe kaydetme özelliğinin çalışması için BOTLOG_CHATID değişkenini ayarlamanız gerekir."
            "Bot Kapatılıyor..."
        )
        quit(1)

    elif not BOTLOG or not LOGSPAMMER:
        return

    entity = await bot.get_entity(BOTLOG_CHATID)
    if entity.default_banned_rights.send_messages:
        LOGS.info(
            "Hesabınızın BOTLOG_CHATID grubuna mesaj gönderme yetkisi yoktur. "
            "Grup ID'sini doğru yazıp yazmadığınızı kontrol edin.")
        quit(1)

with bot:
    me = bot.get_me()
    uid = me.id
    try:
        bot.loop.run_until_complete(check_botlog_chatid())
    except:
        LOGS.info(
            "HATA: Girilen BOTLOG_CHATID değişkeni geçerli değildir. "
            "Lütfen girdiğiniz değeri kontrol edin. "
            "Bot kapatılıyor.."
        )
        quit(1)
    try:
        bot(JoinChannelRequest("@FedaiUserBot"))
        bot(JoinChannelRequest("@FedaiUserBotSupport"))

        if not BOT_TOKEN:
            raise Exception()

        tgbot = TelegramClient(
            "TG_BOT_TOKEN",
            api_id=API_KEY,
            api_hash=API_HASH
        ).start(bot_token=BOT_TOKEN)

        dugmeler = CMD_HELP

        def paginate_help(page_number, loaded_modules, prefix):
            number_of_rows = 5
            number_of_cols = 2
            helpable_modules = []
            for p in loaded_modules:
                if not p.startswith("_"):
                    helpable_modules.append(p)
            helpable_modules = sorted(helpable_modules)
            modules = [custom.Button.inline(
                "{} {}".format("🔸", x),
                data="ub_modul_{}".format(x))
                for x in helpable_modules]
            pairs = list(zip(modules[::number_of_cols],
                             modules[1::number_of_cols]))
            if len(modules) % number_of_cols == 1:
                pairs.append((modules[-1],))
            max_num_pages = ceil(len(pairs) / number_of_rows)
            modulo_page = page_number % max_num_pages
            if len(pairs) > number_of_rows:
                pairs = pairs[modulo_page * number_of_rows:number_of_rows * (modulo_page + 1)] + \
                    [
                    (custom.Button.inline("⬅️Geri", data="{}_prev({})".format(prefix, modulo_page)),
                     custom.Button.inline("İleri➡️", data="{}_next({})".format(prefix, modulo_page)))
                ]
            return pairs

        @tgbot.on(events.NewMessage(pattern='/start'))
        async def handler(event):
            if not event.message.from_id == uid:
                await event.reply(f'`Merhaba ben` @FedaiUserBot`! Ben sahibime (`@{me.username}`) yardımcı olmak için varım, yaani sana yardımcı olamam :/ Kanala bak` @FedaiUserBot')
            else:
                await event.reply(f'`Senin için çalışıyorum :) Seni seviyorum. ❤️`')

        @tgbot.on(events.InlineQuery)  # pylint:disable=E0602
        async def inline_handler(event):
            builder = event.builder
            result = None
            query = event.text
            if event.query.user_id == uid and query.startswith("@FedaiUserBot"):
                rev_text = query[::-1]
                buttons = paginate_help(0, dugmeler, "helpme")
                result = builder.article(
                    f"Lütfen Sadece .yardım Komutu İle Kullanın",
                    text="{}\nYüklenen Modül Sayısı: {}".format(
                        "Merhaba! Ben @FedaiUserBot kullanıyorum!\n\nhttps://github.com/muhammedkpln/fedaiuserbot", len(dugmeler)),
                    buttons=buttons,
                    link_preview=False
                )
            elif query.startswith("tb_btn"):
                result = builder.article(
                    "© @FedaiUserBot",
                    text=f"@FedaiUserBot ile güçlendirildi",
                    buttons=[],
                    link_preview=True
                )
            else:
                result = builder.article(
                    "© @FedaiUserBot",
                    text="""@FedaiUserBot'u kullanmayı deneyin!
Hesabınızı bot'a çevirebilirsiniz ve bunları kullanabilirsiniz. Unutmayın, siz başkasının botunu yönetemezsiniz! Alttaki GitHub adresinden tüm kurulum detayları anlatılmıştır.""",
                    buttons=[
                        [custom.Button.url("Kanala Katıl", "https://t.me/FedaiUserBot"), custom.Button.url(
                            "Gruba Katıl", "https://t.me/FedaiUserBotSupport")],
                        [custom.Button.url(
                            "GitHub", "https://github.com/MuhammedKpln/fedaiuserbot")]
                    ],
                    link_preview=False
                )
            await event.answer([result] if result else None)

        @tgbot.on(events.callbackquery.CallbackQuery(  # pylint:disable=E0602
            data=re.compile(b"helpme_next\((.+?)\)")
        ))
        async def on_plug_in_callback_query_handler(event):
            if event.query.user_id == uid:  # pylint:disable=E0602
                current_page_number = int(
                    event.data_match.group(1).decode("UTF-8"))
                buttons = paginate_help(
                    current_page_number + 1, dugmeler, "helpme")
                # https://t.me/TelethonChat/115200
                await event.edit(buttons=buttons)
            else:
                reply_pop_up_alert = "Lütfen kendine bir @FedaiUserBot aç, benim mesajlarımı düzenlemeye çalışma!"
                await event.answer(reply_pop_up_alert, cache_time=0, alert=True)

        @tgbot.on(events.callbackquery.CallbackQuery(  # pylint:disable=E0602
            data=re.compile(b"helpme_prev\((.+?)\)")
        ))
        async def on_plug_in_callback_query_handler(event):
            if event.query.user_id == uid:  # pylint:disable=E0602
                current_page_number = int(
                    event.data_match.group(1).decode("UTF-8"))
                buttons = paginate_help(
                    current_page_number - 1,
                    dugmeler,  # pylint:disable=E0602
                    "helpme"
                )
                # https://t.me/TelethonChat/115200
                await event.edit(buttons=buttons)
            else:
                reply_pop_up_alert = "Lütfen kendine bir @FedaiUserBot aç, benim mesajlarımı düzenlemeye çalışma!"
                await event.answer(reply_pop_up_alert, cache_time=0, alert=True)

        @tgbot.on(events.callbackquery.CallbackQuery(  # pylint:disable=E0602
            data=re.compile(b"ub_modul_(.*)")
        ))
        async def on_plug_in_callback_query_handler(event):
            if event.query.user_id == uid:  # pylint:disable=E0602
                modul_name = event.data_match.group(1).decode("UTF-8")

                cmdhel = str(CMD_HELP[modul_name])
                if len(cmdhel) > 90:
                    help_string = str(CMD_HELP[modul_name])[
                        :90] + "\n\nDevamı için .fedai " + modul_name + " yazın."
                else:
                    help_string = str(CMD_HELP[modul_name])

                reply_pop_up_alert = help_string if help_string else \
                    "{} modülü için herhangi bir döküman yazılmamış.".format(
                        modul_name)
                await event.answer(reply_pop_up_alert, cache_time=0, alert=True)
            else:
                reply_pop_up_alert = "Lütfen kendine bir @FedaiUserBot aç, benim mesajlarımı düzenlemeye çalışma!"
                await event.answer(reply_pop_up_alert, cache_time=0, alert=True)
    except:
        LOGS.info(
            "Botunuzda inline desteği devre dışı bırakıldı. "
            "Etkinleştirmek için bir bot token tanımlayın ve botunuzda inline modunu etkinleştirin. "
            "Eğer bunun dışında bir sorun olduğunu düşünüyorsanız bize ulaşın."
        )

# Küresel Değişkenler
COUNT_MSG = 0
USERS = {}
BRAIN_CHECKER = []
BLACKLIST = []
COUNT_PM = {}
LASTMSG = {}
ENABLE_KILLME = True
ISAFK = False
AFKREASON = None

PLUGINID = os.environ.get("PLUGIN_CHANNEL_ID", None)
# Plugin İçin
if not PLUGINID:
    PLUGIN_CHANNEL_ID = "me"
else:
    PLUGIN_CHANNEL_ID = int(PLUGINID)
