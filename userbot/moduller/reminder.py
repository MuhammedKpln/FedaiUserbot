import datetime
import re

from userbot import bot, CMD_HELP
from userbot.events import extract_args, register
from userbot.moduller.helpers import message

plugin_category = "user"
regexp = re.compile(r"(\d+)(h|g|sn|d|s)?")


@register(outgoing=True, pattern='^.hatırlat (\w*)')
async def _(e) -> None:
    time = e.pattern_match.group(1)
    text = e.text.partition(e.pattern_match.group(1))[2]


    if not time or not text:
        await e.edit('**Lütfen zaman ve bir hatirlatici mesaj belirtin.**')
        return
    await e.edit('**Fedai**` Peki sizin için bir hatırlatıcı oluşturuyorum...`')

    seconds = await string_to_secs(time)
    if seconds >= 13:
        try:
            await bot.send_message(
                entity='me',
                message=text,
                schedule=datetime.timedelta(seconds=seconds)
            )
            human_time = await _humanfriendly_seconds(seconds)
            print(human_time)
            message = f"**Fedai**: `Peki, sana {human_time} sonra hatırlatacağım.`"
            await e.edit(message)
        except Exception as e:
            print(e)
    else:
        await e.edit("`13 saniye altında hatılatıcı oluşturamam.`")


async def amount_to_secs(amount: tuple) -> int:
    """Resolves one unit to total seconds.
    Args:
        amount (``int``, ``str``):
            Tuple where str is the unit.
    Returns:
        ``int``:
            Total seconds of the unit on success.
    Example:
        >>> await amount_to_secs(("1", "m"))
        60
    """
    num, unit = amount

    num = int(num)
    if not unit:
        unit = 'sn'

    if unit == 'sn':
        return num
    elif unit == 'd':
        return num * 60
    elif unit == 's':
        return num * 60 * 60
    elif unit == 'g':
        return num * 60 * 60 * 24
    elif unit == 'h':
        return num * 60 * 60 * 24 * 7
    else:
        return 0


async def string_to_secs(string: str) -> int:
    """Converts a time string to total seconds.
    Args:
        string (``str``):
            String conatining the time.
    Returns:
        ``int``:
            Total seconds of all the units.
    Example:
        >>> await string_to_sec("6h20m")
        22800
    """
    values = regexp.findall(string)

    totalValues = len(values)
    print('totalvalues', totalValues)

    if totalValues == 1:
        print('values', values)
        return await amount_to_secs(values[0])
    else:
        total = 0
        for amount in values:
            total += await amount_to_secs(amount)
        print(total)
        return total


async def _humanfriendly_seconds(seconds: int or float) -> str:
    elapsed = datetime.timedelta(seconds=round(seconds)).__str__()
    splat = elapsed.split(', ')
    if len(splat) == 1:
        return await _human_friendly_timedelta(splat[0])
    friendly_units = await _human_friendly_timedelta(splat[1])
    return ', '.join([splat[0], friendly_units])


async def _human_friendly_timedelta(timedelta: str) -> str:
    splat = timedelta.split(':')
    nulls = ['0', "00"]
    h = splat[0]
    m = splat[1]
    s = splat[2]
    text = ''
    if h not in nulls:
        unit = "saat" if h == 1 else "saat"
        text += f"{h} {unit}"
    if m not in nulls:
        unit = "dakika" if m == 1 else "dakika"
        delimiter = ", " if len(text) > 1 else ''
        text += f"{delimiter}{m} {unit}"
    if s not in nulls:
        unit = "saniye" if s == 1 else "saniye"
        delimiter = " and " if len(text) > 1 else ''
        text += f"{delimiter}{s} {unit}"
    if len(text) == 0:
        text = "\u221E"
    return text


CMD_HELP.update({
    'hatirlat': message('Hatırlatıcı oluşturur. '
                        '\n\n Kullanım: .hatırlat 2s "hatırlatma mesajınız" '
                        '\n\nZamanlar:'
                        '\n\n 2s - 2 saat'
                        '\n\n 2sn - 2 saniye'
                        '\n\n 2d - 2 dakika'
                        '\n\n 2h - 2 hafta'
                        )
})
