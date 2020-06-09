
import aiohttp

from userbot import CMD_HELP
from userbot.events import extract_args, register

@register(pattern=r"^.git", outgoing=True)
async def github(event):
    args = extract_args(event)
    URL = f"https://api.github.com/users/{args}"
    chat = await event.get_chat()
    async with aiohttp.ClientSession() as session:
        async with session.get(URL) as request:
            if request.status == 404:
                await event.reply(f"`{args} bulunamadı`")
                return

            result = await request.json()

            url = result.get("html_url", None)
            name = result.get("name", None)
            company = result.get("company", None)
            bio = result.get("bio", None)
            created_at = result.get("created_at", "Not Found")

            REPLY = f"`{args} adlı kullanıcının GitHub bilgileri:`\
            \nİsim: `{name}`\
            \nBiyografi: `{bio}`\
            \nURL: {url}\
            \nŞirket: `{company}`\
            \nHesap oluşturulma tarihi: `{created_at}`"

            if not result.get("repos_url", None):
                await event.edit(REPLY)
                return
            async with session.get(result.get("repos_url", None)) as request:
                result = request.json
                if request.status == 404:
                    await event.edit(REPLY)
                    return

                result = await request.json()

                REPLY += "\nRepolar:\n"

                for nr in range(len(result)):
                    REPLY += f"[{result[nr].get('name', None)}]({result[nr].get('html_url', None)})\n"

                await event.edit(REPLY)

CMD_HELP.update({
    "git": 
    ".git \
    \nKullanım: Hedeflenen kişinin GitHub bilgilerini gösterir.\n"
})
