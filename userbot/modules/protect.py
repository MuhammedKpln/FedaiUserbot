from telethon.tl.functions.channels import EditBannedRequest

from userbot import PROTECT_CHAT, bot, CMD_HELP, HEROKU_APIKEY, HEROKU_APPNAME
from userbot.events import register, extract_args
from userbot.modules.admin import BANNED_RIGHTS
from userbot.modules.helpers import message

WARN = 0
WARN_AUTHOR = None
WARNING_IS_ON = True
PROTECT = False
PROTECT_CHATS = PROTECT_CHAT.split(',')

@register(incoming=True, pattern="^")
async def _(e):
    global WARN
    global WARN_AUTHOR
    global PROTECT_CHATS

    if PROTECT:
        if str(e.chat_id) in PROTECT_CHATS:

            msg = e.message.message

            # if e.user_joined and e.message.fwd_from:
            #     return await warn_user(e)

            # Remove messages that has higher than 200 characters
            if len(msg) > 200:
                return await warn_user(e)

            # Remove message that contains hashtag
            if '#' in msg:
                return await warn_user(e)


@register(outgoing=True, pattern='^.protect (.?)')
async def _(e):
    global PROTECT

    arg = extract_args(e)

    if arg == 'on' and not PROTECT:
        await e.edit(message('Korumalar acildi!'))
        PROTECT = True
        return
    else:
        await e.edit(message('Korumalar zaten aktif! Kapatmak icin .protect off yazin.'))
        return

    if arg == 'off' and PROTECT:
        await e.edit(message('Korumalar De-aktif edildi!'))
        PROTECT = False
        return
    else:
        await e.edit(message('Korumalar zaten de-aktif! Yeniden baslatmak icin .protect on yazin.'))
        return


@register(outgoing=True, pattern='^.acil$')
async def _(e):
    global PROTECT
    global WARNING_IS_ON

    PROTECT = True
    WARNING_IS_ON = False

    await e.edit(message('Acil modu acildi! keyfinize bakin.'))


@register(outgoing=True, pattern='^.protectekle$')
async def _(e):
    import heroku3
    global  PROTECT_CHATS


    if not e.chat_id in PROTECT_CHATS:
        PROTECT_CHATS.append(e.chat_id)
        chat = await e.client.get_entity(e.chat_id)

        heroku = heroku3.from_key(HEROKU_APIKEY)
        heroku_app = heroku.apps()[HEROKU_APPNAME]

        heroku.update_appconfig(heroku_app.id, {
            'PROTECT_CHAT': ','.join(PROTECT_CHATS)
        })

        await e.edit(message(f'{chat.title} koruma altına alındı!'))

        return
    else:
        await e.edit(message(f'{e.chat_id} id\'li zaten koruma altında!'))


@register(outgoing=True, pattern='^.protectsil')
async def _(e):
    import heroku3
    global  PROTECT_CHATS


    if e.chat_id in PROTECT_CHATS:
        PROTECT_CHATS.remove(e.chat_id)
        chat = await e.client.get_entity(e.chat_id)

        heroku = heroku3.from_key(HEROKU_APIKEY)
        heroku_app = heroku.apps()[HEROKU_APPNAME]

        heroku.update_appconfig(heroku_app.id, {
            'PROTECT_CHAT': ','.join(PROTECT_CHATS)
        })

        await e.edit(message(f'{chat.title} için koruma devre dışı bırakıldı!'))

        return
    else:
        await e.edit(message(f'Bu sohbet için herhangi bir koruma ayarı bulunmamakta!'))


async def warn_user(e):
    global WARN
    global WARN_AUTHOR
    global WARNING_IS_ON

    message_id = e.message.id
    message_author = await e.client.get_entity(e.message.from_id)

    if message_author.username:
        if message_author.username.lower().endswith('bot'):
            return True

    if WARNING_IS_ON:
        WARN = WARN + 1

    if WARN_AUTHOR == message_author.id and WARN == 3 and WARNING_IS_ON:
        await bot(EditBannedRequest(
            channel=e.chat_id,
            user_id=message_author.id,
            banned_rights=BANNED_RIGHTS
        ))

        WARN = 0

        await e.reply(message(f'{message_author.first_name} Banlandın! '))
    elif not WARNING_IS_ON:
        await bot(EditBannedRequest(
            channel=e.chat_id,
            user_id=message_author.id,
            banned_rights=BANNED_RIGHTS
        ))

        await e.reply(message(f'{message_author.first_name} Banlandın! '))

    WARN = 0

    WARN_AUTHOR = message_author.id
    await e.reply(
        message(f'Lütfen flood atmayın, sadece 3 hakkınız var banlanırsınız! \n\n **Giden Hak**: {WARN}'))

    await e.client.delete_messages(e.chat_id, [message_id])


CMD_HELP.update({
    'protect': message(
        'Gruplarınızı floodlardan veya benzeri tehlikelerden korur, aktif edebilmeniz için env ayarlarından'
        ' grup id\'sini eklemeniz gerekmekte. Ardıdan \'.protect on|off diyerek kapatabilirsiniz.\' '),
    '.acil': message('Olağan üstü durumları başlatır, uyarı vermek yerine direk banlar.')
})
