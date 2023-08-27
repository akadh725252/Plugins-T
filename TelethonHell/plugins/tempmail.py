from . import *
from telethon import events
from telethon.errors.rpcerrorlist import YouBlockedUserError
import asyncio

@hell_cmd(pattern="tempmail$")
async def demn(ult):
    chat = "@TempMailGenRoBot"
    msg = await eor(ult, "Generating Temporary Mail Wait 3 to 6 Second...")
    async with hellbot.conversation(chat) as conv:
        try:
            response = conv.wait_event(events.NewMessage(
                incoming=True,
                from_users=863661281
            ))
            await conv.send_message("/start")
            await asyncio.sleep(5)
            await conv.send_message("➕ Generate New / Delete")
            response = await response

            # Check if the rows list has enough elements
            if len(response.reply_markup.rows) > 2:
                # Check if the buttons list in the third row has enough elements
                buttons = response.reply_markup.rows[2].buttons
                if len(buttons) > 0:
                    link = buttons[0].url
                else:
                    link = None  # or handle the case when there are no buttons in the third row
            else:
                link = None  # or handle the case when there are not enough rows

            await hellbot.send_read_acknowledge(chat)
        except YouBlockedUserError:
            await msg.edit("Boss! Please Unblock @TempMail_org_bot")
            return
        await eor(ult, f"TEMPMAIL ~ \n`{response.message.message}`\n\n[CLICK TO VIEW INBOX](TempMail_org_bot.t.me)")

CmdHelp("tempmail").add_command(
    "tempmail", "Generate Temporary mail....!"
).add()
