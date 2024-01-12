import html
import random
from math import ceil
from re import compile
import httpx

from telethon import Button, custom, functions
from telethon.events import InlineQuery, callbackquery
from telethon.sync import custom
from telethon.tl.functions.users import GetFullUserRequest

from TelethonHell.DB.gvar_sql import gvarstat

from . import *

hell_row = Config.BUTTONS_IN_HELP
hell_emoji = Config.EMOJI_IN_HELP

PM_WARNS = {}
PREV_REPLY_MESSAGE = {}

mybot = Config.BOT_USERNAME
if mybot.startswith("@"):
    botname = mybot
else:
    botname = f"@{mybot}"

LOG_GP = Config.LOGGER_ID

alive_txt = """\
🌟 <b>Bot Status</b> 🌟

🤖 <b>Telethon Version:</b>  <code>{}</code>
🤖 <b>Waruserbot Version:</b>  <code>{}</code>
⏳ <b>Uptime:</b>  <code>{}</code>
🚨 <b>Abuse Status:</b>  <code>{}</code>
👑 <b>Sudo Access:</b>  <code>{}</code>
"""

@tgbot.on(events.NewMessage(pattern='/start'))
async def start(event):
    img_path = 'https://graph.org/file/c83443bf2a2eff3fdadb1.jpg'

    url_button1 = Button.url("Repo", "https://github.com/MeAbhish3k/waruserbot")
    url_button2 = Button.url("Support", "https://t.me/+a7Jui-Qd3vtkYTVl")
    url_button3 = Button.url("Update", "https://t.me/waruserbot")

    await event.respond(
        file=img_path,
        buttons=[
            [url_button1],
            [url_button2, url_button3]
        ]
    )

@tgbot.on(events.NewMessage(pattern='/repo'))
async def repo(event):
    repo_url = "https://api.github.com/repos/MeAbhish3k/waruserbot"
    
    async with httpx.AsyncClient() as client:
        response = await client.get(repo_url)

        if response.status_code == 200:
            repo_data = response.json()
            repo_info = (
                f"**Repository Info:**\n"
                f"[📑 𝙍𝙚𝙥𝙤](https://github.com/MeAbhish3k/waruserbot)\n"
                f"🌟 Stars: {repo_data['stargazers_count']}\n"
                f"🍴 Forks: {repo_data['forks_count']}\n"
                f"🔄 Last Update: {repo_data['updated_at']}\n"
                f"©️ @waruserbot ™"
            )
            await event.reply(repo_info, parse_mode='markdown')
        else:
            await event.reply("Failed to retrieve repository information.")

def button(page, modules):
    Row = hell_row

    modules = sorted([modul for modul in modules if not modul.startswith("_")])
    pairs = list(map(list, zip(modules[::2], modules[1::2])))
    if len(modules) % 2 == 1:
        pairs.append([modules[-1]])
    max_pages = ceil(len(pairs) / Row)
    pairs = [pairs[i : i + Row] for i in range(0, len(pairs), Row)]
    buttons = []
    for pairs in pairs[page]:
        buttons.append(
            [
                custom.Button.inline(
                    f"{hell_emoji} " + pair + f" {hell_emoji}",
                    data=f"Information[{page}]({pair})",
                )
                for pair in pairs
            ]
        )

    buttons.append(
        [
            custom.Button.inline(
                f"◀️ Back {hell_emoji}",
                data=f"page({(max_pages - 1) if page == 0 else (page - 1)})",
            ),
            custom.Button.inline(f"• ❌ •", data="close"),
            custom.Button.inline(
                f"{hell_emoji} Next ▶️",
                data=f"page({0 if page == (max_pages - 1) else page + 1})",
            ),
        ]
    )
    return [max_pages, buttons]

    modules = CMD_HELP


