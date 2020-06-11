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
# By @muhammedkpln
#

import os
import tempfile
from hashlib import md5
from random import randint

import requests
from telethon.errors import PhotoCropSizeSmallError
from telethon.events import NewMessage
from telethon.tl.functions.photos import UploadProfilePhotoRequest

from userbot import bot, LOGS, CMD_HELP
from userbot.events import register
from userbot.moduller.helpers import message

TEMP_DIR = tempfile.gettempdir()
REDDIT_URL = 'https://www.reddit.com/r/wallpaper/top.json'
headers = {
    'User-Agent': 'Mozilla/5.0 (Linux x86_64; rv:77.0) Gecko/20100101 Firefox/77.0'
}


@register(outgoing=True, pattern="^.yenipp$")
async def _(e: NewMessage.Event) -> None:
    api = requests.get(REDDIT_URL, headers=headers)
    json = api.json()
    post = json['data']['children'][randint(0, 24)]
    try:
        await e.edit(message('Peki, sizin için yeni bir profil fotoğrafı arıyorum..'))
        image = post['data'].get('url')
        file_name = md5(str(randint(0, 9000)).encode()).hexdigest() + '.png'
        file_path = os.path.join(TEMP_DIR, file_name)
        downloaded_image_request = requests.get(image, headers=headers)

        with open(file_path, 'wb') as f:
            f.write(downloaded_image_request.content)
            f.close()

        try:
            await e.edit(message('Yeni profil fotoğrafınız ayarlanıyor...'))
            uploaded_image = await bot.upload_file(file_path)
            await bot(UploadProfilePhotoRequest(uploaded_image))
            os.remove(file_path)
            await e.edit(message('Profil fotoğrafınız başarılı bir şekilde değiştirildi!'))
        except PhotoCropSizeSmallError as e:
            _(e)
            LOGS.exception(e)

    except Exception as e:
        LOGS.exception(e)


CMD_HELP.update(message('.yenipp \n\n Yeni bir profil fotoğrafı ayarlar.'))
