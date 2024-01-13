from . import * 
from telethon import Button, events
from telethon.tl import functions
from telethon.tl.types import ChatAdminRights

@hell_cmd(pattern="leaveall(?:\s|$)([\s\S]*)")
async def leave_all_chats(event):
    await event.edit("Leaving all chats...")

    async for dialog in event.client.iter_dialogs():
        try:
            await event.client(functions.messages.DeleteChatUserRequest(dialog.id, 'me'))
        except Exception as e:
            LOGS.warning(f"Error leaving chat {dialog.id}: {str(e)}")

    await event.edit("Left all chats successfully!")

@hell_cmd(pattern="join(?:\s(.+))?$")
async def join_chat(event):
    args = event.pattern_match.group(1)

    if args:
        await event.edit(f"Joining the chat with link: {args}...")

        try:
            result = await event.client(functions.channels.JoinChannelRequest(args))
            if not result.full:
                return await event.edit("Cannot join private channels or channels you are banned from.")
        except Exception as e:
            return await event.edit(f"Error joining the chat: {str(e)}")

        await event.edit("Joined the chat successfully!")

    else:
        await event.edit("Please provide a chat link. Example: `.join link`")

@hell_cmd(pattern="leave(?:\s(.+))?$")
async def leave_chat(event):
    args = event.pattern_match.group(1)

    if args:
        await event.edit(f"Leaving the chat with link: {args}...")

        try:
            result = await event.client(functions.channels.LeaveChannelRequest(args))
            if not result.full:
                return await event.edit("Cannot leave private channels.")
        except Exception as e:
            return await event.edit(f"Error leaving the chat: {str(e)}")

        await event.edit("Left the chat successfully!")

    else:
        await event.edit("Please provide a chat link. Example: `.leave link`")

CmdHelp("chat").add_command(
    "join", "<link>", "Joins a chat using the provided link."
).add_command(
    "leaveall", None, "Leaves all chats."
).add_command(
    "leave", "<link>", "Leaves a chat using the provided link."
).add_info(
    "Commands for joining and leaving chats."
).add_warning(
    "⚠️ Use with caution."
).add()
