from userbot import CMD_HELP, BOT_USERNAME
from userbot.events import register

@register(outgoing=True, pattern="^.yardım")
async def yardim(event):
    tgbotusername = BOT_USERNAME
    if tgbotusername and len(tgbotusername) > 4:
        try:
            results = await event.client.inline_query(
                tgbotusername,
                "@FedaiUserBot"
            )
            await results[0].click(
                event.chat_id,
                reply_to=event.reply_to_msg_id,
                hide_via=True
            )
            await event.delete()
        except:
            await event.edit("`Botunda inline modunu açman gerekiyor.`")
    else:
        await event.edit("`Bot çalışmıyor! Lütfen Bot Tokeni ve Kullanıcı adını doğru ayarlayın. Modül durduruldu.`")