if Config.BOT_USERNAME is not None and tgbot is not None:

    @tgbot.on(InlineQuery)
    async def inline_handler(event):
        cids = await client_id(event, event.query.user_id)
        ForGo10God, HELL_USER, hell_mention = cids[0], cids[1], cids[2]
        builder = event.builder
        result = None
        query = event.text
        auth = await clients_list()
        if event.query.user_id in auth and query == "hellbot_help":
            rev_text = query[::-1]
            veriler = button(0, sorted(CMD_HELP))
            apn = []
            for x in CMD_LIST.values():
                for y in x:
                    apn.append(y)
            a = gvarstat("HELP_PIC")
            if a:
                help_pic = a.split(" ")[0]
            else:
                help_pic = "https://graph.org/file/9f1b4d4c70ec35c8b0594.jpg"
            help_msg = f"🔰 **{hell_mention}**\n\n📜 __No.of Plugins__ : `{len(CMD_HELP)}` \n🗂️ __Commands__ : `{len(apn)}`\n🗒️ __Page__ : 1/{veriler[0]}"
            if help_pic == "DISABLE":
                result = builder.article(
                    f"Hey! Only use {hl}help please",
                    text=help_msg,
                    buttons=veriler[1],
                    link_preview=False,
                )
            elif help_pic.endswith((".jpg", ".png")):
                result = builder.photo(
                    help_pic,
                    text=help_msg,
                    buttons=veriler[1],
                    link_preview=False,
                )
            elif help_pic:
                result = builder.document(
                    help_pic,
                    text=help_msg,
                    title="HellBot Alive",
                    buttons=veriler[1],
                    link_preview=False,
                )
        elif event.query.user_id in auth and query == "alive":
            uptime = await get_time((time.time() - StartTime))
            alive_msg = gvarstat("ALIVE_MSG") or "»»» <b>WarUserBot is Online</b> «««"
            alive_name = gvarstat("ALIVE_NAME") or HELL_USER
            he_ll = alive_txt.format(
                alive_msg, tel_ver, hell_ver, uptime, abuse_m, is_sudo
            )
            alv_btn = [
                [Button.url(f"{alive_name}", f"tg://openmessage?user_id={ForGo10God}")],
                [
                    Button.url("My Channel", f"https://t.me/{my_channel}"),
                    Button.url("My Group", f"https://t.me/{my_group}"),
                ],
            ]
            a = gvarstat("ALIVE_PIC")
            pic_list = []
            if a:
                b = a.split(" ")
                if len(b) >= 1:
                    for c in b:
                        pic_list.append(c)
                PIC = random.choice(pic_list)
            else:
                PIC = "https://graph.org/file/b059e4e2e82350f6e15f5.jpg"
            if PIC and PIC.endswith((".jpg", ".png")):
                result = builder.photo(
                    PIC,
                    text=he_ll,
                    buttons=alv_btn,
                    link_preview=False,
                    parse_mode="HTML",
                )
            elif PIC:
                result = builder.document(
                    PIC,
                    text=he_ll,
                    title="WarBot Alive",
                    buttons=alv_btn,
                    link_preview=False,
                    parse_mode="HTML",
                )
            else:
                result = builder.article(
                    text=he_ll,
                    title="WarBot Alive",
                    buttons=alv_btn,
                    link_preview=False,
                    parse_mode="HTML",
                )

        elif event.query.user_id in auth and query == "pm_warn":
            CSTM_PMP = gvarstat("CUSTOM_PMPERMIT") or None
            HELL_FIRST = f"🔥 𝙒𝙖𝙧𝙐𝙨𝙚𝙧𝘽𝙤𝙩 𝙋𝙈 𝙎𝙚𝙘𝙪𝙧𝙞𝙩𝙮 🔥\n\nHello!! This is an automated message on behalf of {hell_mention}."
            if CSTM_PMP:
                HELL_FIRST += f"\n\n{CSTM_PMP}"
            a = gvarstat("PMPERMIT_PIC")
            pic_list = []
            if a and a == "DISABLE":
                PIC = None
            elif a:
                b = a.split(" ")
                if len(b) >= 1:
                    for c in b:
                        pic_list.append(c)
                PIC = random.choice(pic_list)
            else:
                PIC = "https://graph.org/file/b059e4e2e82350f6e15f5.jpg"
            if PIC and PIC.endswith((".jpg", ".png")):
                result = builder.photo(
                    file=PIC,
                    text=HELL_FIRST,
                    buttons=[
                        [custom.Button.inline("📝 Request Approval", data="req")],
                        [custom.Button.inline("🚫 Block", data="heheboi")],
                        [custom.Button.inline("❓ Curious", data="pmclick")],
                    ],
                    link_preview=False,
                )
            elif PIC:
                result = builder.document(
                    file=PIC,
                    text=HELL_FIRST,
                    title="Warbot PM Permit",
                    buttons=[
                        [custom.Button.inline("📝 Request Approval", data="req")],
                        [custom.Button.inline("🚫 Block", data="heheboi")],
                        [custom.Button.inline("❓ Curious", data="pmclick")],
                    ],
                    link_preview=False,
                )
            else:
                result = builder.article(
                    text=HELL_FIRST,
                    title="Warbot PM Permit",
                    buttons=[
                        [custom.Button.inline("📝 Request Approval", data="req")],
                        [custom.Button.inline("🚫 Block", data="heheboi")],
                        [custom.Button.inline("❓ Curious", data="pmclick")],
                    ],
                    link_preview=False,
                )

        elif event.query.user_id in auth and query == "repo":
            result = builder.article(
                title="Repository",
                text=f"**⚡ LEGENDRY AF WARUSERBOT ⚡**",
                buttons=[
                    [Button.url("📑 Repo 📑", "https://github.com/MeAbhish3k/waruserbot")],
                    [Button.url("WarBot Network", "https://t.me/wrrlegend")],
                ],
            )

        else:
            result = builder.article(
                "@Waruserbot",
                text="""**Hey! This is [WARUSERBOT](https://t.me/waruserbot) \nYou can know more about me from the links given below 👇**""",
                buttons=[
                    [
                        custom.Button.url("🔥 CHANNEL 🔥", "https://t.me/waruserbot"),
                        custom.Button.url("⚡ GROUP ⚡", "https://t.me/waruerbotsupport"),
                    ],
                    [
                        custom.Button.url(
                            "✨ REPO ✨", "https://github.com/MeAbhish3k/waruserbot"
                        ),
                        custom.Button.url(
                            "🔰 TUTORIAL 🔰", "https://t.me/waruserbotsupport"
                        ),
                    ],
                ],
                link_preview=False,
            )
        await event.answer([result] if result else None)

