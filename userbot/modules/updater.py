#

#
# FedaiUserBot is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import asyncio
import sys
from os import remove, execle, path, environ, execl

import heroku3
from git import Repo
from git.exc import GitCommandError, InvalidGitRepositoryError, NoSuchPathError

from userbot import CMD_HELP, HEROKU_APIKEY, HEROKU_APPNAME, UPSTREAM_REPO_URL, STRING_SESSION
from userbot.events import extract_args, register

requirements_path = path.join(
    path.dirname(path.dirname(path.dirname(__file__))), 'requirements.txt')


async def gen_chlog(repo, diff):
    ch_log = ''
    d_form = "%d/%m/%y"
    for c in repo.iter_commits(diff):
        ch_log += f'•[{c.committed_datetime.strftime(d_form)}]: {c.summary} <{c.author}>\n'
    return ch_log


async def update_requirements():
    reqs = str(requirements_path)
    try:
        process = await asyncio.create_subprocess_shell(
            ' '.join([sys.executable, "-m", "pip", "install", "-r", reqs]),
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE)
        await process.communicate()
        return process.returncode
    except Exception as e:
        return repr(e)


@register(outgoing=True, pattern=r"^\.update(?: |$)(.*)")
async def upstream(ups):
    await ups.edit(f"`FedaiBot için güncellemeler denetleniyor...`")
    conf = extract_args(ups)
    off_repo = UPSTREAM_REPO_URL
    force_update = False

    try:
        txt = f"`Güncelleme başarısız oldu!"
        txt += f"Bazı sorunlarla karşılaştık.`\n\n**LOG:**\n"
        repo = Repo()
    except NoSuchPathError as error:
        await ups.edit(f'{txt}\n`{error} klasörü bulunamadı.`')
        repo.__del__()
        return
    except GitCommandError as error:
        await ups.edit(f'{txt}\n`Git hatası! {error}`')
        repo.__del__()
        return
    except InvalidGitRepositoryError as error:
        if conf != "now":
            await ups.edit(
                f"`{error} klasörü bir git reposu gibi görünmüyor.\
            \nFakat bu sorunu .update now komutuyla botu zorla güncelleyerek çözebilirsin.`"
            )
            return
        repo = Repo.init()
        origin = repo.create_remote('upstream', off_repo)
        origin.fetch()
        force_update = True
        repo.create_head('master', origin.refs.fedai)
        repo.heads.fedai.set_tracking_branch(origin.refs.sql)
        repo.heads.fedai.checkout(True)

    ac_br = repo.active_branch.name
    if ac_br != 'fedai':
        await ups.edit(
            f'**[FedaiBot Güncelleyici]:**`Galiba botunun branch ismini değiştirdin. Kullandığın branch ismi: ({ac_br}). '
            f'Böyle olursa botunu güncelleyemem. Çünkü branch ismi uyuşmuyor..'
            f'Lütfen botunu FedaiBot resmi repodan kullan.`')
        repo.__del__()
        return

    try:
        repo.create_remote('upstream', off_repo)
    except BaseException:
        pass

    ups_rem = repo.remote('upstream')
    ups_rem.fetch(ac_br)

    changelog = await gen_chlog(repo, f'HEAD..upstream/{ac_br}')

    if not changelog and not force_update:
        await ups.edit(
            f'\n`Botun` **tamamen güncel!** `Branch:` **{ac_br}**\n')
        repo.__del__()
        return

    if conf != "now" and not force_update:
        changelog_str = f'**{ac_br} için yeni güncelleme mevcut!\n\nDeğişiklikler:**\n`{changelog}`'
        if len(changelog_str) > 4096:
            await ups.edit(f"`Değişiklik listesi çok büyük, dosya olarak görüntülemelisin.`")
            file = open("degisiklikler.txt", "w+")
            file.write(changelog_str)
            file.close()
            await ups.client.send_file(
                ups.chat_id,
                "degisiklikler.txt",
                reply_to=ups.id,
            )
            remove("degisiklikler.txt")
        else:
            await ups.edit(changelog_str)
        await ups.respond(f'`Güncellemeyi yapmak için \".update now\" komutunu kullan.`')
        return

    if force_update:
        await ups.edit(
            f'`Güncel FedaiBot kodu zorla eşitleniyor...`')
    else:
        await ups.edit(f'`Bot güncelleştiriliyor lütfen bekle...`')
    if HEROKU_APIKEY is not None:
        heroku = heroku3.from_key(HEROKU_APIKEY)
        heroku_app = None
        heroku_applications = heroku.apps()
        if not HEROKU_APPNAME:
            await ups.edit(
                f'`FedaiBot Güncelleyiciyi kullanabilmek için HEROKU_APPNAME değişkenini tanımlamalısın. Aksi halde güncelleyici çalışmaz.`'
            )
            repo.__del__()
            return
        for app in heroku_applications:
            if app.name == HEROKU_APPNAME:
                heroku_app = app
                break
        if heroku_app is None:
            await ups.edit(
                f'{txt}\n`Heroku değişkenleri yanlış veya eksik tanımlanmış.`'
            )
            repo.__del__()
            return
        await ups.edit(f'`FedaiBot Güncelleniyor..\
                        \nBu işlem 4-5 dakika sürebilir, lütfen sabırla bekle. Beklemene değer :)`'
                       )
        ups_rem.fetch(ac_br)
        repo.git.reset("--hard", "FETCH_HEAD")
        heroku_git_url = heroku_app.git_url.replace(
            "https://", "https://api:" + HEROKU_APIKEY + "@")
        if "heroku" in repo.remotes:
            remote = repo.remote("heroku")
            remote.set_url(heroku_git_url)
        else:
            remote = repo.create_remote("heroku", heroku_git_url)
        try:
            remote.push(refspec="HEAD:refs/heads/master", force=True)
        except GitCommandError as error:
            await ups.edit(f'{txt}\n`Karşılaşılan hatalar burada:\n{error}`')
            repo.__del__()
            return
        await ups.edit(f'`Güncelleme başarıyla tamamlandı!\n'
                       f'FedaiBot yeniden başlatılıyor sabırla beklediğin için teşekkür ederiz :)`')
    else:
        try:
            ups_rem.pull(ac_br)
        except GitCommandError:
            repo.git.reset("--hard", "FETCH_HEAD")
        await update_requirements()
        await ups.edit(f'`Güncelleme başarıyla tamamlandı!\n'
                       f'FedaiBot yeniden başlatılıyor sabırla beklediğin için teşekkür ederiz :)`')
        args = [sys.executable, "main.py"]
        execle(sys.executable, *args, environ)
        return


