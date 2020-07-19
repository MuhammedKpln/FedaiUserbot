from telethon.tl.functions.channels import EditBannedRequest

from userbot import PROTECT_CHAT, bot, CMD_HELP
from userbot.events import register, extract_args
from userbot.modules.admin import BANNED_RIGHTS
from userbot.modules.helpers import message

WARN = 0
WARN_AUTHOR = None
WARNING_IS_ON = True
PROTECT = False


@register(incoming=True, pattern="^")
async def _(e):
    global WARN
    global WARN_AUTHOR

    PROTECT_CHATS = PROTECT_CHAT.split(',')

    print(PROTECT)

    if PROTECT:
        if str(e.chat_id) in PROTECT_CHATS:

            msg = e.message.message
            print(e.message)
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
