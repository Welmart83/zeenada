import asyncio
import os

import heroku3
from telethon.errors import FloodWaitError

from userbot import CMD_HANDLER as cmd
from userbot import CMD_HELP, DEVS, HEROKU_API_KEY, HEROKU_APP_NAME, GCAST_BLACKLIST
from userbot.utils import edit_delete, edit_or_reply, zelda_cmd

Heroku = heroku3.from_key(HEROKU_API_KEY)
heroku_api = "https://api.heroku.com"
blchat = os.environ.get("GCAST_BLACKLIST") or ""

@zelda_cmd(pattern="blchat$")
async def sudo(event):
    blchat = "True" if GCAST_BLACKLIST else "False"
    blc = blchat
    if sudo == "True":
        await edit_or_reply(
            event,
            f"🚫 **GCast Blacklist :** `Enabled`\n\n📜 ** Blacklist Group :**\n• `{blc}`\n\nKetik `.addbl` di grup untuk menambahkan ke Blacklist.",
        )
    else:
        await edit_delete(event, "🚫 **GCast Blacklis :** `Disabled`")
        

@zelda_cmd(pattern="addbl(?:\s|$)([\s\S]*)")
async def add(event):
    xxnx = await edit_or_reply(event, "`Processing...`")
    var = "GCAST_BLACKLIST"
    gc = await event.get_chat_id()
    if HEROKU_APP_NAME is not None:
        app = Heroku.app(HEROKU_APP_NAME)
    else:
        await edit_delete(
            xxnx,
            "**Silahkan Tambahkan Var** `HEROKU_APP_NAME` **untuk menambahkan blacklist**",
        )
        return
    heroku_Config = app.config()
    if event is None:
        return
    blchat = f"{GCAST_BLACKLIST} {gc}"
    nenwbl = blchat.replace("{", "")
    nenwbl = nenwbl.replace("}", "")
    await xxnx.edit(
        f"**Berhasil Menambahkan** `{gc}` **ke GCast Blacklist.**\n\nSedang MeRestart Heroku untuk Menerapkan Perubahan."
    )
    heroku_Config[var] = nenwbl
    
    
@zelda_cmd(pattern="delbl(?:\s|$)([\s\S]*)")
async def _(event):
	xxx = await edit_or_reply(event, "`Processing...`")
	if HEROKU_APP_NAME is not None:
        # app = Heroku.app(HEROKU_APP_NAME)
    else:
        await edit_delete(
            xxx,
            "**Silahkan Tambahkan Var** `HEROKU_APP_NAME` **untuk menghapus blacklist**",
        )
        return
    heroku_Config = app.config()
    if event is None:
        return
    gc = await event.get_chat_id()
    gett = str(gc)
    if gett in blchat:
        nenwbl = blchat.replace(gett, "")
        await xxx.edit(
            f"**Berhasil Menghapus** `{gc}` **dari Gcast Blacklist.**\n\nSedang MeRestart Heroku untuk Menerapkan Perubahan."
        )
        var = "GCAST_BLACKLIST"
        heroku_Config[var] = nenwbl
    else:
        await edit_delete(
            xxx, "**Group ini tidak ada dalam Daftar Blacklist anda.**", 45
        )


@zelda_cmd(pattern="gcast(?: |$)(.*)")
async def gcast(event):
    xx = event.pattern_match.group(1)
    if xx:
        msg = xx
    elif event.is_reply:
        msg = await event.get_reply_message()
    else:
        return await edit_delete(event, "**Berikan Sebuah Pesan atau Reply**")
    kk = await edit_or_reply(event, "`Mengirim Pesan Siaran...`")
    er = 0
    done = 0
    async for x in event.client.iter_dialogs():
        if x.is_group:
            chat = x.id
            try:
                if chat not in GCAST_BLACKLIST:
                    await event.client.send_message(chat, msg)
                    done += 1
            except FloodWaitError as e:
                if chat not in GCAST_BLACKLIST:
                    await asyncio.sleep(e.x)
                    await event.client.send_message(chat, msg)
                    done += 1
            except BaseException:
                er += 1
    await kk.edit(
        f"✅ Berhasil Terkirim Ke {done} Grup\n⛔ Gagal Mengirim Ke {er} Grup"
    )


@zelda_cmd(pattern="gucast(?: |$)(.*)")
async def gucast(event):
    xx = event.pattern_match.group(1)
    if xx:
        msg = xx
    elif event.is_reply:
        msg = await event.get_reply_message()
    else:
        return await edit_delete(event, "**Berikan Sebuah Pesan atau Reply**")
    kk = await edit_or_reply(event, "`Mengirim Pesan Siaran...`")
    er = 0
    done = 0
    async for x in event.client.iter_dialogs():
        if x.is_user and not x.entity.bot:
            chat = x.id
            try:
                if chat not in DEVS:
                    await event.client.send_message(chat, msg)
                    done += 1
            except FloodWaitError as e:
                if chat not in DEVS:
                    await asyncio.sleep(e.x)
                    await event.client.send_message(chat, msg)
                    done += 1
            except BaseException:
                er += 1
    await kk.edit(
        f"✅ Berhasil Terkirim Ke {done} Obrolan\n⛔ Gagal Mengirim Ke {er} Obrolan"
    )


CMD_HELP.update(
    {
        "gcast": f"**Plugin : **`gcast`\
        \n\n  •  **Syntax :** `{cmd}gcast` <text/reply media>\
        \n  •  **Function : **Mengirim Global Broadcast pesan ke Seluruh Grup yang kamu masuk. (Bisa Mengirim Media/Sticker)\
    "
    }
)


CMD_HELP.update(
    {
        "gucast": f"**Plugin : **`gucast`\
        \n\n  •  **Syntax :** `{cmd}gucast` <text/reply media>\
        \n  •  **Function : **Mengirim Global Broadcast pesan ke Seluruh Private Massage / PC yang masuk. (Bisa Mengirim Media/Sticker)\
    "
    }
)

CMD_HELP.update(
    {
        "setgcast": f"**Plugin : **`gcast`\
        \n\n  •  **Syntax :** `{cmd}blchat`\
        \n  •  **Function : **Untuk Mengecek informasi Gcast Blacklist.\
        \n\n  •  **Syntax :** `{cmd}addbl`\
        \n  •  **Function : **Untuk Menambahkan grup tersebut ke Gcast Blaclist.\
        \n\n  •  **Syntax :** `{cmd}delbl`\
        \n  •  **Function : **Untuk Menghapus grup tersebut dari Gcast Blaclist.\
        \n  •  **Note : **Ketik perintah** `{cmd}addbl` **dan** `{cmd}delbl` **di grup yang kamu Blacklist.\
    "
    }
)