async def is_off_br(br):
    off_br = ['fedai']
    if br in off_br:
        return 1
    return

@register(outgoing=True, pattern="^.softupdate")
async def softupdate(ups):
    ".update komutu ile botunun güncel olup olmadığını denetleyebilirsin."
    await ups.edit("`Güncellemeler denetleniyor...`")
    conf = extract_args(ups)
    off_repo = UPSTREAM_REPO_URL

    try:
        txt = "``Güncelleme başarısız oldu! "
        txt += "Bazı sorunlarla karşılaştık.`\n\n**LOG:**\n"
        repo = Repo()
    except NoSuchPathError as error:
        await ups.edit(f'{txt}\n`{error} klasörü bulunamadı.`')
        return
    except InvalidGitRepositoryError as error:
        await ups.edit(f"`{error} klasörü bir git reposu gibi görünmüyor.\
            \nFakat bu sorunu .update now komutuyla botu zorla güncelleyerek çözebilirsin.`")
        return
    except GitCommandError as error:
        await ups.edit(f'{txt}\n`Git hatası! {error}`')
        return

    ac_br = repo.active_branch.name
    if not await is_off_br(ac_br):
        await ups.edit(
            f'**[Güncelleyici]:**` Galiba fedai botunu modifiye ettin ve kendi branşını kullanıyorsun: ({ac_br}). '
            'Bu durum güncelleyicinin kafasını karıştırıyor,'
            'Güncelleme nereden çekilecek?'
            'Lütfen fedai botunu resmi repodan kullan.`')
        return

    try:
        repo.create_remote('upstream', off_repo)
    except BaseException:
        pass

    ups_rem = repo.remote('upstream')
    ups_rem.fetch(ac_br)
    changelog = await gen_chlog(repo, f'HEAD..upstream/{ac_br}')

    if not changelog:
        await ups.edit(f'\n`Botun` **tamamen güncel!** `Branch:` **{ac_br}**\n')
        return

    if conf != "now":
        changelog_str = f'**{ac_br} için yeni güncelleme mevcut!\n\nDeğişiklikler:**\n`{changelog}`'
        if len(changelog_str) > 4096:
            await ups.edit("`Değişiklik listesi çok büyük, dosya olarak görüntülemelisin.`")
            file = open("degisiklikler.txt", "w+")
            file.write(changelog_str)
            file.close()
            await ups.client.send_file(
                ups.chat_id,
                "degisiklikler.txt",
                reply_to=ups.id,
            )
            remove("degisiklikler.txt")
        else:
            await ups.edit(changelog_str)
        await ups.respond('`Güncellemeyi yapmak için \".softupdate now\" komutunu kullan.`')
        return

    await ups.edit('`Bot güncelleştiriliyor...`')

    ups_rem.fetch(ac_br)
    repo.git.reset('--hard', 'fedai')

    if HEROKU_APIKEY != None:
        heroku = heroku3.from_key(HEROKU_APIKEY)
        if HEROKU_APPNAME != None:
            try:
                heroku_app = heroku.apps()[HEROKU_APPNAME]
            except KeyError:
                await ups.edit(
                    "```HATA: HEROKU_APPNAME değişkeni hatalı! Lütfen uygulama adınızın "
                    "HEROKU_APIKEY ile doğru olduğundan emin olun.```")
                return
        else:
            await ups.edit(
                "```HATA: HEROKU_APPNAME değişkeni ayarlanmadı! Lütfen "
                "Heroku uygulama adınızı değişkene girin.```")
            return

        await ups.edit(
            "`Heroku yapılandırması bulundu! Güncelleyici Fedai'i güncellemeye ve yeniden başlatmaya çalışacak."
            " Bu işlem otomatik olacaktır. İşlem bitince Fedai'in çalışıp çalışmadığını kontrol etmeyi deneyin.\n"
            "\".alive\" komutu ile deneyebilirsin.`\n"
            "**BOT YENIDEN BAŞLATILIYOR..**")
        if not STRING_SESSION:
            repo.git.add('sedenbot.session', force=True)
        if path.isfile('config.env'):
            repo.git.add('config.env', force=True)

        repo.git.checkout("fedai")

        repo.config_writer().set_value("user", "name",
                                       "FedaiBot Updater").release()
        repo.config_writer().set_value("user", "email",
                                       "<>").release()
        repo.git.pull()
        heroku_remote_url = heroku_app.git_url.replace(
            "https://", f"https://api:{HEROKU_APIKEY}@")

        remote = None
        if 'heroku' in repo.remotes:
            remote = repo.remote('heroku')
            remote.set_url(heroku_remote_url)
        else:
            remote = repo.create_remote('heroku', heroku_remote_url)

        try:
            remote.push(refspec="HEAD:refs/heads/fedai", force=True)
        except GitCommandError as e:
            await ups.edit(f'{txt}\n`Git hatası! {e}`')
            return
    else:
        repo.git.pull()

        await ups.edit(
            '`Güncelleme başarıyla tamamlandı!\n'
            'Fedai yeniden başlatılıyor... Lütfen biraz bekleyin, ardından '
            '".alive" komutunu kullanarak FedaiBotun çalışıp çalışmadığnıı kontrol edin.`')

        await ups.client.disconnect()
    execl(sys.executable, sys.executable, *sys.argv)


CMD_HELP.update({
    'softupdate':
        ".softupdate\
    \nKullanım: Botunuza siz kurduktan sonra herhangi bir güncelleme gelip gelmediğini kontrol eder.\
    \n\n.softupdate now\
    \nKullanım: Botunuzu günceller."
})

CMD_HELP.update({
    'update':
        ".update\
    \nKullanım: Botunuza siz kurduktan sonra herhangi bir güncelleme gelip gelmediğini kontrol eder.\
    \n\n.update now\
    \nKullanım: Botunuzu günceller."
})
