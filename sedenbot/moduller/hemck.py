from telethon import events
import asyncio
from events import extract_args, sedenify



@sedenify(outgoing=True, pattern="^.hack")
async def port_hack(event):
    if event.fwd_from:
        return
    message = extract_args(afk_e)

    animation_interval = 3
    animation_ttl = range(0, 11)
    #input_str = event.pattern_match.group(1)
    #if input_str == "hack":
    await event.edit("Hacking..")
    animation_chars = [
            "`Connecting To Hacked Private Server...`",
            "`Target Selected.`",
            "`Hacking... 0%\n▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ `",
            "`Hacking... 4%\n█▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ `",
            "`Hacking... 8%\n██▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ `",    
            "`Hacking... 20%\n█████▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ `",
            "`Hacking... 36%\n█████████▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ `",
            "`Hacking... 52%\n█████████████▒▒▒▒▒▒▒▒▒▒▒▒ `",
            "`Hacking... 84%\n█████████████████████▒▒▒▒ `",
            "`Hacking... 100%\n█████████HACKED███████████ `",
            f"`Targeted Account Hacked by @muhammedkaplan...\n\n {message} `"
        ]

    for i in animation_ttl:
        await asyncio.sleep(animation_interval)
        await event.edit(animation_chars[i % 11])