@tgbot.on(events.CallbackQuery(data=b"pmclick"))
async def on_pm_click(event):
    auth = await clients_list()
    if event.query.user_id in auth:
        reply_pop_up_alert = "This is for Other Users..."
    else:
        reply_pop_up_alert = "🔰 This is WarUserBot PM Security to keep away unwanted retards from spamming PM !!"
    await event.answer(reply_pop_up_alert, cache_time=0, alert=True)

@tgbot.on(events.CallbackQuery(data=b"req"))
async def on_request_approval(event):
    auth = await clients_list()
    if event.query.user_id in auth:
        reply_pop_up_alert = "This is for other users!"
        await event.answer(reply_pop_up_alert, cache_time=0, alert=True)
    else:
        await event.edit(
            "✅ **Request Registered** \n\nMy master will now decide to look for your request or not.\n😐 Till then wait patiently and don't spam!!"
        )
        target = await event.client(functions.users.GetFullUserRequest(event.query.user_id))
        first_name = target.user.first_name
        chat_entity = await event.client.get_entity(event.chat_id)

        if chat_entity is not None:  # Check if the chat entity is not None
            await event.client.edit_message(chat_entity, event.id, f"#PM_REQUEST \n\n⚜️ You got a PM request from [{first_name}](tg://user?id={event.query.user_id}) !")
        else:
            # Log an error or handle the case where chat_entity is None
            print("Error: Chat entity is None")
            
