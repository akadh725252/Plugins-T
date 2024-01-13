from telethon import Button
from telethon.tl import functions
from telethon.tl.types import ChatAdminRights

from HellConfig import Config
from TelethonHell import LOGS
from TelethonHell.helpers.int_str import make_int
from TelethonHell.DB.gvar_sql import addgvar, gvarstat
from TelethonHell.version import __telever__


# Creates the logger group on first deploy and adds the helper bot
async def logger_id(client):
    desc = "A Bᴏᴛ Lᴏɢɢᴇʀ Gʀᴏᴜᴘ Fᴏʀ 𝙒𝙖𝙧𝙐𝙨𝙚𝙧𝘽𝙤𝙩 🇮🇳. Dᴏ Nᴏᴛ Lᴇᴀᴠᴇ Tʜɪs Gʀᴏᴜᴘ!!""
    try:
        grp = await client(
            functions.channels.CreateChannelRequest(
                title="𝙒𝙖𝙧𝙐𝙨𝙚𝙧𝘽𝙤𝙩 𝙇𝙤𝙜𝙜𝙚𝙧 🇮🇳", about=desc, megagroup=True
            )
        )
        grp_id = grp.chats[0].id
    except Exception as e:
        LOGS.error(f"{str(e)}")
        return
    
    if not str(grp_id).startswith("-100"):
        grp_id = int("-100" + str(grp_id))
    
    try:
        new_rights = ChatAdminRights(
            add_admins=True,
            invite_users=True,
            change_info=True,
            ban_users=True,
            delete_messages=True,
            pin_messages=True,
            manage_call=True,
        )
        grp = await client(functions.messages.ExportChatInviteRequest(peer=grp_id))
        await client(
            functions.channels.InviteToChannelRequest(
                channel=grp_id, users=[Config.BOT_USERNAME]
            )
        )
        await client(
            functions.channels.EditAdminRequest(
                grp_id, Config.BOT_USERNAME, new_rights, "helper"
            )
        )
    except Exception as e:
        LOGS.error(f"{str(e)}")

    return grp_id


# Updates sudo cache on every restart
async def update_sudo():
    Sudo = Config.SUDO_USERS
    sudo = gvarstat("SUDO_USERS")
    if sudo:
        int_list = await make_int(gvarstat("SUDO_USERS"))
        for x in int_list:
            Sudo.append(x)


# Checks for logger group.
async def logger_check(bot):
    if Config.LOGGER_ID is None:
        if gvarstat("LOGGER_ID") is None:
            grp_id = await logger_id(bot)
            addgvar("LOGGER_ID", grp_id)
            Config.LOGGER_ID = grp_id
        Config.LOGGER_ID = int(gvarstat("LOGGER_ID"))


# Sends the startup message to logger group
async def start_msg(client, pic, version, total):
    is_sudo = "true" if Config.SUDO_USERS else "false"
    text = f"""
#START

<b><i>Vᴇʀsɪᴏɴ :</b></i> <code>{version}</code>
<b><i>Cʟɪᴇɴᴛs :</b></i> <code>{str(total)}</code>
<b><i>Sᴜᴅᴏ :</b></i> <code>{is_sudo}</code>
<b><i>Lɪʙʀᴀʀʏ :</b></i> <code>Tᴇʟᴇᴛʜᴏɴ - {__telever__}</code>

<b><i>»» <u><a href='https://t.me/waruserbot'>𝙒𝙖𝙧𝙐𝙨𝙚𝙧𝘽𝙤𝙩 🇮🇳</a></u> ««</i></b>
"""
    await client.send_file(
        Config.LOGGER_ID,
        pic,
        caption=text,
        parse_mode="HTML",
        buttons=[[Button.url("𝙒𝙖𝙧𝙐𝙨𝙚𝙧𝘽𝙤𝙩 🇮🇳", "https://t.me/waruserbot")]],
    )


# Joins the hellbot chat and channel from all clients
async def join_it(client):
    if client:
        try:
            await client(functions.channels.JoinChannelRequest("@waruserbot"))
            await client(functions.messages.ImportChatInviteRequest("6nBWPUON43AwYTk1"))
        except BaseException:
            pass