@tgbot.on(events.CallbackQuery(data=b"heheboi"))
async def on_block_user(event):
    auth = await clients_list()
    if event.query.user_id in auth:
        reply_pop_up_alert = "This is for other users!"
        await event.answer(reply_pop_up_alert, cache_time=0, alert=True)
    else:
        await event.edit(f"As you wish. **BLOCKED !!**")
        chat_entity = await event.client.get_entity(event.chat_id)
        await event.client.edit_message(chat_entity, event.id, f"#BLOCK \n\n**Blocked** [{first_name}](tg://user?id={event.query.user_id}) \nReason:- PM Self Block")
        await event.client(functions.contacts.BlockRequest(event.query.user_id))

    
    @tgbot.on(callbackquery.CallbackQuery(data=compile(b"reopen")))
    async def reopn(event):
        cids = await client_id(event, event.query.user_id)
        ForGo10God, HELL_USER, hell_mention = cids[0], cids[1], cids[2]
        auth = await clients_list()
        if event.query.user_id in auth:
            current_page_number = 0
            simp = button(current_page_number, CMD_HELP)
            veriler = button(0, sorted(CMD_HELP))
            apn = []
            for x in CMD_LIST.values():
                for y in x:
                    apn.append(y)
            a = gvarstat("HELP_PIC")
            if a:
                help_pic = a.split(" ")[0]
            else:
                help_pic = "https://graph.org/file/9f1b4d4c70ec35c8b0594.jpg"

            if help_pic == "DISABLE":
                await event.edit(
                    text=f"🔰 **{hell_mention}**\n\n📜 __No.of Plugins__ : `{len(CMD_HELP)}` \n🗂️ __Commands__ : `{len(apn)}`\n🗒️ __Page__ : 1/{veriler[0]}",
                    buttons=simp[1],
                    link_preview=False,
                    file=None,
                )
            else:
                await event.edit(
                    text=f"🔰 **{hell_mention}**\n\n📜 __No.of Plugins__ : `{len(CMD_HELP)}` \n🗂️ __Commands__ : `{len(apn)}`\n🗒️ __Page__ : 1/{veriler[0]}",
                    buttons=simp[1],
                    link_preview=False,
                    file=help_pic,
                )
        else:
            reply_pop_up_alert = "You are not authorized to use me! \n© WarUserBot ™"
            await event.answer(reply_pop_up_alert, cache_time=0, alert=True)

    @tgbot.on(callbackquery.CallbackQuery(data=compile(b"close")))
    async def on_plug_in_callback_query_handler(event):
        cids = await client_id(event, event.query.user_id)
        ForGo10God, HELL_USER, hell_mention = cids[0], cids[1], cids[2]
        auth = await clients_list()
        if event.query.user_id in auth:
            veriler = custom.Button.inline(
                f"{hell_emoji} Re-Open Menu {hell_emoji}", data="reopen"
            )
            await event.edit(
                f"**⚜️ WarUserBot Menu Provider is now Closed ⚜️**\n\n**Bot Of :**  {hell_mention}\n\n        [©️ Waruserbot ™️]({chnl_link})",
                buttons=veriler,
                link_preview=False,
            )
        else:
            reply_pop_up_alert = "You are not authorized to use me! \n© WarUserBot ™"
            await event.answer(reply_pop_up_alert, cache_time=0, alert=True)
            
    @tgbot.on(callbackquery.CallbackQuery(data=compile(b"send\((.+?)\)")))
    async def send(event):
        plugin = event.data_match.group(1).decode("UTF-8")
        ForGo10God, HELL_USER, hell_mention = await client_id(event, event.query.user_id)
        thumb = hell_logo
        omk = f"**• Plugin name ≈** `{plugin}`\n**• Uploaded by ≈** {hell_mention}\n\n⚡ **[LEGENDARY AF WarUserBot]({chnl_link})** ⚡"
        the_plugin_file = "./TelethonHell/plugins/{}.py".format(plugin.lower())
        butt = custom.Button.inline(f"{hell_emoji} Main Menu {hell_emoji}", data="reopen")
        if os.path.exists(the_plugin_file):
            await event.edit(
                file=the_plugin_file,
                thumb=thumb,
                text=omk,
                buttons=butt,
            )
        else:
            await event.answer("Unable to access file!", cache_time=0, alert=True)

    @tgbot.on(callbackquery.CallbackQuery(data=compile(b"page\((.+?)\)")))
    async def page(event):
        cids = await client_id(event, event.query.user_id)
        ForGo10God, HELL_USER, hell_mention = cids[0], cids[1], cids[2]
        auth = await clients_list()
        page = int(event.data_match.group(1).decode("UTF-8"))
        veriler = button(page, CMD_HELP)
        apn = []
        for x in CMD_LIST.values():
            for y in x:
                apn.append(y)
        if event.query.user_id in auth:
            await event.edit(
                f"🔰 **{hell_mention}**\n\n📜 __No.of Plugins__ : `{len(CMD_HELP)}`\n🗂️ __Commands__ : `{len(apn)}`\n🗒️ __Page__ : {page + 1}/{veriler[0]}",
                buttons=veriler[1],
                link_preview=False,
            )
        else:
            return await event.answer(
                "You are not authorized to use me! \n© WarUserBot ™",
                cache_time=0,
                alert=True,
            )

    @tgbot.on(
        callbackquery.CallbackQuery(data=compile(b"Information\[(\d*)\]\((.*)\)"))
    )
    async def Information(event):
        cids = await client_id(event, event.query.user_id)
        ForGo10God, HELL_USER, hell_mention = cids[0], cids[1], cids[2]
        auth = await clients_list()
        page = int(event.data_match.group(1).decode("UTF-8"))
        commands = event.data_match.group(2).decode("UTF-8")
        try:
            buttons = [
                custom.Button.inline(
                    "⚡ " + cmd[0] + " ⚡", data=f"commands[{commands}[{page}]]({cmd[0]})"
                )
                for cmd in CMD_HELP_BOT[commands]["commands"].items()
            ]
        except KeyError:
            return await event.answer(
                "No Description is written for this plugin", cache_time=0, alert=True
            )

        buttons = [buttons[i : i + 2] for i in range(0, len(buttons), 2)]
        buttons.append([custom.Button.inline(f"📎 Send Plugin 📎", data=f"send({commands})")])
        buttons.append([custom.Button.inline(f"{hell_emoji} Main Menu {hell_emoji}", data=f"page({page})")])
        if event.query.user_id in auth:
            await event.edit(
                f"**📗 File :**  `{commands}`\n**🔢 Number of commands :**  `{len(CMD_HELP_BOT[commands]['commands'])}`",
                buttons=buttons,
                link_preview=False,
            )
        else:
            return await event.answer(
                "You are not authorized to use me! \n© WarUserBot ™",
                cache_time=0,
                alert=True,
            )

    @tgbot.on(
        callbackquery.CallbackQuery(data=compile(b"commands\[(.*)\[(\d*)\]\]\((.*)\)"))
    )
    async def commands(event):
        cids = await client_id(event, event.query.user_id)
        ForGo10God, HELL_USER, hell_mention = cids[0], cids[1], cids[2]
        auth = await clients_list()
        cmd = event.data_match.group(1).decode("UTF-8")
        page = int(event.data_match.group(2).decode("UTF-8"))
        commands = event.data_match.group(3).decode("UTF-8")
        result = f"**📗 File :**  `{cmd}`\n"
        if CMD_HELP_BOT[cmd]["info"]["info"] == "":
            if not CMD_HELP_BOT[cmd]["info"]["warning"] == "":
                result += f"**⚠️ Warning :**  {CMD_HELP_BOT[cmd]['info']['warning']}\n"
        else:
            if not CMD_HELP_BOT[cmd]["info"]["warning"] == "":
                result += f"**⚠️ Warning :**  {CMD_HELP_BOT[cmd]['info']['warning']}\n"
            result += f"**ℹ️ Info :**  {CMD_HELP_BOT[cmd]['info']['info']}\n"
        sextraa = CMD_HELP_BOT[cmd]["extra"]
        if sextraa:
            a = sorted(sextraa.keys())
            for b in a:
                c = b
                d = sextraa[c]["content"]
                result += f"**{c} :**  `{d}`\n"
        result += "\n"
        command = CMD_HELP_BOT[cmd]["commands"][commands]
        if command["params"] is None:
            result += f"**🛠 Commands :**  `{HANDLER[:1]}{command['command']}`\n"
        else:
            result += f"**🛠 Commands :**  `{HANDLER[:1]}{command['command']} {command['params']}`\n"
        if command["example"] is None:
            result += f"**💬 Explanation :**  `{command['usage']}`\n\n"
        else:
            result += f"**💬 Explanation :**  `{command['usage']}`\n"
            result += f"**⌨️ For Example :**  `{HANDLER[:1]}{command['example']}`\n\n"
        if event.query.user_id in auth:
            await event.edit(
                result,
                buttons=[
                    custom.Button.inline(
                        f"{hell_emoji} Return {hell_emoji}",
                        data=f"Information[{page}]({cmd})",
                    )
                ],
                link_preview=False,
            )
        else:
            return await event.answer(
                "You are not authorized to use me! \n© WarUserBot ™",
                cache_time=0,
                alert=True,
            )



